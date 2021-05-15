import pygame


class Landscape(pygame.sprite.Sprite):
    """Класс объекта окружения"""
    def __init__(self, x, y, image):
        """
        image - картинка
        rect - прямоугольник, созданный на основе картинки
        """
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def blit(self, surface):
        """Отображает игровой объект"""
        surface.blit(self.image, self.rect)
