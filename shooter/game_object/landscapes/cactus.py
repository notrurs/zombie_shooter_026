from shooter.config import LANDSCAPE_CACTUS
from shooter.game_object.landscape import Landscape


class Cactus(Landscape):
    """Класс кактуса"""
    def __init__(self, x, y, image=LANDSCAPE_CACTUS):
        super().__init__(x, y, image)
