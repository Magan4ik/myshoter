import pygame

pygame.init()

"""Характеристики вікна"""
win_width = 700
win_height = 500
FPS = 20

"""Створення вікна"""
win = pygame.display.set_mode((win_width, win_height + 50))
clock = pygame.time.Clock()

"""Зображення"""
rocket_image = 'textures\player.png'

asteroid_images = ['textures\zombie1.png', 'textures\zombie2.png', 'textures\zombie3.png']

bullet_image = 'textures\\bullet.png'

"""Фонове зображення"""
background_image = pygame.transform.scale(pygame.image.load('textures\\background.png'), (win_width, win_height))
main_screen_image = pygame.transform.scale(pygame.image.load('textures\\main_screen.png'), (win_width, win_height))

"""Звуки"""
fire_sound = pygame.mixer.Sound('sounds\\fire.ogg')
coin_sound = pygame.mixer.Sound('sounds\\coin.ogg')
coins_sound = pygame.mixer.Sound('sounds\\coins.ogg')
damage_sound = pygame.mixer.Sound('sounds\\damage.ogg')
death_sound = pygame.mixer.Sound('sounds\\death.ogg')
levelup_sounds = pygame.mixer.Sound('sounds\\levelup.ogg')

"""Фонова музика"""
pygame.mixer.music.load('Sounds\\music.mp3')

"""Колір фону або колір прямокутника інтерфейса"""
background = (150, 150, 100)

"""Групи"""
bullets = pygame.sprite.Group()
enemys = pygame.sprite.Group()
menu_buttons = pygame.sprite.Group()

"""Шрифт інтерфейсу"""
ui_font = pygame.font.Font(None, 50)

"""Прямокутник інтерфейса"""
UI = pygame.Rect(0, win_height, win_width, 50)
