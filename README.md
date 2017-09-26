# Home Assistant Config

[![Build Status](https://travis-ci.org/danrspencer/hass-config.svg?branch=master)](https://travis-ci.org/danrspencer/hass-config)

My Home Assistant (HA) Config, updated pretty regularly. Feel free to steal ideas / use it for examples.

***-- this document is still very much work in progress --***

## Interesting Bits
- [Workflow / Build Pipeline](#workflow)
- [Day Phase Sensor](#day-phase-sensor)
- [Lighting Automations (Philips Hue)](#lighting-automations)
- Harmony Integration
- Hyperion Integration
- Dynamic Group For Active Media Players
- Audio Greeters
- Nest Synced Generic Thermostat
- [Destiny 2 Integration](#destiny-2)

## <a name="workflow"></a>Workflow / Build Pipeline

My config is validated by [Travis CI](https://travis-ci.org/danrspencer/hass-config) using the latest version of Home Assistant after each push. HA uses a [sensor](https://github.com/danrspencer/hass-config/blob/master/sensor/misc.yaml) to monitor the Travis build state and sends me notifications of the outcome for each build.

![Notification Example](https://github.com/danrspencer/hass-config/blob/master/documentation/images/build-notifications.jpeg)

After a successful build I use the [Makefile](https://github.com/danrspencer/hass-config/blob/master/Makefile) to push the update to Home Assistant and restart the service.

*TODO: Create a Hassio addon which can automate updating the config. Then update the notifications for a successful build to provide an actionable "Update and Restart" prompt.*

## <a name="day-phase-sensor"></a>Day Phase Sensor

The `Day Phase Sensor` is one of the lynch pins of my HA setup. It uses a combination of time and sun position to decide if the it's currently `Morning`, `Day`, `Evening` or `Night`. This allows me to easily keep automations that rely on the time of day easily in sync and removes a lot of duplication.

```yaml
- platform: template
  sensors:
    day_phase:
      friendly_name: 'Day Phase'
      value_template: >
        {% if now() > now().replace(hour=5).replace(minute=0).replace(second=0) and
            now() < now().replace(hour=9).replace(minute=0).replace(second=0) %}
            Morning
        {% elif states.sun.sun.state == "above_horizon" %}
            Day
        {% elif now() < now().replace(hour=22).replace(minute=0).replace(second=0) and
            now() > now().replace(hour=9).replace(minute=0).replace(second=0) %}
            Evening
        {% else %}
            Night
        {% endif %}
```

[Actual sensor config](https://github.com/danrspencer/hass-config/blob/master/sensor/template.yaml)

## <a name="lighting-automations"></a>Lighting Automations (Philips Hue)

The `Day Phase Sensor` allows me to keep my lighting automations very simple. For rooms with motion sensors I generally have three basic automations:

...

## <a name="destiny-2"></a>Destiny 2 Integration

I've implemented a [custom Destiny 2 sensor component](https://github.com/danrspencer/hass-config/blob/master/custom_components/sensor/destiny2.py) to monitor the subclass of my current / most recently played character in Destiny 2.

```yaml
- platform: destiny2
  membership_type: 2
  destiny_membership_id: 4611686018428481758
  api_key: !secret destiny2_api_key
```

Finding your `membership_type` and `destiny_membership_id` can be done by navigating to your profile on the Bungie website then clicking on the platform you're interested in (e.g. `PlayStation Network`).Your `membership_type` will the first number after `profile` in the url and your `destiny_membership_id` is the second number.


  e.g.

  My profile is [https://www.bungie.net/en/Profile/ **2** / **461168601842848175** /Atraignis](https://www.bungie.net/en/Profile/2/4611686018428481758/Atraignis)
  So my details are:

    membership_type: 2
    destiny_membership_id: 4611686018428481758

To get your API key you need to sign up at [Bungie's Application Portal](https://www.bungie.net/en/Application) and create an application.

Unfortunately the sensor isn't quite as responsive as I'd like due to the (extremely reasonable) rate limiting imposed by the Bungie API. The sensor should refresh roughly every 30 seconds.

---

This sensor, combined with the PS4 integration, allows me to do some [nice automations](https://github.com/danrspencer/hass-config/blob/master/automation/den/ps4.yaml) setting the lights in my games room to colors corresponding to my current subclass. It adds a bit of immersion and helps to stop me forgetting what subclass I'm currently running!

*There's potential for loads of extra automations with this component, especially if I can get OAuth working with it.*
