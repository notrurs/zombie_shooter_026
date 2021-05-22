from pathlib import Path

# Настройки путей
_BASE_DIR = Path.cwd()  # D:\Program Files\Other\Coding\shooter_game\shooter
_RESOURCES_DIR = _BASE_DIR / 'resources'
_IMAGES_DIR = _RESOURCES_DIR / 'images'
_LEVELS_DIR = _RESOURCES_DIR / 'levels'

# Общие настройки
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 533
WINDOW_CAPTION = 'Zombie Shoter!'
FRAME_RATE = 60

# Настройки игры
BACKGROUND_COLOR = (0, 0, 0)

# Настройки игрока
PLAYER_IMAGE = _IMAGES_DIR / 'player_min.png'
PLAYER_SPEED = 5
PLAYER_HEALTH = 100

# Настройки пули
BULLET_IMG = _IMAGES_DIR / 'bullet.png'
BULLET_SPEED = 15
BULLET_DAMAGE = 10

# Настройки врагов
ZOMBIE_IMAGE = _IMAGES_DIR / 'zombie_min.png'
ZOMBIE_SPEED = 3
ZOMBIE_AGR_RANGE = 50
ZOMBIE_HEALTH = 2000
ZOMBIE_DAMAGE = 40
ZOMBIE_ATTACK_DELAY = 1

# Настройка объектов игрового окружения
LANDSCAPE_GROUND = _IMAGES_DIR / 'ground.png'
LANDSCAPE_WATER = _IMAGES_DIR / 'water.png'
LANDSCAPE_STONE = _IMAGES_DIR / 'stone.png'
LANDSCAPE_PALM = _IMAGES_DIR / 'palm-1.png'
LANDSCAPE_BONEFIRE = _IMAGES_DIR / 'bonefire.png'

# Настройка объектов ловушек
CACTUS_IMG = _IMAGES_DIR / 'cactus.png'
CACTUS_ATTACK_DELAY = 1
CACTUS_SPIKE_DAMAGE = 10

# Список уровней
LEVEL_1 = _LEVELS_DIR / 'level.txt'
LEVEL_2 = _LEVELS_DIR / 'level_2.txt'
