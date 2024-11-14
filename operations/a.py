# 地图类
MAP_WIDTH = 9
MAP_HEIGHT = 4
map_hl = [[0, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 0, 1, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 1, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 0]]
map_deploy = [[1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1]]
map_mv = [[0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [1, 1, 1, 1, 1],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0]]
doctor_home = (4, 2)
enemy_home = (0, 2)

# 敌人类
# 小兵
soldier = {'hp': 1650,
           'speed': 1.1,
           'attack': 200,
           'range': 0,
           'attack_interval': 2,
           'armor_p': 30,
           'armor_m': 0,
           'path': [(0, 2), (4, 2)]}

# 血狼，但其实是源石虫
blood_wolf = {'hp': 550,
              'speed': 1,
              'attack': 130,
              'range': 0,
              'attack_interval': 1.7,
              'armor_p': 0,
              'armor_m': 0,
              'path': [(0, 2), (4, 2)]}
