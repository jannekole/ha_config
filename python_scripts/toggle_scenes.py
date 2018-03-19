
id = data.get('id')

entities = hass.states.all()


state_id = 'scenes_toggle.scene_num'

prev_scene = hass.states.get(state_id).state or 0
prev_scene = int(prev_scene)

    

logger.error('prev_scene: ' + str(prev_scene) + 'xxxxxxxxxxxxxxxxxxxxxxx')


scenes = []

for entity in entities:
    if entity.domain == 'scene':
        scenes.append(entity)
        logger.error(entity.as_dict()['attributes'])

def getName(scene):
    return scene.name

scenes = sorted(scenes, key=getName)

numOfScenes = len(scenes)
    
new_scene = (prev_scene + 1) % numOfScenes

hass.states.set(state_id, new_scene)

new_scene_name = scenes[new_scene].object_id
hass.bus.fire('call_service', {"service": "turn_on", "domain":"scene", "service_data": {"entity_id": "scene." + new_scene_name}})


logger.error("num: " + str(scenes) +  "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")

