"""
Virtual light that adjusts the brightness of a target light but lets the user
make temporary adjustments.
"""

from datetime import (timedelta, datetime)

import logging

from homeassistant.util.dt import (utcnow, now, parse_time)
import homeassistant.util.color as color_util
from homeassistant.helpers.event import (
    track_point_in_utc_time)
from homeassistant.components.light import (
    ATTR_BRIGHTNESS, ATTR_COLOR_TEMP, ATTR_EFFECT,
    ATTR_RGB_COLOR, ATTR_WHITE_VALUE, ATTR_XY_COLOR, SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR_TEMP, SUPPORT_EFFECT, SUPPORT_RGB_COLOR, SUPPORT_WHITE_VALUE,
    ATTR_TRANSITION, Light)
from homeassistant.components.input_boolean import InputBoolean

SUPPORT_DEMO = (SUPPORT_BRIGHTNESS | SUPPORT_COLOR_TEMP | SUPPORT_EFFECT |
                SUPPORT_RGB_COLOR | SUPPORT_WHITE_VALUE)

_LOGGER = logging.getLogger(__name__)

first = True


def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Set up the demo light platform."""
    isOn = True
    id = 'light.olohuone'
    # originalLight = hass.states.get(id)
    # _LOGGER.error('light: ' + originalLight)

    virtualLight = DemoLight(
        4, "Virtual Light", isOn, True,
        lightId=id, hass=hass)
    isControlledSwitch = InputBoolean('controlled', 'Bri is controlled', True, 'mdi:lightbulb')

    def add_devices():

        add_devices_callback([
            virtualLight,
            isControlledSwitch
        ])
    add_devices()

    def handle_state_change(event):
        global first
        #  _LOGGER.error('state_changed: flskfj' + str(event.as_dict()))
        if event.data['entity_id'] == id:
            new_state = event.data['new_state']
            virtualLight.update(new_state)
            if new_state.state == 'on' and first:
                _LOGGER.error('new_state on')
                virtualLight.turn_on()
                first = False
        elif event.data['entity_id'] == 'input_boolean.brightness_is_controlled':
            virtualLight.gain_control_bri()
            virtualLight.refresh(transition=virtualLight._default_transition)

    hass.bus.listen('state_changed', handle_state_change)


class DemoLight(Light):
    """Representation of a demo light."""

    def __init__(self, unique_id, name, state, available=False, rgb=None,
                 ct=None, brightness=180, xy_color=(.5, .5), white=200,
                 effect_list=None, effect=None, lightId=None, hass=None):
        """Initialize the light."""
        self._unique_id = unique_id
        self._name = name
        self._state = state
        self._rgb = rgb
        self._brightness = brightness
        self._xy_color = xy_color
        self._white = white
        self._effect_list = effect_list
        self._effect = effect
        self._lightId = lightId
        self._hass = hass
        self._available = True

        self._attributes = {}

        self._controlBrightness = True
        self._controlTemp = True

        self._enabled = True

        self._seconds_to_control = 60 * 60

        self._default_transition = 1
        self._control_transition = False

        self._update_interval = 30
        self._time_between = 1

        self._schedule = [
            {'time': parse_time('00:30:00'), 'brightness': 2, 'kelvin': 2200},
            {'time': parse_time('08:20:00'), 'brightness': 2, 'kelvin': 2200},
            {'time': parse_time('08:30:00'), 'brightness': 255, 'kelvin': 4000},
            {'time': parse_time('17:00:00'), 'brightness': 255, 'kelvin': 4000},
            {'time': parse_time('19:00:00'), 'brightness': 255, 'kelvin': 2700},
            {'time': parse_time('21:00:00'), 'brightness': 200, 'kelvin': 2700},
            {'time': parse_time('22:00:00'), 'brightness': 80, 'kelvin': 2400},
            {'time': parse_time('23:59:00'), 'brightness': 40, 'kelvin': 2200},

        ]

        self._delete_bri_control_timer = None
        self._delete_temp_control_timer = None
        self._delete_timer = None

    def update(self, new_state):

        self._attributes = new_state.attributes

        self._state = new_state.state == 'on'
        if new_state.state == 'unavailable':
            self._available = False
        else:
            self._available = True

        self.schedule_update_ha_state()

    @property
    def should_poll(self):
        """No polling needed for a demo light."""
        return False

    @property
    def hidden(self):
        """Return the name of the light if any."""
        return False

    @property
    def name(self):
        """Return the name of the light if any."""
        return self._name

    @property
    def unique_id(self):
        """Return unique ID for light."""
        return self._unique_id

    @property
    def available(self):
        """Return availability."""
        # This demo light is always available, but well-behaving components
        # should implement this to inform Home Assistant accordingly.
        return self._available

    @property
    def brightness(self):
        """Return the brightness of this light between 0..255."""

        return self._attributes.get('brightness', None)

    @property
    def xy_color(self):
        """Return the XY color value [float, float]."""
        return self._attributes.get('xy_color', None)

    @property
    def rgb_color(self):
        """Return the RBG color value."""
        return self._attributes.get('rgb', None)

    @property
    def color_temp(self):
        """Return the CT color temperature."""
        return self._attributes.get('color_temp', None)

    @property
    def white_value(self):
        """Return the white value of this light between 0..255."""
        return self._attributes.get('white_value', None)

    @property
    def effect_list(self):
        """Return the list of supported effects."""
        return self._attributes.get('effect_list', None)

    @property
    def effect(self):
        """Return the current effect."""
        return self._attributes.get('effect', None)

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    @property
    def supported_features(self):
        """Flag supported features."""
        return self._attributes.get('supported_features', None)

    def isEnabled(self):
        _LOGGER.error(str(self.hass.states.get('input_boolean.brightness_is_controlled')))
        return self.hass.states.get('input_boolean.brightness_is_controlled').state == 'on'

    # def replaceTimer(self, time):
    #     if self._delete_timer is not None:
    #         self._delete_timer()
    #     self._delete_timer = track_point_in_utc_time(
    #         self.hass,
    #         self.refresh,
    #         utcnow() + timedelta(seconds=time)
    #     )

    def refresh(self, now=None, transition=None):
        if transition is None:
            transition = self._update_interval
        _LOGGER.error(
            'refresh DDDDDDDDDDDDDDDDDDDDDd: ' + str(utcnow() + timedelta(seconds=transition)))

        if self._delete_timer is not None:
            self._delete_timer()

        if self._state is True and self.isEnabled():
            self.turn_on(transition=transition)

        # self._delete_timer = track_point_in_utc_time(
        #     self.hass,
        #     self.refresh,
        #     utcnow() + timedelta(seconds=transition)
        # )
        _LOGGER.error(
            'track time DDDDDDDDDDDDDDDDDDDDDd: ' + str(utcnow() + timedelta(seconds=transition)))

    def gain_control_bri(self, now=None):
        if self._delete_bri_control_timer is not None:
            self._delete_bri_control_timer()
        _LOGGER.error('gain_control_bri')
        self._controlBrightness = True

    def lose_control_bri(self):
        if self._delete_bri_control_timer is not None:
            self._delete_bri_control_timer()

        self._controlBrightness = False
        self._delete_bri_control_timer = track_point_in_utc_time(
            self.hass,
            self.gain_control_all,
            utcnow() + timedelta(seconds=self._seconds_to_control)
        )
        _LOGGER.error('lose_control_bri:  ' + str(utcnow() + timedelta(seconds=self._seconds_to_control)))

    def gain_control_temp(self, now=None):
        if self._delete_bri_control_timer is not None:
            self._delete_bri_control_timer()
        self._controlTemp = True

    def lose_control_temp(self):
        if self._delete_bri_control_timer is not None:
            self._delete_bri_control_timer()

        self._controlTemp = False
        self._delete_bri_control_timer = track_point_in_utc_time(
            self.hass,
            self.gain_control_all,
            utcnow() + timedelta(seconds=self._seconds_to_control)
        )

    def gain_control_all(self, now=None):
        self.gain_control_temp(now)
        self.gain_control_bri(now)

    def getPrev(self, current_time):
        time = datetime.combine(now().date(), parse_time('13:45:00'))
        out = {'time': time, 'brightness': 255}
        _LOGGER.error('prev: ' + str(out))
        return out

    def getNextOfDay(self, current_time, day):
        out = None
        prev = None
        for t in self._schedule:
            next_time = datetime.combine(
                day,
                t['time']
            )

            if next_time > current_time:
                out = t.copy()
                out['time'] = next_time

                break
            prev = t.copy()
            prev['time'] = next_time
        return (prev, out)

    def getNext(self, current_time):

        today = now().date()

        (prev, out) = self.getNextOfDay(current_time, today)

        if prev is None:
            yesterday = today - timedelta(days=1)
            (prev, out2) = self.getNextOfDay(current_time, yesterday)

        if out is None:
            tomorrow = today + timedelta(days=1)
            (prev2, out) = self.getNextOfDay(current_time, tomorrow)

        _LOGGER.error('SSSSSSSSSSSSSSSSSS prev: ' + str(prev))
        return (prev, out)

    def get_brightness(self, offset_secs):
        current_time = now().replace(tzinfo=None)

        (prev, next) = self.getNext(current_time + timedelta(seconds=offset_secs))
        # next = self.getNext(current_time + timedelta(seconds=offset_secs))
        _LOGGER.error('KKKKKKKKKKKK prev: ' + str(prev))
        elapsed_time = now().replace(tzinfo=None) - prev['time']
        delta_time = next['time'] - prev['time']
        delta_brightness = next['brightness'] - prev['brightness']
        current_brightness = (elapsed_time / delta_time * delta_brightness + prev['brightness'])

        return current_brightness

    def get_temp(self, offset_secs):
        current_time = now().replace(tzinfo=None)

        (prev, next) = self.getNext(current_time + timedelta(seconds=offset_secs))
        elapsed_time = now().replace(tzinfo=None) - prev['time']
        delta_time = next['time'] - prev['time']

        prev_temp = self.temp_from_schedule(prev)
        next_temp = self.temp_from_schedule(next)

        if prev_temp is None or next_temp is None:
            return None

        delta_temp = next_temp - prev_temp

        current_temp = (elapsed_time / delta_time * delta_temp + prev_temp)

        return current_temp

    def temp_from_schedule(self, schedule):
        temp = schedule.get('mired')
        if temp is None:
            kelvin = schedule.get('kelvin')
            if kelvin is not None:
                temp = color_util.color_temperature_kelvin_to_mired(kelvin)
        return temp

    def turn_on(self, **kwargs):
        """Turn the light on."""
        self._state = True

        if self._delete_timer is not None:
            self._delete_timer()

        service_data = {"entity_id": self._lightId}

        if ATTR_TRANSITION in kwargs:
            service_data[ATTR_TRANSITION] = int(str(kwargs[ATTR_TRANSITION]))
        else:
            service_data[ATTR_TRANSITION] = self._default_transition

        if ATTR_RGB_COLOR in kwargs:
            service_data[ATTR_RGB_COLOR] = kwargs[ATTR_RGB_COLOR]

        if ATTR_COLOR_TEMP in kwargs:
            service_data[ATTR_COLOR_TEMP] = kwargs[ATTR_COLOR_TEMP]
            self.lose_control_temp()
        elif self._controlTemp:
            service_data[ATTR_COLOR_TEMP] = self.get_temp(
                service_data[ATTR_TRANSITION]
            )
            _LOGGER.error(str(service_data[ATTR_COLOR_TEMP]))

        if ATTR_BRIGHTNESS in kwargs:
            service_data[ATTR_BRIGHTNESS] = kwargs[ATTR_BRIGHTNESS]
            self.lose_control_bri()
        elif self._controlBrightness:
            service_data[ATTR_BRIGHTNESS] = self.get_brightness(
                service_data[ATTR_TRANSITION]
            )

        if ATTR_XY_COLOR in kwargs:
            service_data[ATTR_XY_COLOR] = kwargs[ATTR_XY_COLOR]

        if ATTR_WHITE_VALUE in kwargs:
            service_data[ATTR_WHITE_VALUE] = kwargs[ATTR_WHITE_VALUE]

        if ATTR_EFFECT in kwargs:
            service_data[ATTR_EFFECT] = kwargs[ATTR_EFFECT]

        self._delete_timer = track_point_in_utc_time(
            self.hass,
            self.refresh,
            utcnow().replace(microsecond=0) +
            timedelta(seconds=service_data[ATTR_TRANSITION] + self._time_between)
        )

        if service_data[ATTR_TRANSITION] == 1:
            del service_data[ATTR_TRANSITION]
        # service_data['']
        self.hass.bus.fire('call_service', {
            "service": "turn_on",
            "domain": "light",
            "service_data": service_data})

        # As we have disabled polling, we need to inform
        # Home Assistant about updates in our state ourselves.
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        if self._delete_timer is not None:
            self._delete_timer()
        """Turn the light off."""
        self._state = False
        self.gain_control_all()
        self.hass.bus.fire('call_service', {
            "service": "turn_off",
            "domain": "light",
            "service_data": {"entity_id": self._lightId}})
        # As we have disabled polling, we need to inform
        # Home Assistant about updates in our state ourselves.
        self.schedule_update_ha_state()
