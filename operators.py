from pygame import draw
from attack import agent

# 继承agent类


class Operator(agent):
    def __init__(self, x, y, hp, attack, range: list[list], attack_speed, armor_p, armor_m, facing=0):
        super().__init__(hp, attack, attack_speed, armor_p, armor_m)
        self.x = x
        self.y = y
        self.facing = facing
        self.range = []
        for chunk in range:
            if facing == 0:
                pos = [chunk[0] + x, chunk[1] + y]  # 向右
            elif facing == 1:
                pos = [chunk[1] + x, -chunk[0] + y]  # 向下
            elif facing == 2:
                pos = [-chunk[0] + x, -chunk[1] + y]  # 向左
            elif facing == 3:
                pos = [-chunk[1] + x, chunk[0] + y]  # 向上
            self.range.append(pos)

    def in_range(self, target):
        return [round(target.x), round(target.y)] in self.range

    def draw(self, screen):
        draw.circle(screen, (0, 255, 0),
                    (self.x * 50 + 25, self.y * 50 + 25), 20)
        draw.rect(screen, (51, 153, 255), (self.x * 50 + 5,
                                           self.y * 50 + 40, self.hp/self.hp_max*30, 5))
