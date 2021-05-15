from math import cos, sin, radians

import pygame

from shooter.game_object.game_object import GameObject


class Player(GameObject):
    """Класс игрока"""
    def __init__(self, x, y, image, speed, health):
        """
        state - состояние игрока ("idle" - ничего не делает, "attack" - атакует)
        moving_* - булевые значения, которые сообщают, движется ли персонаж в какую-либо из сторон
        collide_* - булевые значения, которые сообщают, касается ли персонаж чего-либо какой-либо из сторон
        radius - радиус окружности, которая описывается игроком при его повороте
        health - уровень здоровья игрока
        """
        super().__init__(x, y, image, speed)
        self.state = 'idle'
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.collide_up = False
        self.collide_down = False
        self.collide_left = False
        self.collide_right = False
        self.radius = 27
        self.health = health

    def get_damage(self, damage):
        """Метод получения урона"""
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def handle_keydown(self, key):
        """Метод-обработчик нажатых клавиш"""
        if key == pygame.K_w:
            self.moving_up = True
        elif key == pygame.K_s:
            self.moving_down = True
        elif key == pygame.K_a:
            self.moving_left = True
        elif key == pygame.K_d:
            self.moving_right = True

    def handle_keyup(self, key):
        """Метод-обработчик отжатых клавиш"""
        if key == pygame.K_w:
            self.moving_up = False
        elif key == pygame.K_s:
            self.moving_down = False
        elif key == pygame.K_a:
            self.moving_left = False
        elif key == pygame.K_d:
            self.moving_right = False

    def handle_mouse(self, type, pos):
        """Метод-обработчик событий мышки"""
        if type == pygame.MOUSEMOTION:
            self.rotate(pos)
        elif type == pygame.MOUSEBUTTONDOWN:
            self.state = 'attack'
        elif type == pygame.MOUSEBUTTONUP:
            self.state = 'idle'

    def get_barrel_pos(self):
        """Метод, возвращающий положение ствола оружия"""
        x = self.rect.centerx + self.radius * cos(radians(self.angle - 16.5))
        y = self.rect.centery + self.radius * -sin(radians(self.angle - 16.5))
        return x, y

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

    def update(self):
        """Метод, отвечающий за изменение объекта (как простанственное, так и визуальное)"""
        dx = dy = 0

        if self.moving_left:
            dx = -self.speed
        if self.moving_right:
            dx = self.speed
        if self.moving_up:
            dy = -self.speed
        if self.moving_down:
            dy = self.speed

        if self.moving_left and self.collide_left:
            dx = 0
        if self.moving_right and self.collide_right:
            dx = 0
        if self.moving_up and self.collide_up:
            dy = 0
        if self.moving_down and self.collide_down:
            dy = 0

        self.move(dx, dy)
