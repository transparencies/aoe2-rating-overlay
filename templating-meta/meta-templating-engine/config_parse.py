import simplejson as json


# class ConfigParse():
#     """
#         Parse the config file of our overlay templates
#     """

    # def __init__(self):
with open('sample-template-config.json') as json_file:
    data = json.load(json_file)
    print(json.dumps(data, sort_keys=True, indent=3))

    for p in data['Package-Info']:
        print('Version: ' + p['Version'])
        print('Creator: ' + p['Creator'])
        print('License: ' + p['License'])
        print('')

