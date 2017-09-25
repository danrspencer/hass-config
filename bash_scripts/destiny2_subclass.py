#!/usr/bin/env python

import requests

from dateutil.parser import parse

url = "https://www.bungie.net/Platform/Destiny2/2/Profile/4611686018428481758/?components=200,201"
headers = {'X-API-Key': '03e0f76e26b04e2285ed57304bf8cf16'}

res = requests.get(url, headers=headers)

char_data_dict = res.json()['Response']['characters']['data']
char_data_list = []

for key, value in char_data_dict.iteritems():
    char_data_list.append(value)

# last_played = res.json()['Response']['characters']['data']['2305843009265083697']['dateLastPlayed']

def last_played_cmp(a, b):
    epocA = parse(a['dateLastPlayed']).strftime('%s')
    epocB = parse(b['dateLastPlayed']).strftime('%s')
    return epocA - epocB

# print(sorted(char_data_list, cmp=last_played_cmp))
