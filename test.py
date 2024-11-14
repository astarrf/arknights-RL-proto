import json

config = json.load(open("./arknights-RL-proto/operations/01.json"))
print(config['MAP_WIDTH'])
print(config['MAP_HEIGHT'])
print(config['map_hl'])
print(config['map_deploy'])
print(config['map_mv'])
print(config['doctor_home'])
print(config['enemy_home'])
print(config['operators'])
print(config['enemies'])
