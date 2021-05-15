from math import sin
from math import cos
from math import atan2
from math import degrees
from time import monotonic

from pygame.transform import rotate

from shooter.game_object.game_object import GameObject


class Zombie(GameObject):
    """Класс зомби, который умеет нападать на игрока и преследовать его бесконечно"""
    def __init__(self, x, y, image, speed, agr_range, health, damage, attack_delay):
        """
        speed - текущая скорость зомби
        const_speed - константная скорость
        state - текущее состояние зомби
        radius - радиус, в котором зомби заметит игрока
        health - уровень здоровья зомби
        damage - урон зомби
        attack_delay - задержка атаки в секундах перед следующей
        last_attack_time - время последней атаки
        moving_* - булевые значения, которые сообщают, движется ли зомби в какую-либо из сторон
        collide_* - булевые значения, которые сообщают, касается ли зомби чего-либо какой-либо из сторон
        angle - угол поворота зомби
        """
        super().__init__(x, y, image, speed)
        self.speed = (0, 0)
        self.const_speed = speed
        self.state = 'idle'
        self.radius = agr_range
        self.health = health
        self.damage = damage
        self.attack_delay = attack_delay
        self.last_attack_time = monotonic()
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.collide_up = False
        self.collide_down = False
        self.collide_left = False
        self.collide_right = False
        self.angle = 0

    def set_moving(self):
        """Метод, вычисляющий направление движения"""
        if 10 <= self.angle < 80:
            self.moving_up = True
            self.moving_left = True
            self.moving_right = False
            self.moving_down = False
        elif 80 <= self.angle < 100:
            self.moving_up = True
            self.moving_left = False
            self.moving_right = False
            self.moving_down = False
        elif 100 <= self.angle < 170:
            self.moving_up = True
            self.moving_left = False
            self.moving_right = True
            self.moving_down = False
        elif 170 <= self.angle < 190:
            self.moving_up = False
            self.moving_left = False
            self.moving_right = True
            self.moving_down = False
        elif 190 <= self.angle < 260:
            self.moving_up = False
            self.moving_left = False
            self.moving_right = True
            self.moving_down = True
        elif 260 <= self.angle < 280:
            self.moving_up = False
            self.moving_left = False
            self.moving_right = False
            self.moving_down = True
        elif 280 <= self.angle < 350:
            self.moving_up = False
            self.moving_left = True
            self.moving_right = False
            self.moving_down = True
        else:
            self.moving_up = False
            self.moving_left = True
            self.moving_right = False
            self.moving_down = False

    def block_moving(self, side):
        """Метод, блокирующий движение в какую-либо из сторон"""
        if side == 'left':
            self.collide_left = True
        elif side == 'right':
            self.collide_right = True
        elif side == 'up':
            self.collide_up = True
        elif side == 'down':
            self.collide_down = True
        else:
            self.collide_left = self.collide_right = self.collide_up = self.collide_down = False

    def get_damage(self, damage):
        """Метод получения урона"""
        self.health -= damage

        if self.state == 'idle':
            self.change_state()

        if self.health <= 0:
            self.kill()

    def deal_damage(self, target):
        """Метод нанесения урона. Наносит урон раз в attack_delay секунд"""
        current_attack_time = monotonic()
        if current_attack_time - self.last_attack_time >= self.attack_delay:
            target.get_damage(self.damage)
            self.last_attack_time = current_attack_time

    def rotate(self, target):
        """Метод, отвечающий за поворот зомби и дельты его скоростей по каждой оси"""
        if self.state == 'attack':
            angle = atan2(target[1] - self.rect.y, target[0] - self.rect.x)

            dx = round(self.const_speed * cos(abs(angle)))
            if self.rect.y > target[1]:
                dy = -round(self.const_speed * sin(abs(angle)))
            else:
                dy = round(self.const_speed * sin(abs(angle)))

            angle = degrees(angle)
            self.angle = angle + 180
            self.image = rotate(self.original_image, -angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.speed = (dx, dy)

    def attack(self, target):
        """Отвечает за атаку зомби"""
        if self.state == 'attack':
            self.rotate(target)

    def change_state(self):
        """Меняет состоние зомби на атакующее"""
        if self.state == 'idle':
            self.state = 'attack'

    def update(self):
        """Передвигает зомби в зависимости от его состояния"""
        if self.state == 'attack':
            self.set_moving()

            dx, dy = self.speed

            if self.moving_left and self.collide_left:
                dx = 0
            if self.moving_right and self.collide_right:
                dx = 0
            if self.moving_up and self.collide_up:
                dy = 0
            if self.moving_down and self.collide_down:
                dy = 0

            self.move(dx, dy)
        elif self.state == 'idle':
            self.move(0, 0)
