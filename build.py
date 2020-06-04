from lxml import etree

with open('templates/overlay.svg', 'rb') as svg_in:
    svg_template = svg_in.read()

if "tspan1042" in svg_template.decode("utf-8"):
    print("tspan1042")

# load the template from a file
svg_template = etree.fromstring(svg_template)
namespace = {'s': 'http://www.w3.org/2000/svg'}


def tpl_text(t, k, v):
    # find the element by id
    nodes = svg_template.xpath("//s:%s[@id = '%s']" % (t, k), namespaces=namespace)
    
    if nodes is not None and len(nodes) > 0:
        for n in nodes:
            print("%s -> %s" % (k, v))
            n.text = v
    else:
        print("%s ?" % k)


def tpl_set(t, k, a, v):
    # find the element by id
    nodes = svg_template.xpath("//s:%s[@id = '%s']" % (t, k), namespaces=namespace)
    
    if nodes is not None and len(nodes) > 0:
        for n in nodes:
            print("%s:%s -> %s" % (k, a, v))
            n.set(a, v)
            print(n.get(a))
    else:
        print("%s ?" % k)


# player names
tpl_text('tspan', 'playername_p1', '{{f.name(database.match.players.0.name)}}')
tpl_text('tspan', 'playername_p2', '{{f.name(database.match.players.1.name)}}')

# player flags
tpl_set('image', 'country_flag_p1', '{http://www.w3.org/1999/xlink}href', "{{f.flagImage(database.players.0)}}")
tpl_set('image', 'country_flag_p1', 'clip-path', 'url(#circleClip)')
tpl_set('image', 'country_flag_p2', '{http://www.w3.org/1999/xlink}href', "{{f.flagImage(database.players.1)}}")
tpl_set('image', 'country_flag_p2', 'clip-path', 'url(#circleClip)')

# ratings p1
tpl_set('g', 'player_1_rating', 'style', '{{f.showRating(database.players.0)}}')
tpl_text('tspan', 'player_1_unranked', '{{f.unranked(database.players.0)}}')

tpl_text('tspan', 'rank_p1', '{{f.rank(database.players.0)}}')
tpl_text('tspan', 'rating_p1', '{{database.players.0.rating}}')
tpl_text('tspan', 'winrate_p1', '{{f.winrate(database.players.0)}}')
tpl_text('tspan', 'wins_p1', '{{database.players.0.wins}}')
tpl_text('tspan', 'losses_p1', '{{database.players.0.losses}}')

# ratings p2
tpl_set('g', 'player_2_rating', 'style', '{{f.showRating(database.players.1)}}')
tpl_text('tspan', 'player_2_unranked', '{{f.unranked(database.players.1)}}')

tpl_text('tspan', 'rank_p2', '{{f.rank(database.players.1)}}')
tpl_text('tspan', 'rating_p2', '{{database.players.1.rating}}')
tpl_text('tspan', 'winrate_p2', '{{f.winrate(database.players.1)}}')
tpl_text('tspan', 'wins_p2', '{{database.players.1.wins}}')
tpl_text('tspan', 'losses_p2', '{{database.players.1.losses}}')

# gameTypes
tpl_text('tspan', 'gameType', '{{f.gameType(database.match)}}')
tpl_text('tspan', 'gameType2', '{{f.gameType2(database.match)}}')

# civ pictures
tpl_set('image', 'civ_img_p1', '{http://www.w3.org/1999/xlink}href', "{{f.civImage(database.match.players.0, 'left')}}")
tpl_set('image', 'civ_img_p2', '{http://www.w3.org/1999/xlink}href', "{{f.civImage(database.match.players.1, 'right')}}")

# colors
tpl_set('stop', 'color_start_p1', 'style', 'stop-color:{{f.color(database.match.players.0.color)}};stop-opacity:1;')
tpl_set('stop', 'color_stop_p1', 'style', 'stop-color:{{f.color(database.match.players.0.color)}};stop-opacity:0;')
tpl_set('stop', 'color_start_p2', 'style', 'stop-color:{{f.color(database.match.players.1.color)}};stop-opacity:1;')
tpl_set('stop', 'color_stop_p2', 'style', 'stop-color:{{f.color(database.match.players.1.color)}};stop-opacity:0;')

svg = etree.tostring(svg_template, encoding='utf8', method='xml')
if "tspan1042" in svg.decode("utf-8"):
    print("tspan1042")

# inject svg-template into html-template
with open('templates/overlay.html') as html_in:
    html_template = html_in.read()

html_template = html_template.replace('###SVG-TEMPLATE###', svg.decode("utf-8"))


with open('out/overlay.html', 'w') as html_out:
    html_out.write(html_template)
