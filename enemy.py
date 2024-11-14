from pygame import draw
from attack import agent
from config import *


class Enemy(agent):
    def __init__(self, hp, speed, attack, range, attack_interval, armor_p, armor_m, path):
        super().__init__(hp, attack, attack_interval, armor_p, armor_m)
        x, y = path[0]
        self.x = x  # 位置X
        self.y = y  # 位置Y
        self.speed = speed/2/TICK  # 移动速度
        self.range = range  # 攻击范围
        self.path = path  # 移动路径
        self.path_idx = 1  # 当前路径点

    def is_blocked(self, x, y):
        return round(self.x) == x and round(self.y) == y

    def in_range(self, target):
        return (target.x - self.x)**2 + (target.y - self.y)**2 <= self.range**2

    def move(self):
        x, y = self.path[self.path_idx]
        vec = [x - self.x, y - self.y]
        l = (vec[0]**2 + vec[1]**2)**0.5
        vec = [vec[0]/l, vec[1]/l]
        self.x += vec[0]*self.speed
        self.y += vec[1]*self.speed
        if l < self.speed:
            self.path_idx = self.path_idx+1 if self.path_idx < len(
                self.path) - 1 else -1

    def cooldown_tick(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def draw(self, screen):
        draw.circle(screen, (255, 0, 0),
                    (self.x * 50 + 25, self.y * 50 + 25), 15)
        # 画出敌人的生命值
        draw.rect(screen, (255, 165, 0), (self.x * 50 + 5,
                  self.y * 50 + 40, self.hp/self.hp_max*30, 5))


class group:
    def __init__(self, enemies: Enemy, num=1, interval=0):
        self.enemies = enemies
        self.remaining = num
        self.interval = interval
        self.cooldown = 0

    def cooldown_tick(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def spawn(self):
        if self.cooldown == 0 and self.remaining > 0:
            self.cooldown = self.interval
            self.remaining -= 1
            return self.enemies
        return []
