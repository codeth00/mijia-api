import json
import time
import sys
sys.path.extend(['.', '..'])
from mijiaAPI import mijiaAPI

with open('jsons/auth.json') as f:
    auth = json.load(f)
api = mijiaAPI(auth)


# ---------------------- get devices list ----------------------
devices = api.get_devices_list()['list']
with open('jsons/devices.json', 'w') as f:
    json.dump(devices, f, indent=2, ensure_ascii=False)
time.sleep(0.5)

# ---------------------- get homes list ------------------------
homes = api.get_homes_list()['homelist']
with open('jsons/homes.json', 'w') as f:
    json.dump(homes, f, indent=2, ensure_ascii=False)
time.sleep(0.5)

# ---------------------- get scenes list -----------------------
home_id = homes[0]['id']
scenes = api.get_scenes_list(home_id)['scene_info_list']
with open('jsons/scenes.json', 'w') as f:
    json.dump(scenes, f, indent=2, ensure_ascii=False)
time.sleep(0.5)

# ---------------------- run scene -----------------------------
# scence_id = scenes[0]['scene_id']
# scence_name = scenes[0]['name']
# scence_id = '1721535555688607744'
# scence_name = '双键无线开关2单击左键-开/关卧室吸顶灯'
# trigger_key = 'event.3.1012'
scence_id = '1716484888997294080'
scence_name = '开面板灯'
trigger_key = 'user.click'
ret = api.run_scene(scence_id,trigger_key=trigger_key)
print(f'Run scene {scence_name}: {ret}')
time.sleep(0.5)

# # ---------------------- get consumable items ------------------
consumable_items = api.get_consumable_items(home_id)['items']
with open('jsons/consumable_items.json', 'w') as f:
    json.dump(consumable_items, f, indent=2, ensure_ascii=False)
time.sleep(0.5)

# ---------------------- get/set device properties -------------
# look for did and model in devices.json
# look for siid and piid in https://home.miot-spec.com/spec/{model}
# or it's feasible to use `run_scene`` to set the device properties
# did = devices[0]['did']
# name = devices[0]['name']
did = '493371712'
name = '米家追光氛围灯带'
# model = 'philips.light.strip3'
# 访问链接获取siid、piid，有点卡等个十几秒，https://home.miot-spec.com/spec/philips.light.strip3

brightness_piid = 3
color_temperature_piid = 4
ret = api.get_devices_prop([
    {"did": did, "siid": 2, "piid": brightness_piid},
    {"did": did, "siid": 2, "piid": color_temperature_piid},
])
print(f'ret_get_devices_prop:{ret}')
brightness = ret[0]['value']
color_temperature = ret[1]['value']
print(f'Get device {name} properties:\nBrightness: {brightness}%\n'
      f'Color temperature: {color_temperature}K')
time.sleep(0.5)

ret = api.set_devices_prop([
    {"did": did, "siid": 2, "piid": brightness_piid, "value": 10},
    {"did": did, "siid": 2, "piid": color_temperature_piid, "value": 2700},
])
print(f'ret_set_devices_prop:{ret}')
print(f'Set device {name} properties:\n'
      f'Brightness: {"Success" if ret[0]["code"] == 0 else "Failed"}\n'
      f'Color temperature: {"Success" if ret[1]["code"] == 0 else "Failed"}')
