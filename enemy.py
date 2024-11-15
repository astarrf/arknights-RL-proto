from pygame import draw
from attack import agent
from config import *


class Enemy(agent):
    def __init__(self, hp, speed, attack, range, attack_interval, armor_p, armor_m, path, able_block=True):
        super().__init__(hp, attack, attack_interval, armor_p, armor_m)
        x, y = path[0]
        self.x = x  # 位置X
        self.y = y  # 位置Y
        self.speed = speed/2/TICK  # 移动速度
        self.range = range  # 攻击范围
        self.path = path  # 移动路径
        self.path_idx = 1  # 当前路径点
        self.blocked_by = None
        self.able_block = able_block

    def action(self, operators):
        path_idx_next, x_next, y_next = self.try_move()
        # 是否被干员挡住,返回挡住的干员,否则返回None
        block_op = self.is_blocked(operators, x_next, y_next)
        self.cooldown_tick()
        self.attack(operators, block_op)
        if block_op:
            return
        self.move(path_idx_next, x_next, y_next)

    def is_blocked(self, operators, x, y):
        for operator in operators:
            if operator.can_block(self, x, y):
                self.blocked_by = operator
                return operator
        return None

    def in_range(self, target):
        return (target.x - self.x)**2 + (target.y - self.y)**2 <= self.range**2

    def try_move(self):
        x, y = self.path[self.path_idx]
        path_idx_next = self.path_idx
        vec = [x - self.x, y - self.y]
        l = (vec[0]**2 + vec[1]**2)**0.5
        vec = [vec[0]/l, vec[1]/l]
        x_next = self.x + vec[0]*self.speed
        y_next = self.y + vec[1]*self.speed
        if l < self.speed:
            path_idx_next = self.path_idx+1 if self.path_idx < len(
                self.path) - 1 else -1
        return path_idx_next, x_next, y_next

    def move(self, path_idx_next, x_next, y_next):
        self.path_idx = path_idx_next
        self.x = x_next
        self.y = y_next

    def cooldown_tick(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def block_release(self):
        if self.blocked_by:
            self.blocked_by.block_release(self)
            self.blocked_by = None

    def die(self):
        self.block_release()

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
