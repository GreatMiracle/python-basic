class Enemy:
    def __init__(self, type_of_enemy, health_points, attack_damage):
        self.type = type_of_enemy
        self.health = health_points
        self.attack_damage = attack_damage

    def talk(self):
        print(f"I am a {self.type}. Be prepared to fight!")

    def walk_forward(self):
        print(f"{self.type} moves closer to you")

    def attack(self):
        print(f"{self.type} attacks for {self.attack_damage} damage")