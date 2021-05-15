from math import atan2
from math import degrees
from math import cos
from math import sin

from pygame.transform import rotate

from shooter.game_object.game_object import GameObject


class Bullet(GameObject):
    """Класс пули"""
    def __init__(self, x, y, image, speed, damage, target_pos):
        """
        speed - скорость пули
        damage - урон пули
        """
        super().__init__(x, y, image, speed)
        self.speed = (speed, speed)
        self.damage = damage
        self.rotate(target_pos)

    def rotate(self, target_pos):
        """Метод, отвечающий за поворот пули и задающий вектор перемещения (dx, dy)"""
        attacker_pos = (self.rect.x, self.rect.y)
        angle = atan2(attacker_pos[1] - target_pos[1], attacker_pos[0] - target_pos[0])

        dx = -round(self.speed[0] * cos(abs(angle)))
        if attacker_pos[1] > target_pos[1]:
            dy = -round(self.speed[1] * sin(abs(angle)))
        else:
            dy = round(self.speed[1] * sin(abs(angle)))

        self.image = rotate(self.original_image,  180 - degrees(angle))
        self.rect = self.image.get_rect(center=self.rect.center)

        self.speed = (dx, dy)
