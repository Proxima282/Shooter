import pygame as pg

pg.init()

#Характеристики вікна
win_width = 700
win_height = 500
FPS = 30

#Створення вікна
win = pg.display.set_mode((win_width, win_height))
clock = pg.time.Clock()

#Зображення
player_image = './textures/player.png'
zombie_images = ['./textures/zombie1.png', './textures/zombie2.png', './textures/zombie3.png']
bullet_image = './textures/bullet.png'

#Фонове зображення
background_image = pg.transform.scale(pg.image.load('./textures/background.png'), (win_width, win_height))

#Звуки
fire_sound = pg.mixer.Sound('./sounds/fire.ogg')
coin_sound = pg.mixer.Sound('./sounds/coin.ogg')
coins_sound = pg.mixer.Sound('./sounds/coins.ogg')
damage_sound = pg.mixer.Sound('./sounds/damage.ogg')
death_sound = pg.mixer.Sound('./sounds/death.ogg')

#Музика
pg.mixer.music.load('./sounds/music.mp3')

#Колір фону інтерфейса
background = (150, 150, 100)

#Групи для куль та ворогів
bullets = pg.sprite.Group()
zombies = pg.sprite.Group()

#Шрифт інтерфейса
ui_font = pg.font.Font(None, 50)

#Інтерфейс
UI = pg.Rect(0, win_height, win_width, 50)

