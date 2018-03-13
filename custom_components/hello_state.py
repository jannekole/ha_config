from homeassistant.const import (MATCH_ALL, ATTR_NOW)
DOMAIN = 'hello_state'

def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""
    count = 0

    # Listener to handle fired events
    def handle_event(event):
        if hass.states.get('input_boolean.hello_state_on').state == 'on':
            second = event.data[ATTR_NOW].second
            secmin  = second + (event.data[ATTR_NOW].minute * 60)
            if secmin % 9 == 0 or secmin % 11 == 0 or secmin % 23 == 0 or secmin % 19 == 0 or secmin % 7 == 0 or secmin % 5 == 0:
                hass.bus.fire('call_service', {"service": "flash", "domain":"python_script", "service_data": {"event":second, "entity_id": "light.light_1", "transition": "0", "brightness":"0"}})


    # Listen for when my_cool_event is fired
    hass.bus.listen('time_changed', handle_event)
    return True
