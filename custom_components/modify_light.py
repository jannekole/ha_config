from homeassistant.const import (MATCH_ALL, ATTR_NOW)
import logging

DOMAIN = 'hello_state'

_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""
    count = 0
    hass.states.set('input_boolean.brightness_is_controlled', 'on')
    hass.states.set('light.test_light', 'on')
    hass.states.set('test_comp.test_1', {"key":"value"})
    hass.states.set('test_comp.test_2', {"key":{"innerkey":"value"}})
    default_brightness = 255
    # Listener to handle fired events
    def handle_event(event):
        data = event.as_dict()['data']
        _LOGGER.error("event")
        _LOGGER.error(event)
        _LOGGER.error("data:")
        _LOGGER.error(data)
        _LOGGER.error("event.service")
        _LOGGER.error(data['service'])
        _LOGGER.error('modified' in data)



        if event.data['domain'] == 'light' and event.data['service'] == 'turn_on' and not 'modified' in data:
            service_data = data['service_data']
            new_service_data = service_data.copy()
            brightness_is_controlled = hass.states.get('input_boolean.brightness_is_controlled').state
            default_brightness = int(float(hass.states.get('input_number.slider1').state))
            _LOGGER.error('default_brightness:')
            _LOGGER.error(default_brightness)
            if not any (key in new_service_data for key in ("brightness","brightness_pct")):
            # if not ('brightness' in new_service_data or 'brightness_pct' in new_service_data ):


                _LOGGER.error(True)
                _LOGGER.error('True')
                _LOGGER.error(brightness_is_controlled)
                if brightness_is_controlled == 'on':
                    _LOGGER.error("default bright")
                    new_service_data['brightness'] = default_brightness
            else:
                hass.states.set('input_boolean.brightness_is_controlled', 'off')
            # if not ('xy_color' in data or 'color_temp' in data ):
            #     service_data['brightness':'255']
            #new_service_data['transition'] = 20
            _LOGGER.error('got here')
            hass.bus.fire('call_service', {"modified":True,"service": "turn_on", "domain":"light", "service_data": new_service_data})


    # Listen for when my_cool_event is fired
    hass.bus.listen('call_service', handle_event)
    return True
