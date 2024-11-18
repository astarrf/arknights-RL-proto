from config import *


class agent:
    def __init__(self, hp, attack, attack_interval, atk_num, armor_p, armor_m):
        self.hp_max = hp
        self.hp = hp
        self.attack = attack  # 攻击力
        self.attack_interval = attack_interval*TICK  # 攻击速度（每多少回合攻击一次）
        self.cooldown = 0  # 攻击冷却
        self.atk_num = atk_num
        self.armor_p = armor_p  # 物理护甲
        self.armor_m = armor_m  # 法术护甲

    def can_attack(self):
        return self.cooldown == 0

    def reset_cooldown(self):
        self.cooldown = self.attack_interval

    def cooldown_tick(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def attack_enemy(self, enemy, attack_type):
        enemy.get_hurt(self.attack, attack_type)
        self.reset_cooldown()
        # print(f"干员攻击敌人，敌人剩余HP: {enemy.hp}")

    def get_hurt(self, damage, damage_type):
        if damage_type == -1:
            self.hp -= damage  # 真伤和治疗
        if damage_type == 0:
            final_damage = damage - self.armor_p
        elif damage_type == 1:
            final_damage = damage*(100 - self.armor_m)/100
        final_damage = max(final_damage, 0.05*damage)
        self.hp -= final_damage
        # print(f"敌人攻击干员，干员剩余HP: {self.hp}")

    def attack(self, position_x, position_y, target_list, block_list, atk_type="Normal"):
        '''

        :param position_x: 导入攻击者的位置
        :param position_y: 导入攻击者的位置
        :param target_list: 导入攻击范围内实例列表
        :param block_list: 导入阻挡列表
        :param atk_type: 仇恨过滤器
        :return: 不return，直接进行攻击操作
        '''
        #基本逻辑 先打阻挡
        if self.atk_num <= len(block_list):
            atk_list = [block_list[i] for i in range(self.atk_num)]
            #从阻挡列表中获得攻击列表
        else:
            #打数大于阻挡数
            atk_list = block_list
            atk_number = self.atk_num - len(block_list)
            for item in block_list:
                try:
                    target_list.remove(item)
                except Exception:
                    print("Error raised")
            if atk_type == "Normal":
                #最正常的攻击方式 索敌距离基地最近的单位
                distance_tem = []
                for enemy in target_list:
                    distance_tem.append(enemy.update_distance())
                #存储目标的距离
                dist_max = max(distance_tem)
                index_list = []
                for i in range(atk_number):
                    min_value = min(distance_tem)
                    min_index = distance_tem.index(min_value)
                    index_list.append(min_index)
                    distance_tem[min_index] = dist_max + 1
                atk_list = atk_list + [target_list[i] for i in index_list]
                #拼接列表
            elif atk_type == "HP down":
                #低血量索敌
                HP_tem = []
                for enemy in target_list:
                    HP_tem.append(enemy.hp)
                #存储目标的距离
                HP_max = max(HP_tem)
                index_list = []
                for i in range(atk_number):
                    min_value = min(HP_tem)
                    min_index = HP_tem.index(min_value)
                    index_list.append(min_index)
                    HP_tem[min_index] = HP_max + 1
                atk_list = atk_list + [target_list[i] for i in index_list]








