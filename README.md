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
- Destiny 2 Integration

## <a name="workflow"></a>Workflow / Build Pipeline

My config is validated using [Travis CI](https://travis-ci.org/danrspencer/hass-config) after each push using the latest version of Home Assistant. HA uses a [sensor](https://github.com/danrspencer/hass-config/blob/master/sensor/misc.yaml) to monitor the Travis build state and sends me notifications of the outcome for each build.

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
