from time import monotonic

from shooter.config import LANDSCAPE_CACTUS
from shooter.config import CACTUS_ATTACK_DELAY
from shooter.config import CACTUS_SPIKE_DAMAGE
from shooter.game_object.landscape import Landscape


class Cactus(Landscape):
    """Класс кактуса"""
    def __init__(self, x, y, image=LANDSCAPE_CACTUS):
        super().__init__(x, y, image)
        self.spike_damage = CACTUS_SPIKE_DAMAGE
        self.attack_delay = CACTUS_ATTACK_DELAY
        self.last_attack_time = monotonic()

    def deal_damage(self, target):
        """Метод нанесения урона шипами. Наносит урон раз в attack_delay секунд"""
        current_attack_time = monotonic()
        if current_attack_time - self.last_attack_time >= self.attack_delay:
            target.get_damage(self.spike_damage)
            self.last_attack_time = current_attack_time
