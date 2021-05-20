import pygame

from game.game import Game
from game_object.entity.player import Player
from game_object.entity.bullet import Bullet
from game_object.entity.zombie import Zombie
from game_object.landscapes.stone import Stone
from game_object.landscapes.ground import Ground
from game_object.landscapes.palm import Palm
from shooter.game_object.traps.cactus import Cactus

from config import WINDOW_WIDTH
from config import WINDOW_HEIGHT
from config import WINDOW_CAPTION
from config import FRAME_RATE
from config import BACKGROUND_COLOR
from config import PLAYER_IMAGE
from config import PLAYER_SPEED
from config import PLAYER_HEALTH
from config import BULLET_IMG
from config import BULLET_SPEED
from config import BULLET_DAMAGE
from config import ZOMBIE_IMAGE
from config import ZOMBIE_SPEED
from config import ZOMBIE_AGR_RANGE
from config import ZOMBIE_HEALTH
from config import ZOMBIE_DAMAGE
from config import ZOMBIE_ATTACK_DELAY
from config import LEVEL_1


class GameLogic(Game):
    """Класс игровой логики, где связаны все объекты между собой и реализовано их взаимодействие"""
    def __init__(self):
        """
        player - объект игрока
        """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_CAPTION, BACKGROUND_COLOR, FRAME_RATE, LEVEL_1)
        self.player = None
        self.create_objects()

    def create_objects(self):
        """Метод, вызывающий все остальные методы, которые что-то создают"""
        self.create_level()

    def create_level(self):
        """
        Метод, строящий уровень, генерируя все игровые объекты в определенных (в файле с уровнем) для них
        координатах
        """
        with open(LEVEL_1) as f:
            level_objects_list = f.readlines()
        x = y = 0

        level_objects_list = list(map(lambda x: x.rstrip(), level_objects_list))

        for row in level_objects_list:
            for obj in row:
                self.landscapes.add(Ground(x, y))
                if obj == '-':
                    self.obstacles.add(Stone(x, y))
                elif obj == '+':
                    self.obstacles.add(Palm(x, y))
                elif obj == '*':
                    self.obstacles.add(Cactus(x, y))
                elif obj == 'P':
                    self.create_player(x, y)
                elif obj == 'Z':
                    self.create_enemy(x, y)
                x += 40
            y += 40
            x = 0

    def create_player(self, x, y):
        """Метод, создающий игрока"""
        self.player = Player(x, y, PLAYER_IMAGE, PLAYER_SPEED, PLAYER_HEALTH)

        # Список со всеми клавишами на клавиатуре, которые могут быть задействованы игроком
        keys = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]

        # Список со всеми событиями мышки, которые могут быть задейстованы игроком
        mouse_events = [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]

        # Добавляем все клавиши в соответствующие словари
        for key in keys:
            self.keydown_handlers[key].append(self.player.handle_keydown)
            self.keyup_handlers[key].append(self.player.handle_keyup)

        # Добавляем все события мышки в словарь
        for event in mouse_events:
            self.mouse_handlers[event].append(self.player.handle_mouse)

        # Добавляем созданного игрока в группу игровых объектов
        self.player_objects.add(self.player)

    def create_enemy(self, x, y):
        """Метод, создающий врагов"""
        zombie = Zombie(x, y, ZOMBIE_IMAGE, ZOMBIE_SPEED, ZOMBIE_AGR_RANGE, ZOMBIE_HEALTH, ZOMBIE_DAMAGE, ZOMBIE_ATTACK_DELAY)
        self.enemies.add(zombie)

    def handle_bullets(self):
        """Обработчик создания пуль"""
        if self.player.state == 'attack':
            spawn_bullet_x, spawn_bullet_y = self.player.get_barrel_pos()  # self.player.rect.center
            target_pos = pygame.mouse.get_pos()
            bullet = Bullet(spawn_bullet_x, spawn_bullet_y, BULLET_IMG, BULLET_SPEED, BULLET_DAMAGE, target_pos)
            self.player_bullets.add(bullet)

    def handle_enemies_attack(self):
        """Обработчик атак врагов"""
        for enemy in self.enemies:
            if pygame.sprite.collide_circle(enemy, self.player):
                enemy.change_state()
                enemy.attack(self.player.rect)
            else:
                enemy.attack(self.player.rect)

    def handle_enemy_with_bullet_collision(self):  # {'пуля': [враг1, враг2, ...], 'пуля2': [враг1]}
        """Обработчик соприкосновения пули с врагами"""
        collide_dict = pygame.sprite.groupcollide(self.player_bullets, self.enemies, False, False)
        for bullet, enemies in collide_dict.items():
            for enemy in enemies:
                enemy.get_damage(bullet.damage)
            bullet.kill()

    def handle_player_with_enemy_collision(self):
        """Обработчик соприкосновения игрока с врагами"""
        collide_enemy = pygame.sprite.spritecollideany(self.player, self.enemies)
        if collide_enemy:
            collide_enemy.deal_damage(self.player)

    def handle_player_with_obstacle_collision(self):
        """Обработчик соприкосновения игрока с препятствием"""
        touched_obstacles = pygame.sprite.spritecollide(self.player, self.obstacles, False)

        if not touched_obstacles:
            self.player.block_moving(None)

        for obstacle in touched_obstacles:
            if self.player.rect.collidepoint(*obstacle.rect.midleft) and self.player.moving_right:
                self.player.block_moving('right')
            elif self.player.rect.collidepoint(*obstacle.rect.midright) and self.player.moving_left:
                self.player.block_moving('left')
            elif self.player.rect.collidepoint(*obstacle.rect.midtop) and self.player.moving_down:
                self.player.block_moving('down')
            elif self.player.rect.collidepoint(*obstacle.rect.midbottom) and self.player.moving_up:
                self.player.block_moving('up')

    def handle_bullets_with_obstacles_collision(self):
        """Обработчик соприкосновения пули с препятствием"""
        pygame.sprite.groupcollide(self.player_bullets, self.obstacles, True, False)

    def handle_enemy_with_obstacle_collision(self):
        """Обработчик соприкосновения врага с препятствием"""
        touched_obstacles = pygame.sprite.groupcollide(self.enemies, self.obstacles, False, False) # {'враг': [камень1, камень2, ...], ...}

        if not touched_obstacles:
            for enemy in self.enemies:
                enemy.block_moving(None)

        for enemy, obstacles in touched_obstacles.items():
            for obstacle in obstacles:
                if enemy.rect.collidepoint(*obstacle.rect.midleft) and enemy.moving_right:
                    enemy.block_moving('right')
                elif enemy.rect.collidepoint(*obstacle.rect.midright) and enemy.moving_left:
                    enemy.block_moving('left')
                elif enemy.rect.collidepoint(*obstacle.rect.midtop) and enemy.moving_down:
                    enemy.block_moving('down')
                elif enemy.rect.collidepoint(*obstacle.rect.midbottom) and enemy.moving_up:
                    enemy.block_moving('up')

    def update(self):
        """Запускает все хендлеры (обработчики) и вызывает update родителя"""
        self.handle_bullets()
        self.handle_enemies_attack()
        self.handle_enemy_with_bullet_collision()
        self.handle_player_with_enemy_collision()
        self.handle_player_with_obstacle_collision()
        self.handle_bullets_with_obstacles_collision()
        self.handle_enemy_with_obstacle_collision()
        super().update()


# "Запускатр" игры
if __name__ == '__main__':
    GameLogic().run()
