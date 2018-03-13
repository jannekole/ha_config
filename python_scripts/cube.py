
value = int(data.get('event'))
id = data.get('id')

lastDigits = value % 1000
firstDigit = int(value / 1000)

logger.error("value: " + str(firstDigit) + ", " + str(lastDigits) + "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")

if id == 'switch_1':
    # Shaking toggles the lights
    if value == 7007:  
        hass.bus.fire('call_service', {"service": "toggle", "domain":"light", "service_data": {"entity_id": "light.light_1"}})
    
    # flipping to side 2 or double tapping with 2 on top switches scene to red
    if firstDigit == 2 and lastDigits != 0:
        hass.bus.fire('call_service', {"service": "turn_on", "domain":"scene", "service_data": {"entity_id": "scene.red"}})
   
    # flipping to side 6 or double tapping with 6 on top switches scene to red
    if firstDigit == 6 and lastDigits != 0:
        hass.bus.fire('call_service', {"service": "turn_on", "domain":"scene", "service_data": {"entity_id": "scene.blue"}})

    # sliding play/pauses media
    if lastDigits == 0 and firstDigit < 7:
        hass.bus.fire('call_service', {"service": "media_play_pause", "domain":"media_player", "service_data": {}})

elif id == 'switch_2':
    absValue = abs(value)
    threshold = 5000
    
    # rotating left: volume down
    if value < 0:
        hass.bus.fire('call_service', {"service": "volume_down", "domain":"media_player", "service_data": {}})
        if value < -threshold:
            hass.bus.fire('call_service', {"service": "volume_down", "domain":"media_player", "service_data": {}})
    # rotating right: volume up
    else:
        hass.bus.fire('call_service', {"service": "volume_up", "domain":"media_player", "service_data": {}})
        if value > threshold:
            hass.bus.fire('call_service', {"service": "volume_up", "domain":"media_player", "service_data": {}})
