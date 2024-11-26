from pygame import draw
import numpy as np
from attack import agent
from config import *


class Enemy(agent):
    def __init__(self, hp, speed, attack, atk_range, attack_interval, atk_num, armor_p, armor_m, path, weight, able_block=True):
        super().__init__(hp, attack, attack_interval, atk_num, armor_p, armor_m)
        x, y = path[0]
        self.x = x  # 位置X
        self.y = y  # 位置Y
        self.speed = speed/2/TICK  # 移动速度
        self.path = path  # 移动路径
        self.path_idx = 1  # 当前路径点
        self.blocked_by = None
        self.weight = weight
        self.able_block = able_block
        self.path_distance = [0]*(len(path)-1)
        self.range = atk_range
        for i in range(len(path)-1):
            x1, y1 = path[i]
            x2, y2 = path[i+1]
            self.path_distance[i] = ((x2-x1)**2 + (y2-y1)**2)**0.5
        self.remaining_distance = np.sum(self.path_distance)

    def update_distance(self):
        x, y = self.path[self.path_idx]
        self.remaining_distance = (
            (self.x-x)**2+(self.y-y)**2)**0.5 + np.sum(self.path_distance[self.path_idx:])

    def search_target(self, operators):
        '''

        :param operators:输入operators实例列表
        :return: 输出可被攻击干员列表
        '''
        target_list = []
        for operator in operators:
            if self.in_range(operator):
                target_list.append(operator)
        return target_list

    def action(self, operators):
        path_idx_next, x_next, y_next = self.try_move()
        # 是否被干员挡住,返回挡住的干员,否则返回None
        block_op = self.is_blocked(operators, x_next, y_next)
        self.cooldown_tick()
        target_list = self.search_target(operators)
        self.attack(self.x, self.y, target_list, [block_op])
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
        '''

        :param target: 输入目标干员实例
        :return: 布尔值，距离是否小于索敌距离
        '''
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
        self.update_distance()

    def arrive(self):
        return self.path_idx == -1

    def cooldown_tick(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def block_release(self):
        if self.blocked_by:
            self.blocked_by.block_release(self)
            self.blocked_by = None

    def die(self):
        self.block_release()

    def clone(self):
        # 创建一个具有相同属性的新 Enemy 实例
        new_enemy = Enemy(self.hp, self.speed, self.atk, self.range, self.attack_interval,
                          self.armor_p, self.armor_m, self.path[:], self.weight, self.able_block)
        # 确保克隆的敌人从路径的起始点开始
        new_enemy.x, new_enemy.y = self.path[0]
        new_enemy.path_idx = 1
        return new_enemy

    def draw(self, screen):
        draw.circle(screen, (255, 0, 0),
                    (self.x * 50 + 25, self.y * 50 + 25), 15)
        # 画出敌人的生命值
        draw.rect(screen, (255, 165, 0), (self.x * 50 + 5,
                  self.y * 50 + 40, self.hp/self.hp_max*30, 5))


class Group:
    def __init__(self, enemies: Enemy, start_time, name=None, num=1, interval=0):
        self.enemies = enemies
        self.start_time = start_time
        self.name = name
        self.remaining = num
        self.interval = interval
        self.next_spawn_time = start_time

    def can_spawn(self, current_time):
        return self.remaining > 0 and self.next_spawn_time <= current_time

    def spawn(self):
        new_enemy = self.enemies.clone()  # Enemy 复制自身
        self.remaining -= 1
        self.next_spawn_time += self.interval
        return [new_enemy]


class Wave:
    def __init__(self, groups: list[Group], active_enemies: list[Enemy] = []):
        # groups 是一个包含多个 enemy 组的列表，每个组包含特定类型的敌人和其出现的时间和数量
        self.groups = groups
        self.active_enemies = active_enemies  # 当前活跃的敌人列表

    def spawn_update(self, current_time):
        # 遍历每个组，检查是否到了生成新敌人的时间
        for group in self.groups:
            if group.can_spawn(current_time):
                new_enemies = group.spawn()
                self.active_enemies.extend(new_enemies)

    def get_active_enemies(self):
        # 返回当前活跃的敌人列表
        return self.active_enemies

    def remove_dead_enemies(self):
        # 移除已经死亡的敌人
        for enemy in self.active_enemies[:]:
            if enemy.hp <= 0:
                enemy.die()
                self.active_enemies.remove(enemy)

    def remove_arrived_enemies(self):
        # 移除到达基地的敌人
        arrived_num = 0
        for enemy in self.active_enemies[:]:
            if enemy.arrive():
                arrived_num += 1
                enemy.die()
                self.active_enemies.remove(enemy)
        return arrived_num

    def action(self, operators):
        # 移动每个敌人
        for enemy in self.active_enemies:
            enemy.action(operators)

    def draw(self, screen):
        for enemy in self.active_enemies:
            enemy.draw(screen)
