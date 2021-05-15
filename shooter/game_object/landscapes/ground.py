from shooter.config import LANDSCAPE_GROUND
from shooter.game_object.landscape import Landscape


class Ground(Landscape):
    """Класс земли"""
    def __init__(self, x, y, image=LANDSCAPE_GROUND):
        super().__init__(x, y, image)
