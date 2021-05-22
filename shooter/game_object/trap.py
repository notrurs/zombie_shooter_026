from time import monotonic

from .landscape import Landscape


class Trap(Landscape):
    """Класс объекта ловушек"""
    def __init__(self, x, y, image, damage, attack_delay):
        super().__init__(x, y, image)
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
