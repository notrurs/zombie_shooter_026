from shooter.config import LANDSCAPE_WATER
from shooter.game_object.landscape import Landscape


class Water(Landscape):
    """Класс вода"""
    def __init__(self, x, y, image=LANDSCAPE_WATER):
        super().__init__(x, y, image)