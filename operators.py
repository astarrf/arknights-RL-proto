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
        super().__init__(hp, attack, attack_speed, armor_p, armor_m)

    def search_target(self, enemies):
        '''

        :param enemies:输入所有敌方实例列表
        :return: 在索敌范围内敌方列表
        '''
        target_list = []
        for enemy in enemies:
            if self.in_range(enemy):
                target_list.append(enemy)
        return target_list

    def action(self, enemies):
        self.cooldown_tick()
        target_list = self.search_target(enemies)
        self.attack(self.x, self.y, target_list, self.is_blocking)

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
        '''

        :param target:输入目标实例
        :return: 输出布尔值，目标实例的x，y坐标是否在攻击范围以内
        '''
        return [round(target.x), round(target.y)] in self.range

    def retreat(self):
        for enemy in self.is_blocking:
            enemy.blocked_by = None

    def draw(self, screen):
        draw.circle(screen, (0, 255, 0),
                    (self.x * 50 + 25, self.y * 50 + 25), 20)
        draw.rect(screen, (51, 153, 255), (self.x * 50 + 5,
                                           self.y * 50 + 40, self.hp/self.hp_max*30, 5))


class OperatorGroup:
    def __init__(self, operator: list[Operator] = []):
        self.operators = operator

    def add_operator(self, operator: Operator):
        self.operators.append(operator)

    def retreat_operator(self, operator: Operator):
        operator.retreat()
        self.operators.remove(operator)

    def remove_dead_operators(self):
        for operator in self.operators:
            if operator.hp <= 0:
                self.retreat_operator(operator)

    def action(self, enemies):
        for operator in self.operators:
            operator.action(enemies)

    def draw(self, screen):
        for operator in self.operators:
            operator.draw(screen)

    def __len__(self):
        return len(self.operators)
