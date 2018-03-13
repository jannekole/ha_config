
name = 'light.' + data.get('light', 'light_1')
second = data.get('event', 0)
delay = data.get('delay', 0.01)


logger.info("Helldfsdo {}".format(name))

def lightOff(hass):
#    hass.bus.fire('call_service', {"service": "turn_off", "domain":"light", "service_data": {"entity_id": "light.light_1", "transition": "0"}})
    hass.bus.fire('call_service', {"service": "turn_on", "domain":"light", "service_data": {"entity_id": "light.light_1", "transition": "0", "brightness":"0"}})

#    hass.bus.fire('call_service', {"service": "turn_off", "domain":"light", "service_data": {"entity_id": "light.light_1"}})

def lightOn(hass, on=True, transition=0, brightn=255):
    if on:
        brightness = brightn
    else:
        brightness = "0"


    hass.bus.fire('call_service', {"service": "turn_on", "domain":"light", "service_data": {"entity_id": "light.light_1", "transition": "0", "brightness":brightness}})

lightIsOn = hass.states.get(name)
logger.warning(lightIsOn.state + 'hei')
#
sensor1 = int(hass.states.get('sensor.random_sensor').state)
sensor2 = int(hass.states.get('sensor.random_sensor_2').state)
sensor3 = int(hass.states.get('sensor.random_sensor_3').state)

shouldFlash = True
shouldFlashTwice = (second  + sensor1) % 2 or sensor1 > 60


def flash(hass, lightOn, delay, brightn):
    lightOn(hass, True, 0, brightn)
    time.sleep(delay)
    lightOn(hass, False, 0, brightn)


if shouldFlash:
    time.sleep(sensor2 / 500.0)
    flash(hass, lightOn, delay, sensor1 * 2)
if shouldFlashTwice:
    time.sleep(sensor3 / 500.0)
    flash(hass, lightOn, delay, sensor1)



# <Event call_service[L]: service=light.turn_on, entity_id=light.light_1>
# <Event call_service[L]: service_call_id=1972982544-45, service=turn_on, service_data=entity_id=light.light_1, domain=light>


#<Event call_service[L]: service_call_id=1972982544-113, service=turn_off, service_data=entity_id=light.light_1, domain=light>
#<Event call_service[L]: service=turn_iff, transition=0, domain=light, entity_id=light.light_1>
#{'service': 'turn_off', 'type': 'call_service', 'service_data': {'entity_id': 'light.light_1'}

#<Event call_service[L]: service=turn_off, domain=light, service_data=entity_id=light.light_1>

#<Event call_service[L]: service=turn_off, domain=light, service_data=entity_id=['light.light_1']>

#<Event call_service[L]: service=turn_off, domain=light, service_data=entity_id=light.light_1, transition=0>
