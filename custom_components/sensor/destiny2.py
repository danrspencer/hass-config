import datetime
import logging
import requests
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_API_KEY,
    CONF_NAME
)
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

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

DEFAULT_NAME = 'Destiny2'
CONF_MEMBERSHIP_TYPE = 'membership_type'
CONF_DESTINY_MEMBERSHIP_ID = 'destiny_membership_id'

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_MEMBERSHIP_TYPE): cv.string,
    vol.Required(CONF_DESTINY_MEMBERSHIP_ID): cv.string,
    vol.Required(CONF_API_KEY): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string
})

def dict_to_list(dict):
    list = []
    for key, value in dict.items():
        list.append(value)
    return list

def get_date_last_played(record):
    date_last_played = datetime.datetime.strptime(record['dateLastPlayed'], "%Y-%m-%dT%H:%M:%SZ")
    return date_last_played.strftime('%s')

def get_current_element(equipment):
    for item in equipment['items']:
        if item['itemHash'] in ARC:
            return 'Arc'
        if item['itemHash'] in VOID:
            return 'Void'
        if item['itemHash'] in SOLAR:
            return 'Solar'
    return 'Unknown'

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    name = config.get(CONF_NAME)
    membership_type = config.get(CONF_MEMBERSHIP_TYPE)
    destiny_membership_id = config.get(CONF_DESTINY_MEMBERSHIP_ID)
    api_key = config.get(CONF_API_KEY)

    add_devices([Destiny2Sensor(name, membership_type, destiny_membership_id, api_key)])

class Destiny2Sensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, name, membership_type, destiny_membership_id, api_key):
        """Initialize the sensor."""
        _LOGGER.info('Initialize Destiny2 sensor: ' + name)

        self._state = 'Unknown'

        self._name = name
        self._membership_type = membership_type
        self._destiny_membership_id = destiny_membership_id
        self._api_key = api_key

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @Throttle(datetime.timedelta(seconds=30))
    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        try:
            url = "https://www.bungie.net/Platform/Destiny2/" + self._membership_type + "/Profile/" + self._destiny_membership_id + "/?components=200,205"
            headers = {'X-API-Key': self._api_key}

            _LOGGER.info('Requesting to: ' + url)
            _LOGGER.info('API Key: ' + self._api_key)

            response = requests.get(url, headers=headers)

            _LOGGER.info('Got response from Destiny2 api...')

            characters = response.json()['Response']['characters']['data']
            equipment = response.json()['Response']['characterEquipment']['data']

            sorted_chars_list = sorted(dict_to_list(characters), key=get_date_last_played, reverse=True)
            most_recent_char_id = sorted_chars_list[0]['characterId']

            most_recent_char_equip = equipment[most_recent_char_id]

            self._state = get_current_element(most_recent_char_equip)
        except:
            _LOGGER.error('Unexpected error: ' + sys.exc_info()[0])
            self._state = 'Error'
