# Copyright 2020-2020 the aoe-assoc authors. See COPYING.md for legal info.

from aiohttp import web, hdrs, WSCloseCode
import asyncio
import aiohttp
import aiohttp_cors
import yaml
from collections import defaultdict
from weakref import WeakSet
import json


async def fetch(url, params, session, text=False):
    async with session.get(url, params=params) as resp:
        if resp.status == 200:
            if text:
                return await resp.text()
            else:
                return await resp.json(content_type=None)
        else:
            return None


async def get_reference_players(session):
    data = await fetch('https://raw.githubusercontent.com/SiegeEngineers/aoc-reference-data/master/data/players.yaml',
                       params={},
                       session=session,
                       text=True)
    players = yaml.load(data, Loader=yaml.SafeLoader)
    aliases = dict()
    for player in players:
        if 'platforms' in player and player['platforms'] is not None and 'de' in player['platforms']:
            for profile_id in player['platforms']['de']:
                if profile_id.isnumeric():
                    aliases[int(profile_id)] = player['name']

    return aliases


async def root(request):
    return web.Response(text="aoe2obs")


async def matchinfo(request):
    profile_id = request.rel_url.query.get('profile_id', None)
    if profile_id is not None:
        params = {'game': 'aoe2de', 'profile_id': profile_id}

    steam_id = request.rel_url.query.get('steam_id', None)
    if steam_id is not None:
        params = {'game': 'aoe2de', 'steam_id': steam_id}

    if profile_id is None and steam_id is None:
        return web.json_response(data={'error': 'Please provide either a steam_id or a profile_id'})

    data = dict()

    data['match'] = await fetch('https://aoe2.net/api/player/lastmatch',
                                params=params,
                                session=request.app['CLIENT_SESSION'])
    if data['match'] is None:
        return web.json_response(data={'error': 'Player not found'})

    data['match'] = data['match']['last_match']

    # if the lobby is an unranked custom lobby, return 1v1 leaderboard info instead
    leaderboard_id = data['match']['leaderboard_id']
    if leaderboard_id == 0:
        leaderboard_id = 3

    data['players'] = await asyncio.gather(*[fetch('https://aoe2.net/api/leaderboard',
                                                   params={'game': 'aoe2de',
                                                           'profile_id': p['profile_id'],
                                                           'leaderboard_id': leaderboard_id},
                                                   session=request.app['CLIENT_SESSION'])
                                             if p['profile_id'] is not None else asyncio.sleep(0)
                                             for p in data['match']['players']])

    data['players'] = [x['leaderboard'][0] if x is not None and len(x['leaderboard']) > 0 else None for x in data['players']]

    history = await asyncio.gather(*[fetch('https://aoe2.net/api/player/ratinghistory',
                                           params={'game': 'aoe2de',
                                                   'profile_id': p['profile_id'],
                                                   'leaderboard_id': leaderboard_id,
                                                   'count': 1},
                                           session=request.app['CLIENT_SESSION'])
                                     if data['players'][p_idx] is None else asyncio.sleep(0)
                                     for p_idx, p in enumerate(data['match']['players'])])

    # map fieldnames
    for p_idx, p in enumerate(history):
        if p is not None and len(p) > 0:
            data['players'][p_idx] = {
                "historic": True,
                "rating": p[0]['rating'],
                "wins": p[0]['num_wins'],
                "losses": p[0]['num_losses'],
                "streak": p[0]['streak'],
                "drops": p[0]['drops'],
                "timestamp": p[0]['timestamp']
            }

    for player in data['match']['players']:
        if player is not None:
            # get alias name
            if player['profile_id'] in request.app['REFERENCE_PLAYERS']:
                player['name'] = request.app['REFERENCE_PLAYERS'][player['profile_id']]

    return web.json_response(data=data)


async def send_message(request):
    channel = request.rel_url.query.get('channel', None)
    message = request.rel_url.query.get('message', None)
    if channel is None or message is None:
        web.json_response(data={'error': 'Specify the channel and a message to send.'})

    try:
        for ws in request.app['CHANNELS'][channel]:
            await ws.send_str(message)
    except IndexError:
        pass

    return web.Response(text="Done.")


async def websocket_handler(request):
    ws = web.WebSocketResponse(heartbeat=30)
    await ws.prepare(request)

    request.app['WEBSOCKETS'].add(ws)
    print("new socket connection")
    try:
        async for msg in ws:
            print("msg %s" % str(msg))
            if msg.type == aiohttp.WSMsgType.TEXT:
                print("type text")
                try:
                    data = json.loads(msg.data)
                    print(data)
                    if data['action'] == "subscribe":
                        request.app['CHANNELS'][data['channel']].add(ws)
                except (json.JSONDecodeError, IndexError, ValueError) as e:
                    print(e)
                    continue

    finally:
        for channel in request.app['CHANNELS']:
            request.app['CHANNELS'][channel].discard(ws)

        request.app['WEBSOCKETS'].discard(ws)

    return ws

app = web.Application()
app.add_routes([web.get('/', root), web.get('/matchinfo', matchinfo),
                web.get('/ws', websocket_handler), web.get('/send_message', send_message)])

cors = aiohttp_cors.setup(app, defaults={
    "https://share.polskafan.de": aiohttp_cors.ResourceOptions(allow_credentials=True,
                                                               expose_headers="*",
                                                               allow_headers="*"),
    "https://twitch.polskafan.de": aiohttp_cors.ResourceOptions(allow_credentials=True,
                                                                expose_headers="*",
                                                                allow_headers="*"),
})

# Configure CORS on all routes.
for route in list(app.router.routes()):
    cors.add(route)


async def persistent_session(app):
    app['CLIENT_SESSION'] = session = aiohttp.ClientSession()
    app['REFERENCE_PLAYERS'] = await get_reference_players(session=session)
    app['WEBSOCKETS'] = WeakSet()
    app['CHANNELS'] = defaultdict(WeakSet)
    yield
    await session.close()
    for ws in set(app['websockets']):
        await ws.close(code=WSCloseCode.GOING_AWAY,
                       message='Server shutdown')

app.cleanup_ctx.append(persistent_session)

if __name__ == '__main__':
    web.run_app(app, port=9090)
