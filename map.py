import numpy as np
import pygame


class Map:
    def __init__(self, MAP_WIDTH=5, MAP_HEIGHT=5, map_hl=None, map_deploy=None, map_mv=None, map_home=None):
        self.MAP_WIDTH = MAP_WIDTH
        self.MAP_HEIGHT = MAP_HEIGHT
        self.map_hl = map_hl  # 地面高台, 1为高台，0为地面
        self.map_deploy = map_deploy  # 可部署, 1为可部署，0为不可部署
        self.map_mv = map_mv  # 可移动, 1为可移动，0为不可移动
        # 双方基地, 0为空，1为敌人基地, 2为干员基地, 3为其他基地
        self.map_home = map_home

    def show(self):
        print(self.map_hl)
        print(self.map_deploy)
        print(self.map_mv)
        print(self.map_home)

    def draw(self, screen):
        for y in range(self.MAP_HEIGHT):
            for x in range(self.MAP_WIDTH):
                if self.map_home[y][x] == 1:
                    pygame.draw.rect(screen, (150, 0, 0),
                                     (x * 50, y * 50, 50, 50))  # 画出敌人基地
                    continue
                elif self.map_home[y][x] == 2:
                    pygame.draw.rect(screen, (0, 0, 125),
                                     (x * 50, y * 50, 50, 50))  # 画出干员基地
                    continue
                if self.map_hl[y][x]:
                    pygame.draw.rect(screen, (192, 192, 192),
                                     (x * 50, y * 50, 50, 50))  # 画出高台
                else:
                    pygame.draw.rect(screen, (128, 128, 128),
                                     (x * 50, y * 50, 50, 50))  # 画出地面
