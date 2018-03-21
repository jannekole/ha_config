"""
Demo light platform that implements lights.
For more details about this platform, please refer to the documentation
https://home-assistant.io/components/demo/
"""
import random
import json

import logging

from homeassistant.helpers.discovery import listen_platform
from homeassistant.components.light import (
    ATTR_BRIGHTNESS, ATTR_COLOR_TEMP, ATTR_EFFECT,
    ATTR_RGB_COLOR, ATTR_WHITE_VALUE, ATTR_XY_COLOR, SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR_TEMP, SUPPORT_EFFECT, SUPPORT_RGB_COLOR, SUPPORT_WHITE_VALUE,
    ATTR_TRANSITION, Light)

LIGHT_COLORS = [
    [237, 224, 33],
    [255, 63, 111],
]

LIGHT_EFFECT_LIST = ['rainbow', 'none']

LIGHT_TEMPS = [240, 380]

SUPPORT_DEMO = (SUPPORT_BRIGHTNESS | SUPPORT_COLOR_TEMP | SUPPORT_EFFECT |
                SUPPORT_RGB_COLOR | SUPPORT_WHITE_VALUE)

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Set up the demo light platform."""
    isOn = True
    id = 'light.light_1'
    #originalLight = hass.states.get(id)
    #_LOGGER.error('light: ' + originalLight)
    virtualLight = DemoLight(4, "Virtual Light", isOn, True,
              LIGHT_COLORS[1], LIGHT_TEMPS[0], lightId=id, hass=hass)
    def add_devices():
        #_LOGGER.error('state_changed: flskf: ' + str(event))

        add_devices_callback([
            DemoLight(1, "Bed Light", False, True, effect_list=LIGHT_EFFECT_LIST,
                      effect=LIGHT_EFFECT_LIST[0], hass=hass),
            DemoLight(2, "Ceiling Lights", True, True,
                      LIGHT_COLORS[0], LIGHT_TEMPS[1], hass=hass),
            DemoLight(3, "Kitchen Lights", True, True,
                      LIGHT_COLORS[1], LIGHT_TEMPS[0], hass=hass),
            virtualLight
        ])
    add_devices()

    def handle_state_change(event):

        #  _LOGGER.error('state_changed: flskfj' + str(event.as_dict()))
         if event.data['entity_id'] == id:
             _LOGGER.error('state_changed: flhsjkf: ' + str(event.data['new_state'].attributes))
             virtualLight.update(event.data['new_state'])

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
        self._ct = ct or random.choice(LIGHT_TEMPS)
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

    def update(self, new_state):

        _LOGGER.error('updating: X!X!X!X!X!X!X!X!X!')

        self._attributes = new_state.attributes

        self._state = new_state.state == 'on'
        if new_state.state == 'unavailable':
            self._available = False
        else:
            self._available = True
        _LOGGER.error('updating: X!X!X!X!X!X!X!X!X!' + str(new_state.state) + str(self._state))
        # self._rgb = rgb
        # self._ct = ct or random.choice(LIGHT_TEMPS)
        # self._brightness = brightness
        # self._xy_color = xy_color
        # self._white = white
        # self._effect_list = effect_list
        # self._effect = effect

        self.schedule_update_ha_state()
        _LOGGER.error('updated')
    @property
    def should_poll(self) -> bool:
        """No polling needed for a demo light."""
        return False

    @property
    def hidden(self) -> bool:
        """Return the name of the light if any."""
        return False

    @property
    def name(self) -> str:
        """Return the name of the light if any."""
        return self._name

    @property
    def unique_id(self):
        """Return unique ID for light."""
        return self._unique_id

    @property
    def available(self) -> bool:
        """Return availability."""
        # This demo light is always available, but well-behaving components
        # should implement this to inform Home Assistant accordingly.
        return self._available

    @property
    def brightness(self) -> int:
        """Return the brightness of this light between 0..255."""

        return self._attributes.get('brightness', None)

    @property
    def xy_color(self) -> tuple:
        """Return the XY color value [float, float]."""
        return self._attributes.get('xy_color', None)

    @property
    def rgb_color(self) -> tuple:
        """Return the RBG color value."""
        return self._attributes.get('rgb', None)

    @property
    def color_temp(self) -> int:
        """Return the CT color temperature."""
        return self._attributes.get('color_temp', None)

    @property
    def white_value(self) -> int:
        """Return the white value of this light between 0..255."""
        return self._attributes.get('white_value', None)

    @property
    def effect_list(self) -> list:
        """Return the list of supported effects."""
        return self._attributes.get('effect_list', None)

    @property
    def effect(self) -> str:
        """Return the current effect."""
        return self._attributes.get('effect', None)

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        return self._state

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return self._attributes.get('supported_features', None)

    def lose_control_bri(self):
        self._controlBrightness = False

    def get_brightness(self):
        return 100

    def turn_on(self, **kwargs) -> None:
        """Turn the light on."""
        self._state = True

        service_data = {"entity_id": self._lightId}



        if ATTR_RGB_COLOR in kwargs:
            service_data[ATTR_RGB_COLOR] = kwargs[ATTR_RGB_COLOR]

        if ATTR_COLOR_TEMP in kwargs:
            service_data[ATTR_COLOR_TEMP] = kwargs[ATTR_COLOR_TEMP]


        if ATTR_BRIGHTNESS in kwargs:
            service_data[ATTR_BRIGHTNESS] = kwargs[ATTR_BRIGHTNESS]
            self.lose_control_bri()
        elif self._controlBrightness:
            service_data[ATTR_BRIGHTNESS] = self.get_brightness()

        if ATTR_XY_COLOR in kwargs:
            service_data[ATTR_XY_COLOR] = kwargs[ATTR_XY_COLOR]

        if ATTR_WHITE_VALUE in kwargs:
            service_data[ATTR_WHITE_VALUE] = kwargs[ATTR_WHITE_VALUE]

        if ATTR_EFFECT in kwargs:
            service_data[ATTR_EFFECT] = kwargs[ATTR_EFFECT]

        if ATTR_TRANSITION in kwargs:
            service_data[ATTR_TRANSITION] = kwargs[ATTR_TRANSITION]


        # service_data['']
        self.hass.bus.fire('call_service', {"service": "turn_on", "domain":"light", "service_data": service_data})

        # As we have disabled polling, we need to inform
        # Home Assistant about updates in our state ourselves.
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs) -> None:
        """Turn the light off."""
        self._state = False
        self.hass.bus.fire('call_service', {"service": "turn_off", "domain":"light", "service_data": {"entity_id": "light.light_1"}})
        # As we have disabled polling, we need to inform
        # Home Assistant about updates in our state ourselves.
        self.schedule_update_ha_state()
