import json
import numpy as np
from enemy import *
from operator import *
from map import *
from config import *


def load_map_from_json(filepath) -> Map:
    # 加载 JSON 文件
    with open(filepath, 'r') as file:
        data = json.load(file)

    map_data = data['maps']

    # 创建 Map 实例
    width = map_data['MAP_WIDTH']
    height = map_data['MAP_HEIGHT']
    map_hl = np.array(map_data['map_hl'], dtype=int)
    map_deploy = np.array(map_data['map_deploy'], dtype=int)
    map_mv = np.array(map_data['map_mv'], dtype=int)
    map_home = np.array(map_data['map_home'], dtype=int)
    # 检测地图数据是否合法
    if map_hl.shape != (height, width):
        raise ValueError('地图数据不合法')
    if map_deploy.shape != (height, width):
        raise ValueError('地图数据不合法')
    if map_mv.shape != (height, width):
        raise ValueError('地图数据不合法')
    if map_home.shape != (height, width):
        raise ValueError('地图数据不合法')
    map = Map(
        MAP_WIDTH=width,
        MAP_HEIGHT=height,
        map_hl=map_hl,
        map_deploy=map_deploy,
        map_mv=map_mv,
        map_home=map_home
    )

    return map


def load_waves_from_json(filepath) -> Wave:
    # 加载 JSON 文件
    with open(filepath, 'r') as file:
        data = json.load(file)

    waves_data = data['waves']
    groups = []

    for wave_data in waves_data:
        enemy_data = wave_data['enemy']
        # 创建 Enemy 实例
        enemy_template = Enemy(
            hp=enemy_data['hp'],
            speed=enemy_data['speed'],
            attack=enemy_data['attack'],
            atk_range=enemy_data['atk_range'],
            attack_interval=enemy_data['attack_interval'],
            atk_num=enemy_data['atk_num'],
            armor_p=enemy_data['armor_p'],
            armor_m=enemy_data['armor_m'],
            path=enemy_data['path'],
            weight=enemy_data['weight'],
            able_block=enemy_data['able_block']
        )
        # 创建 Group 实例
        group = Group(
            enemy_template=enemy_template,
            start_time=wave_data['start_time'],
            name=wave_data['name'],
            interval=wave_data['interval'],
            count=wave_data['count']
        )
        groups.append(group)

    # 创建并返回 Wave 实例
    return Wave(groups)
