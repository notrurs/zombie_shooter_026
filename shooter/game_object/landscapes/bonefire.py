from shooter.config import LANDSCAPE_BONEFIRE
from shooter.game_object.landscape import Landscape


class Bonefire(Landscape):
    """Класс костра"""
    def __init__(self, x, y, image=LANDSCAPE_BONEFIRE):
        super().__init__(x, y, image)
