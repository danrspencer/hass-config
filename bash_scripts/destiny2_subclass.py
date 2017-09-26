#!/usr/bin/env python

import requests

from dateutil.parser import parse

STORMCALLER = 1751782730
VOIDWALKER = 3887892656
DAWNBLADE = 3481861797

ARCSTRIDER = 1334959255
NIGHTSTALKER = 3225959819
GUNSLINGER = 3635991036

STRIKER = 2958378809
SENTINEL = 3382391785
SUNBREAKER = 3105935002

ARC = [STORMCALLER, ARCSTRIDER, STRIKER]
VOID = [VOIDWALKER, NIGHTSTALKER, SENTINEL]
SOLAR = [DAWNBLADE, GUNSLINGER, SUNBREAKER]

def dictToList(dict):
    list = []
    for key, value in dict.items():
        list.append(value)
    return list

def getDateLastPlayed(record):
    return parse(record['dateLastPlayed']).strftime('%s')

def getCurrentElement(equipment):
    for item in equipment['items']:
        if item['itemHash'] in ARC:
            return 'Arc'
        if item['itemHash'] in VOID:
            return 'Void'
        if item['itemHash'] in SOLAR:
            return 'Solar'
    return 'Unknown'

try:
    url = "https://www.bungie.net/Platform/Destiny2/2/Profile/4611686018428481758/?components=200,205"
    headers = {'X-API-Key': '03e0f76e26b04e2285ed57304bf8cf16'}

    response = requests.get(url, headers=headers)

    characters = response.json()['Response']['characters']['data']
    equipment = response.json()['Response']['characterEquipment']['data']

    sortedCharsList = sorted(dictToList(characters), key=getDateLastPlayed, reverse=True)
    mostRecentCharId = sortedCharsList[0]['characterId']

    mostRecentCharEquip = equipment[mostRecentCharId]

    currentElement = getCurrentElement(mostRecentCharEquip)

    print(currentElement)
except:
    print('Unknown')
