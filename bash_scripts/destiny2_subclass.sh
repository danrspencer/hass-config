#!/usr/bin/env bash

set -e

API_KEY=`less ${1} | grep destiny2_api_key |  awk '{print $2}'`

echo ${API_KEY}

STRIKER=2958378809
SUNBREAKER=3105935002
SENTINEL=3382391785

NIGHTSTALKER=3225959819
ARCSTRIDER=1334959255
GUNSLINGER=3635991036

VOIDWALKER=3887892656
DAWNBLADE=3481861797
STORMCALLER=1751782730

RES=`curl -s --header "X-API-Key: ${API_KEY}" https://www.bungie.net/Platform/Destiny2/2/Profile/4611686018428481758/?components=203`

echo ${RES}

if [[ ${RES} == *"${STORMCALLER}"* ]];
then
  echo "Arc"
elif [[ ${RES} == *"${DAWNBLADE}"* ]];
then
  echo "Solar"
elif [[ ${RES} == *"${VOIDWALKER}"* ]];
then
  echo "Void"
else
  echo "Unknown"
fi
