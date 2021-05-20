from time import monotonic

from shooter.config import LANDSCAPE_CACTUS
from shooter.config import CACTUS_ATTACK_DELAY
from shooter.config import CACTUS_SPIKE_DAMAGE
from shooter.game_object.trap import Trap


class Cactus(Trap):
    """Класс кактуса"""
    def __init__(self, x, y, image=LANDSCAPE_CACTUS, damage=CACTUS_SPIKE_DAMAGE, attack_delay=CACTUS_ATTACK_DELAY):
        super().__init__(x, y, image, damage, attack_delay)
