import numpy as np
import pygame


class map:
    def __init__(self, MAP_WIDTH=5, MAP_HEIGHT=5):
        self.MAP_WIDTH = MAP_WIDTH
        self.MAP_HEIGHT = MAP_HEIGHT
        self.map_hl = np.ones((MAP_HEIGHT, MAP_WIDTH),
                              dtype=int)  # 地面高台, 1为高台，0为地面
        self.map_hl[2, :] = 0
        self.map_deploy = np.ones(
            (MAP_HEIGHT, MAP_WIDTH), dtype=int)  # 可部署, 1为可部署，0为不可部署
        self.map_mv = np.zeros((MAP_HEIGHT, MAP_WIDTH),
                               dtype=int)  # 可移动, 1为可移动，0为不可移动
        self.map_mv[2, :] = 1
        # 双方基地, 0为空，1为敌人基地, 2为干员基地, 3为其他基地
        self.map_home = np.zeros((MAP_HEIGHT, MAP_WIDTH), dtype=int)

    def set_hl(self, hl_list: list):
        # 检查hl_list和map_hl的所有维度是否相同
        if len(hl_list) != self.MAP_HEIGHT:
            print("高台列表长度错误")
            return
        for i in range(self.MAP_HEIGHT):
            if len(hl_list[i]) != self.MAP_WIDTH:
                print("高台列表长度错误")
                return
        self.map_hl = hl_list

    def set_deploy(self, deploy_list):
        if len(deploy_list) != self.MAP_HEIGHT:
            print("可部署列表长度错误")
            return
        for i in range(self.MAP_HEIGHT):
            if len(deploy_list[i]) != self.MAP_WIDTH:
                print("可部署列表长度错误")
                return
        self.map_deploy = deploy_list

    def set_mv(self, mv_list):
        if len(mv_list) != self.MAP_HEIGHT:
            print("可通过列表长度错误")
            return
        for i in range(self.MAP_HEIGHT):
            if len(mv_list[i]) != self.MAP_WIDTH:
                print("可通过列表长度错误")
                return
        self.map_mv = mv_list

    def set_doctor_home(self, home):
        x, y = home
        if x < 0 or x >= self.MAP_WIDTH or y < 0 or y >= self.MAP_HEIGHT:
            print("基地位置错误")
            return
        self.map_home[y, x] = 2

    def set_enemy_home(self, home):
        x, y = home
        if x < 0 or x >= self.MAP_WIDTH or y < 0 or y >= self.MAP_HEIGHT:
            print("基地位置错误")
            return
        self.map_home[y, x] = 1

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
