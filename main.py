import numpy as np
import pygame
from operators import *
from enemy import *
from map import *
from config import *
from utils import *


class Simulator:
    def __init__(self, config_path):
        self.map = load_map_from_json(f'{config_path}/maps.json')
        self.waves = load_waves_from_json(f'{config_path}/waves.json')
        self.operators = OperatorGroup()
        self.base_hp = 10  # 基地生命值
        self.turn = 0  # 当前回合

    def render_init(self):
        pygame.init()  # 初始化pygame
        screen_width = self.map.MAP_WIDTH * 50
        screen_height = self.map.MAP_HEIGHT * 50+50
        screen = pygame.display.set_mode(
            (screen_width, screen_height))  # 创建屏幕对象
        pygame.display.set_caption("Arknights RL Proto")
        clock = pygame.time.Clock()  # 获取时钟对象
        return screen, clock

    def render(self, screen: pygame.Surface):
        # 渲染地图
        screen.fill((255, 255, 255))
        Map.draw(screen)
        # 写出基地生命值
        font = pygame.font.Font(None, 36)
        text = font.render(f"HP: {self.base_hp}", True, (0, 0, 0))
        screen.blit(text, (10, self.map.MAP_HEIGHT * 50 + 10))
        # 画出干员
        self.operators.draw(screen)
        # 画出敌人
        self.waves.draw(screen)

    def step(self, screen, action):
        # 游戏的一个时间步
        # 生成敌人
        self.waves.spawn_update(self.turn)

        # 部署干员
        # 用action来控制干员的部署位置

        # 干员攻击
        self.operators.action(self.waves.get_active_enemies())
        self.waves.remove_dead_enemies()
        # 敌人攻击
        self.waves.action(self.operators)
        self.operators.remove_dead_operators()

        # 敌人到达基地
        arrived_num = self.waves.remove_arrived_enemies()
        self.base_hp -= arrived_num
        print(f"敌人到达基地！基地剩余HP: {self.base_hp}")

        self.render(screen)
        self.turn += 1

    def run(self, max_turns=20):

        screen, clock = self.render_init()

        for _ in range(max_turns):
            events = pygame.event.get()
            print(f"\n---- 第 {self.turn} 回合 ----")
            self.step(screen)
            pygame.display.flip()  # 更新显示
            clock.tick(TICK)
            if self.base_hp <= 0:
                print("基地被摧毁，游戏结束！")
                break
            if self.waves.get_active_enemies() and self.turn > 5:
                print("所有敌人被消灭，游戏胜利！")
                break


# 示例运行
if __name__ == "__main__":
    # 从./operation/01.json中导入operation_config
    config_path = "./arknights-RL-proto/operations/0-1"
    sim = Simulator(config_path)
    # sim.deploy_operator(1, 1, hp=10, attack=3,  range=[
    #     [0, 0], [1, 0], [2, 0], [1, 1], [1, -1]], attack_speed=1, armor_p=0, armor_m=0, facing=2)
    # sim.deploy_operator(2, 1, hp=10, attack=2,  range=[
    #     [0, 0], [1, 0], [2, 0], [1, 1], [1, -1]], attack_speed=1, armor_p=0, armor_m=0, facing=2)
    # sim.deploy_operator(1, 2, hp=50, attack=2,  range=[
    #     [0, 0], [1, 0], [2, 0], [1, 1], [1, -1]], attack_speed=1, armor_p=2, armor_m=0, facing=2)
    # sim.run()
