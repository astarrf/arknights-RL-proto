from config import *


class agent:
    def __init__(self, hp, attack, attack_interval, armor_p, armor_m):
        self.hp_max = hp
        self.hp = hp
        self.attack = attack  # 攻击力
        self.attack_interval = attack_interval*TICK  # 攻击速度（每多少回合攻击一次）
        self.cooldown = 0  # 攻击冷却
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
