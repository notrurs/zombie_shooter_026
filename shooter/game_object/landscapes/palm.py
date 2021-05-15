from shooter.config import LANDSCAPE_PALM
from shooter.game_object.landscape import Landscape


class Palm(Landscape):
    """Класс пальмы"""
    def __init__(self, x, y, image=LANDSCAPE_PALM):
        super().__init__(x, y, image)
