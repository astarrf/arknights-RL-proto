from pygame import draw
from attack import agent

# 继承agent类


class Operator(agent):
    def __init__(self, x, y, hp, attack, range: list[list], attack_speed, armor_p, armor_m, block_num=0, facing=0):
        self.x = x
        self.y = y
        self.block_num = block_num
        self.is_blocking = []
        self.facing = facing
        abs_range = []
        for chunk in range:
            if facing == 0:
                pos = [chunk[0] + x, chunk[1] + y]  # 向右
            elif facing == 1:
                pos = [chunk[1] + x, -chunk[0] + y]  # 向下
            elif facing == 2:
                pos = [-chunk[0] + x, -chunk[1] + y]  # 向左
            elif facing == 3:
                pos = [-chunk[1] + x, chunk[0] + y]  # 向上
            abs_range.append(pos)
        super().__init__(hp, attack, attack_speed, armor_p, armor_m, abs_range)

    def action(self, enemies):
        self.cooldown_tick()
        self.attack(self.x, self.y, enemies, self.is_blocking)

    def can_block(self, enemy, x, y):
        if len(self.is_blocking) == self.block_num:
            return False
        if (enemy.x-self.x)**2 + (enemy.y-self.y)**2 <= 0.0625:
            vec = [x-self.x, y-self.y]
            l = (vec[0]**2 + vec[1]**2)**0.5
            vec = [vec[0]/l*0.25, vec[1]/l*0.25]
            enemy.x = self.x+vec[0]
            enemy.y = self.y+vec[1]
            self.is_blocking.append(enemy)
            return True
        if round(x) == self.x and round(y) == self.y:
            self.is_blocking.append(enemy)
            return True
        return False

    def block_release(self, enemy):
        self.is_blocking.remove(enemy)

    def in_range(self, target):
        return [round(target.x), round(target.y)] in self.range

    def retreat(self):
        for enemy in self.is_blocking:
            enemy.blocked_by = None

    def draw(self, screen):
        draw.circle(screen, (0, 255, 0),
                    (self.x * 50 + 25, self.y * 50 + 25), 20)
        draw.rect(screen, (51, 153, 255), (self.x * 50 + 5,
                                           self.y * 50 + 40, self.hp/self.hp_max*30, 5))
