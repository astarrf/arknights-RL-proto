import numpy as np
import pygame
from operators import Operator
from enemy import Enemy
from map import map
from config import *
from .operations.a import *
# 导入/operations/01.py


class Simulator:
    def __init__(self):
        self.operators = []
        self.enemies = []
        self.base_hp = 10  # 基地生命值
        self.turn = 0  # 当前回合

    def load_map(self, map: map):
        self.map = map

    def deploy_operator(self, x, y, **kwargs):
        # 部署干员
        if self.map.map_deploy[y][x]:
            operator = Operator(x, y, **kwargs)
            self.operators.append(operator)
            print(f"部署干员在位置 ({x}, {y})")
        else:
            print(f"位置 ({x}, {y}) 不能部署干员")

    def render_init(self):
        pygame.init()  # 初始化pygame
        screen_width = MAP_WIDTH * 50
        screen_height = MAP_HEIGHT * 50+50
        screen = pygame.display.set_mode(
            (screen_width, screen_height))  # 创建屏幕对象
        pygame.display.set_caption("Arknights RL Proto")
        clock = pygame.time.Clock()  # 获取时钟对象
        return screen, clock

    def render(self, screen):
        # 渲染地图
        screen.fill((255, 255, 255))
        map.draw(screen)
        # 写出基地生命值
        font = pygame.font.Font(None, 36)
        text = font.render(f"HP: {self.base_hp}", True, (0, 0, 0))
        screen.blit(text, (10, MAP_HEIGHT * 50 + 10))
        # 画出干员
        for operator in self.operators:
            operator.draw(screen)
        # 画出敌人
        for enemy in self.enemies:
            enemy.draw(screen)

    def step(self, screen):
        # 游戏的一个时间步
        # 干员攻击
        for operator in self.operators:
            operator.cooldown_tick()
            operator.attack(self.enemies)  # 需要在attack.py中修改
            # if operator.can_attack():
            #     # 寻找范围内的敌人
            #     for enemy in self.enemies:
            #         if enemy.in_range(operator):
            #             operator.attack_enemy(enemy, 0)
            #             operator.reset_cooldown()
            #             print(
            #                 f"干员在 ({operator.x}, {operator.y}) 攻击敌人，敌人剩余HP: {enemy.hp}")
            #             break
            operator.draw(screen)

        # 移动敌人
        for enemy in self.enemies:
            enemy.cooldown_tick()
            enemy.move()
            enemy.attack(self.operators)  # 需要在attack.py中修改
            # blocked = False
            # for operator in self.operators:
            #     if enemy.is_blocked(operator.x, operator.y):
            #         blocked = True
            #         print(f"敌人被干员挡住了")
            #         if enemy.can_attack():
            #             enemy.attack_enemy(operator, 0)
            #             enemy.reset_cooldown()
            #             print(f"敌人攻击干员，干员剩余HP: {operator.hp}")
            #         break
            # if enemy.path_idx >= 0:
            #     enemy.move()
            #     print(f"敌人移动到 ({enemy.x}, {enemy.y})")
            if enemy.path_idx == -1:
                # 敌人到达基地
                self.base_hp -= 1
                self.enemies.remove(enemy)
                print(f"敌人到达基地！基地剩余HP: {self.base_hp}")

        # 清除死亡的敌人
        self.enemies = [enemy for enemy in self.enemies if enemy.hp > 0]

        # 清除死亡的干员
        self.operators = [
            operator for operator in self.operators if operator.hp > 0]

        self.render(screen)
        self.turn += 1

    def run(self, max_turns=20):
        my_map = map(MAP_WIDTH, MAP_HEIGHT)
        my_map.set_hl(map_hl)
        my_map.set_deploy(map_deploy)
        my_map.set_mv(map_mv)
        my_map.set_doctor_home(doctor_home)
        my_map.set_enemy_home(enemy_home)
        self.load_map(my_map)

        screen, clock = self.render_init()

        self.spawn_enemy()
        for _ in range(max_turns):
            events = pygame.event.get()
            print(f"\n---- 第 {self.turn} 回合 ----")
            self.step(screen)
            pygame.display.flip()  # 更新显示
            clock.tick(TICK)
            if self.base_hp <= 0:
                print("基地被摧毁，游戏结束！")
                break
            if not self.enemies and self.turn > 5:
                print("所有敌人被消灭，游戏胜利！")
                break


# 示例运行
if __name__ == "__main__":
    sim = Simulator()
    sim.deploy_operator(1, 1, hp=10, attack=3,  range=[
        [0, 0], [1, 0], [2, 0], [1, 1], [1, -1]], attack_speed=1, armor_p=0, armor_m=0, facing=2)
    sim.deploy_operator(2, 1, hp=10, attack=2,  range=[
        [0, 0], [1, 0], [2, 0], [1, 1], [1, -1]], attack_speed=1, armor_p=0, armor_m=0, facing=2)
    sim.deploy_operator(1, 2, hp=50, attack=2,  range=[
        [0, 0], [1, 0], [2, 0], [1, 1], [1, -1]], attack_speed=1, armor_p=2, armor_m=0, facing=2)
    sim.run()
