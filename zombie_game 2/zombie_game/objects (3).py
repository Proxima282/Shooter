import random
import math
from settings import*

pg.init()

class GameSprite(pg.sprite.Sprite):
    #Основний клас-спадкоємець від Sprite. Від цього класу створена Кулю, Ворог, Гравець

    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        #Базові властивості та зображення
        self.w = w
        self.h = h
        self.speed = speed
        self.image = pg.transform.scale(pg.image.load(img).convert_alpha(), (w, h))
        self.start_image = self.image #Стартове зображення, від якого виконується поворот

        #Створення підпису. За замовчуванням вимкнутий
        self.font = pg.font.Font(None, 30)
        self.text = ""
        self.label = self.font.render(self.text, True, (100, 50, 50))
        self.text_visible = False

        #Отримання прямокутника від зображення
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        #Створення хіт-бокс. Прямокутник в 2 рази менший за стартовий
        self.hitbox = pg.Rect(self.rect.x, self.rect.y, w/2, h/2)
    
    def change_image(self, new_image):
        #Зміна зображення на нове
        self.image = pg.transform.scale(pg.image.load(new_image).convert_alpha(), (self.w, self.h))
        self.start_image = self.image #Стартове зображення, від якого виконується поворот

    def rotate(self, angle):
        #Поворт спрайта
        self.image = pg.transform.rotate(self.start_image, angle)
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
    
    def draw(self):
        #Відмалювання спрайта та підпису
        win.blit(self.image, self.rect)
        if self.text_visible:
            rect = self.label.get_rect()
            win.blit(self.label, (self.rect.centerx - rect.width /2, self.rect.centery + 50))

class Player(GameSprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__(img, x, y, w, h, speed)
        self.reload = 0 #затримка між потрілами
        self.rate = 5 #скорострільність
        self.max_hp = 100
        self.hp = 100
        self.text = f"Здоров'я: {self.hp}/{self.max_hp}"

    def update(self):
        #Переміщення, поворот та потріл гравця
        self.hitbox.center = self.rect.center
        self.label = self.font.render(f"Здоров'я: {self.hp}/{self.max_hp}", True, (100, 50, 50))

        keys = pg.key.get_pressed()
        but = pg.mouse.get_pressed()

        #Переміщення
        if keys[pg.K_a] and self.rect.x > 0:
            self.rect.centerx -= self.speed
        if keys[pg.K_d] and self.rect.x < win_width - self.rect.width:
            self.rect.centerx += self.speed
        if keys[pg.K_w] and self.rect.y > 0:
            self.rect.centery -= self.speed
        if keys[pg.K_s] and self.rect.y < win_height - self.rect.height:
            self.rect.centery += self.speed   

        #Постріл та затримка між ними
        if but[0]:
            if self.reload == 0:
                self.fire()
                self.reload += 1

        if self.reload != 0:
            self.reload +=1
        if self.reload == self.rate:
            self.reload = 0

        #Поворот гравця до мишки
        pos = pg.mouse.get_pos()
        dx = pos[0] - self.rect.centerx
        dy = self.rect.centery - pos[1]

        ang = math.degrees(math.atan2(dy, dx))

        self.rotate(ang-90)
    
    def fire(self):
        #Метод пострілу 
        fire_sound.play()
        pos = pg.mouse.get_pos()
        dx = pos[0] - self.rect.centerx
        dy = self.rect.centery - pos[1]
        ang = -math.atan2(dy, dx)

        b = Bullet(bullet_image, self.rect.centerx, self.rect.centery, 8, 18, 70, ang)
        bullets.add(b)

class Bullet(GameSprite):
    def __init__(self, img, x, y, w, h, speed, angle):
        super().__init__(img, x, y, w, h, speed)
        self.angle = angle

    def update(self):
        #Рух кулі по траєкторії під кутом
        self.hitbox.center = self.rect.center
        self.rotate(math.degrees(-self.angle)-90) #поворот кулі в напрямі руху
        self.rect.x += math.cos(self.angle) * self.speed
        self.rect.y += math.sin(self.angle) * self.speed 

class Enemy(GameSprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__(img, x, y, w, h, speed)
        self.max_hp = 1
        self.hp = self.max_hp
        self.text = f"Здоров'я: {self.hp}/{self.max_hp}"

    def spawn(self):
        self.hp = self.max_hp
        self.change_image(random.choice(zombie_images)) 
        #Випадкове розташування 
        place = random.randint(1,4)

        if place == 1:
            self.rect.x = random.randint(0, win_width)
            self.rect.y = -100
        elif place == 2:
            self.rect.x = win_width + 100
            self.rect.y = random.randint(0, win_height)
        elif place == 3:
            self.rect.x = -100
            self.rect.y = random.randint(0, win_height)
        elif place == 4:
            self.rect.x = random.randint(0, win_width)
            self.rect.y = win_height + 100
    
    def update(self, angle):
        #Оновлення руху ворогів
        self.hitbox.center = self.rect.center
        self.rotate(math.degrees(-angle)-90) #поворот ворога в напрямі руху
        self.rect.x += math.cos(angle) * self.speed
        self.rect.y += math.sin(angle) * self.speed 

class Button(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, color, label, callback=None):
        super().__init__()
        #callback - посилання на функцію як викликається при натиску

        if callback is not None:
            self.callback = callback
        else:
            self.callback = self.cb_fun

        #Базові властивості
        self.color = color
        self.w = w
        self.h = h
        self.pressed = False

        #Фон кнопки
        self.surface = pg.Surface((w, h))

        self.rect = self.surface.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        #Напис кнопки
        self.label = label
        label_rect = self.label.get_rect() 
        label_rect.centerx = w/2
        label_rect.centery = h/2
        self.surface.fill(self.color)
        self.surface.blit(label, label_rect)
    def cb_fun(self):
        print(self.pressed)

    def is_press(self):
        #Перевірка на натиск та виклик функції callback
        x, y = pg.mouse.get_pos()
        bt = pg.mouse.get_pressed()

        if self.rect.collidepoint(x, y) and bt[0] and not self.pressed:
            self.pressed = True
            self.callback()
        
        if not bt[0]:
            self.pressed = False

    def update(self):
        self.is_press()
    
    def draw(self):
        win.blit(self.surface, (self.rect.x, self.rect.y))


