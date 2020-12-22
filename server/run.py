# Copyright 2020-2020 the aoe-assoc authors. See COPYING.md for legal info.

from aiohttp import web, WSCloseCode
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


async def update_reference_players(app_ctx):
    while True:
        data = await fetch('https://raw.githubusercontent.com/SiegeEngineers/aoc-reference-data/master/data/players.yaml',
                           params={},
                           session=app_ctx['CLIENT_SESSION'],
                           text=True)
        players = yaml.load(data, Loader=yaml.SafeLoader)

        reference_players_by_profile_id = dict()
        for player in players:
            if 'platforms' in player and player['platforms'] is not None and 'de' in player['platforms']:
                for profile_id in player['platforms']['de']:
                    if profile_id.isnumeric():
                        reference_players_by_profile_id[int(profile_id)] = player

        if len(reference_players_by_profile_id) > 0:
            app_ctx['REFERENCE_PLAYERS'] = reference_players_by_profile_id

        await asyncio.sleep(3600)



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

    # return the requested id first
    if profile_id is not None:
        data['match']['players'] = list(filter(lambda x: str(x['profile_id']) == profile_id, data['match']['players'])) + \
                                   list(filter(lambda x: str(x['profile_id']) != profile_id, data['match']['players']))
    else:
        data['match']['players'] = list(filter(lambda x: str(x['steam_id']) == steam_id, data['match']['players'])) + \
                                   list(filter(lambda x: str(x['steam_id']) != steam_id, data['match']['players']))

    # include AI in player count
    data['match']['num_players'] = len([p for p in data['match']['players'] if 'profile_id' in p])

    # if the lobby is an unranked custom lobby, return 1v1 leaderboard info instead
    leaderboard_id = data['match']['leaderboard_id']
    if leaderboard_id == 0:
        if data['match']['game_type'] == 2:
            leaderboard_id = 1
        else:
            leaderboard_id = 3

    ladder_data = await asyncio.gather(*[fetch('https://aoe2.net/api/leaderboard',
                                               params={'game': 'aoe2de',
                                                         'profile_id': p['profile_id'],
                                                         'leaderboard_id': leaderboard_id},
                                               session=request.app['CLIENT_SESSION'])
                                         if p['profile_id'] is not None else asyncio.sleep(0)
                                         for p in data['match']['players']])

    # filter to first returned result, return None if nothing was found
    ladder_data = [x['leaderboard'][0] if x is not None and len(x['leaderboard']) > 0 else None for x in ladder_data]

    historic_data = await asyncio.gather(*[fetch('https://aoe2.net/api/player/ratinghistory',
                                           params={'game': 'aoe2de',
                                                   'profile_id': p['profile_id'],
                                                   'leaderboard_id': leaderboard_id,
                                                   'count': 1},
                                           session=request.app['CLIENT_SESSION'])
                                           if p['profile_id'] is not None and
                                           ladder_data[p_idx] is None else asyncio.sleep(0)
                                           for p_idx, p in enumerate(data['match']['players'])])

    # filter to first returned result, return None if nothing was found
    historic_data = [history[0] if history is not None and len(history) > 0 else None for history in historic_data]

    for player_idx, player in enumerate(data['match']['players']):
        if player is not None:
            # store reference object for front end replacements
            if player['profile_id'] in request.app['REFERENCE_PLAYERS']:
                player['reference'] = request.app['REFERENCE_PLAYERS'][player['profile_id']]

            if ladder_data[player_idx] is not None:
                # store rating info
                player['rating'] = ladder_data[player_idx]
                player['rating']['historic'] = False
            elif historic_data[player_idx] is not None:
                # store history info
                player['rating'] = historic_data[player_idx]
                player['rating']['historic'] = True
            else:
                player['rating'] = None

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
    "https://overlays.polskafan.de": aiohttp_cors.ResourceOptions(allow_credentials=True,
                                                                  expose_headers="*",
                                                                  allow_headers="*"),
})

# Configure CORS on all routes.
for route in list(app.router.routes()):
    cors.add(route)


async def persistent_session(app):
    app['CLIENT_SESSION'] = session = aiohttp.ClientSession()
    app['REFERENCE_PLAYERS'] = dict()
    app['ALIAS_TASK'] = asyncio.ensure_future(update_reference_players(app))
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
