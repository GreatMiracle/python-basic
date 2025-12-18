class Enemy:
    def __init__(self, enemy_type, health_points=10, attack_damage=1):
        self.__type_of_enemy = enemy_type
        self.health_points = health_points
        self.__attack_damage = attack_damage

    # def get_type_of_enemy(self):
    #     return self.__type_of_enemy
