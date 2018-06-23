"""Code to handle a Hue bridge."""
import asyncio

import async_timeout
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import aiohttp_client, config_validation as cv

from .const import DOMAIN, LOGGER
from .errors import AuthenticationRequired, CannotConnect

SERVICE_HUE_SCENE = "hue_activate_scene"
ATTR_GROUP_NAME = "group_name"
ATTR_SCENE_NAME = "scene_name"
SCENE_SCHEMA = vol.Schema({
    vol.Required(ATTR_GROUP_NAME): cv.string,
    vol.Required(ATTR_SCENE_NAME): cv.string,
})


class HueBridge(object):
    """Manages a single Hue bridge."""

    def __init__(self, hass, config_entry, allow_unreachable, allow_groups):
        """Initialize the system."""
        self.config_entry = config_entry
        self.hass = hass
        self.allow_unreachable = allow_unreachable
        self.allow_groups = allow_groups
        self.available = True
        self.api = None
        self._cancel_retry_setup = None

    @property
    def host(self):
        """Return the host of this bridge."""
        return self.config_entry.data['host']

    async def async_setup(self, tries=0):
        """Set up a phue bridge based on host parameter."""
        host = self.host
        hass = self.hass

        try:
            self.api = await get_bridge(
                hass, host, self.config_entry.data['username'])
        except AuthenticationRequired:
            # usernames can become invalid if hub is reset or user removed.
            # We are going to fail the config entry setup and initiate a new
            # linking procedure. When linking succeeds, it will remove the
            # old config entry.
            hass.async_add_job(hass.config_entries.flow.async_init(
                DOMAIN, source='import', data={
                    'host': host,
                }
            ))
            return False

        except CannotConnect:
            retry_delay = 2 ** (tries + 1)
            LOGGER.error("Error connecting to the Hue bridge at %s. Retrying "
                         "in %d seconds", host, retry_delay)

            async def retry_setup(_now):
                """Retry setup."""
                if await self.async_setup(tries + 1):
                    # This feels hacky, we should find a better way to do this
                    self.config_entry.state = config_entries.ENTRY_STATE_LOADED

            self._cancel_retry_setup = hass.helpers.event.async_call_later(
                retry_delay, retry_setup)

            return False

        except Exception:  # pylint: disable=broad-except
            LOGGER.exception('Unknown error connecting with Hue bridge at %s',
                             host)
            return False

        hass.async_add_job(hass.config_entries.async_forward_entry_setup(
            self.config_entry, 'light'))

        hass.services.async_register(
            DOMAIN, SERVICE_HUE_SCENE, self.hue_activate_scene,
            schema=SCENE_SCHEMA)

        return True

    async def async_reset(self):
        """Reset this bridge to default state.

        Will cancel any scheduled setup retry and will unload
        the config entry.
        """
        # The bridge can be in 3 states:
        #  - Setup was successful, self.api is not None
        #  - Authentication was wrong, self.api is None, not retrying setup.
        #  - Host was down. self.api is None, we're retrying setup

        # If we have a retry scheduled, we were never setup.
        if self._cancel_retry_setup is not None:
            self._cancel_retry_setup()
            self._cancel_retry_setup = None
            return True

        # If the authentication was wrong.
        if self.api is None:
            return True

        self.hass.services.async_remove(DOMAIN, SERVICE_HUE_SCENE)

        # If setup was successful, we set api variable, forwarded entry and
        # register service
        return await self.hass.config_entries.async_forward_entry_unload(
            self.config_entry, 'light')

    async def hue_activate_scene(self, call, updated=False):
        """Service to call directly into bridge to set scenes."""
        group_name = call.data[ATTR_GROUP_NAME]
        scene_name = call.data[ATTR_SCENE_NAME]

        group = next(
            (group for group in self.api.groups.values()
             if group.name == group_name), None)

        # Additional scene logic to handle duplicate scene names across groups
        scene = next(
            (scene for scene in self.api.scenes.values()
             if scene.name == scene_name
             and group is not None
             and sorted(scene.lights) == sorted(group.lights))
            , None)

        # If we can't find it, fetch latest info.
        if not updated and (group is None or scene is None):
            await self.api.groups.update()
            await self.api.scenes.update()
            await self.hue_activate_scene(call, updated=True)
            return

        if group is None:
            LOGGER.warning('Unable to find group %s', group_name)
            return

        if scene is None:
            LOGGER.warning('Unable to find scene %s', scene_name)
            return

        await group.set_action(scene=scene.id)

async def get_bridge(hass, host, username=None):
    """Create a bridge object and verify authentication."""
    import aiohue

    bridge = aiohue.Bridge(
        host, username=username,
        websession=aiohttp_client.async_get_clientsession(hass)
    )

    try:
        with async_timeout.timeout(5):
            # Create username if we don't have one
            if not username:
                await bridge.create_user('home-assistant')
            # Initialize bridge (and validate our username)
            await bridge.initialize()

        return bridge
    except (aiohue.LinkButtonNotPressed, aiohue.Unauthorized):
        LOGGER.warning("Connected to Hue at %s but not registered.", host)
        raise AuthenticationRequired
    except (asyncio.TimeoutError, aiohue.RequestError):
        LOGGER.error("Error connecting to the Hue bridge at %s", host)
        raise CannotConnect
    except aiohue.AiohueException:
        LOGGER.exception('Unknown Hue linking error occurred')
        raise AuthenticationRequired
