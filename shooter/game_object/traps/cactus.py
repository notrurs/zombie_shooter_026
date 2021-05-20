from time import monotonic

from shooter.game_object.trap import Trap


class Cactus(Trap):
    """Класс кактуса"""
    def __init__(self, x, y, image, damage, attack_delay):
        super().__init__(x, y, image, damage, attack_delay)
