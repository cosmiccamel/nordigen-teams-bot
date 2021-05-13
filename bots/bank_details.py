# # import requests
# import urllib.error, urllib.request, urllib.parse
# import json
# #
# # target = 'http://py4e-data.dr-chuck.net/json?'
# # local = input('Enter location: ')
# # url = target + urllib.parse.urlencode({'address': local, 'key' : 42})
# #
# # print('Retriving', url)
# # data = urllib.request.urlopen(url).read()
# # print('Retrived', len(data), 'characters')
# # js = json.loads(data)
# # print(json.dumps(js, indent = 4))
# # print('Place id', js['results'][0]['place_id'])
#
#
#
# url = "https://bank-country.azurewebsites.net/api/" \
#       "country?code=w7LXvmkwLHgSZ/UgRxNrULA3rzPW8qvrFOqAwcnh1piUvD5bAJENKQ==&bank-country="
#
# bankCardJson = """{
#     "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
#     "type": "AdaptiveCard",
#     "version": "1.3",
#     "body": [
#
#         {
#             "type": "TextBlock",
#             "text": "Select Bank",
#             "wrap": true
#         },
#         {
#             "type": "Input.ChoiceSet",
#             "id": "bankID",
#             "choices": [
#                 {
#                     "title": "ICICI",
#                     "value": "ic"
#                 },
#                 {
#                     "title": "HDFC",
#                     "value": "hd"
#                 }
#             ]
#         }
#     ],
#     "actions": [
#         {
#             "type": "Action.Submit",
#             "title": "Submit",
#             "data": {
#                 "id": "2"a
#             }
#         }
#     ]
# }
# """
#
#
# def getBanks(cc):
#
#     findUrl=f"{url}{cc}"
#     data = urllib.request.urlopen(findUrl).read()
#     # upData =
#
#     # Remove other data
#     js = json.loads(data)
#
#     new_dictArry = []
#     for items in js:
#         # new_dictArry.append({key:val for key, val in items.items() if key not in ('bic' , 'countries' , 'countries') })
#
#         new_dictArry.append({'value' : items.get('id'),
#                              'title': items.get('name')})
#
#
#     # print(new_dictArry)
#
#     bankJson = json.loads(bankCardJson)
#
#     bankJson["body"][1]["choices"] = new_dictArry
#
#     return  json.dumps(bankJson)
#
# if __name__ == '__main__':
#     # getBanks('ee')
#
#     print(getBanks('ee'))
#
