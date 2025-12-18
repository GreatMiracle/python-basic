from enemy import *

zombie = Enemy("zombie", health_points=50, attack_damage=1)

zombie.talk()         # Chỉ cần gọi .talk() → không cần biết bên trong print gì
zombie.walk_forward()
zombie.attack()