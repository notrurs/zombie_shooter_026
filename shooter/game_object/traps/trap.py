from time import monotonic

import pygame


class Trap(pygame.sprite.Sprite):
    """Класс объекта ловушек"""
    def __init__(self, x, y, image, damage, attack_delay):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.damage = damage
        self.attack_delay = attack_delay
        self.last_attack_time = monotonic()

    def deal_damage(self, target):
        """Метод нанесения урона. Наносит урон раз в attack_delay секунд"""
        current_attack_time = monotonic()
        if current_attack_time - self.last_attack_time >= self.attack_delay:
            target.get_damage(self.damage)
            self.last_attack_time = current_attack_time

    def blit(self, surface):
        """Отображает игровой объект"""
        surface.blit(self.image, self.rect)
