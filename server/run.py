from aiohttp import web, hdrs
import asyncio
import aiohttp
import aiohttp_cors
import yaml

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
    data = await fetch('https://raw.githubusercontent.com/SiegeEngineers/aoc-reference-data/master/data/players.yaml', params={}, session=session, text=True)
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

    data['match'] = await fetch('https://aoe2.net/api/player/lastmatch', params=params, session=request.app['CLIENT_SESSION'])
    if data['match'] is None:
        return web.json_response(data={'error': 'Player not found'})

    data['match'] = data['match']['last_match']

    # if the lobby is an unranked custom lobby, return 1v1 leaderboard info instead
    leaderboard_id = data['match']['leaderboard_id']
    if leaderboard_id == 0:
       leaderboard_id = 3

    data['players'] = await asyncio.gather(*[fetch('https://aoe2.net/api/leaderboard', params={'game': 'aoe2de', 'profile_id': p['profile_id'], 'leaderboard_id': leaderboard_id}, session=request.app['CLIENT_SESSION']) for p in data['match']['players']])
    data['players'] = [p['leaderboard'][0] for p in data['players']]

    for player in data['match']['players']:
        if player is not None:
            # get alias name
            if player['profile_id'] in request.app['REFERENCE_PLAYERS']:
                player['name'] = request.app['REFERENCE_PLAYERS'][player['profile_id']]

    return web.json_response(data=data)


app = web.Application()
app.add_routes([web.get('/', root), web.get('/matchinfo', matchinfo)])

cors = aiohttp_cors.setup(app, defaults={
    "https://share.polskafan.de": aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*")
})

# Configure CORS on all routes.
for route in list(app.router.routes()):
    cors.add(route)


async def persistent_session(app):
    app['CLIENT_SESSION'] = session = aiohttp.ClientSession()
    app['REFERENCE_PLAYERS'] = await get_reference_players(session=session)
    yield
    await session.close()

app.cleanup_ctx.append(persistent_session)

if __name__ == '__main__':
    web.run_app(app, port=9090)
