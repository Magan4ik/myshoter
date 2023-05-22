import random
import math
from settings import *

pygame.init()


class GameSprite(pygame.sprite.Sprite):
    """Основний клас-спадкоємець від Sprite. Від цього класу створена Куля, Ворог та Гравець"""

    def __init__(self, image, x, y, w, h, speed):
        super().__init__()
        """Базові властивості та зображення"""
        self.w = w
        self.h = h
        self.speed = speed
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (w, h))
        self.start_image = self.image  # Стартове зображення (завжди постійне, від нього виконується поворот)

        """Створення підпису. По замовчуванню вимкнутий прапорцем text_visible"""
        self.font = pygame.font.Font(None, 30)
        self.text = ""
        self.label = self.font.render(self.text, True, (100, 50, 50))
        self.text_visible = False

        """Отримання прямокутника від зображення"""
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        """Створення хіт-бокса. Прямокутник в 2 рази менший за стартовий (для якісної колізії)"""
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, w / 2, h / 2)

    def change_image(self, new_image):
        """Заміна зображення на нове"""
        self.image = pygame.transform.scale(pygame.image.load(new_image).convert_alpha(), (self.w, self.h))
        self.start_image = self.image

    def rotate(self, angle):
        """Поворот спрайта"""
        self.image = pygame.transform.rotate(self.start_image, angle)
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))

    def draw(self):
        """Відмальовування спрайта та підпису (за умови прапорця)"""
        win.blit(self.image, self.rect)
        if self.text_visible:
            rect = self.label.get_rect()
            win.blit(self.label, (self.rect.centerx - rect.width / 2, self.rect.centery + 50))


class Player(GameSprite):
    """Клас гравця"""

    def __init__(self, image, x, y, w, h, speed):
        super().__init__(image, x, y, w, h, speed)
        """Базові властивості"""
        self.reload = 0  # Лічільник затримки між пострілами
        self.rate = 5  # Скорострільність (мешне - швидше)
        self.max_hp = 100  # Макс. здоров'є
        self.hp = 100  # Теперешнє здоров'є
        self.text = f"Health: {self.hp}/{self.max_hp}"  # Текст для підпису

    def update(self):
        """Клас оновлення гравця. Переміщення, поворот та постріл"""
        self.hitbox.center = self.rect.center  # Переміщення хітбоксу
        self.label = self.font.render(f"Health: {self.hp}/{self.max_hp}", True, (100, 50, 50))  # Оновлення підпису

        keys = pygame.key.get_pressed()
        but = pygame.mouse.get_pressed()

        """Переміщення"""
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.centerx -= self.speed
        if keys[pygame.K_d] and self.rect.x < win_width - self.rect.width:
            self.rect.centerx += self.speed
        if keys[pygame.K_w] and self.rect.y > 0:
            self.rect.centery -= self.speed
        if keys[pygame.K_s] and self.rect.y < win_height - self.rect.height:
            self.rect.centery += self.speed

        """Постріл та затримка між ними"""
        if but[0]:
            if self.reload == 0:
                self.fire()
                self.reload += 1

        if self.reload != 0:
            self.reload += 1
        if self.reload == self.rate: self.reload = 0  # Онулення лічільнику затримки між пострілами

        """Поворот гравця до мишки"""
        pos = pygame.mouse.get_pos()
        dx = pos[0] - self.rect.centerx
        dy = self.rect.centery - pos[1]
        ang = math.degrees(math.atan2(dy, dx))

        self.rotate(ang - 90)

    def fire(self):
        """Метод пострілу в позицію мишки"""
        fire_sound.play()
        pos = pygame.mouse.get_pos()
        dx = pos[0] - self.rect.centerx
        dy = self.rect.centery - pos[1]
        ang = -math.atan2(dy, dx)

        b = Bullet(bullet_image, self.rect.centerx, self.rect.centery, 8, 18, 70, ang)  # Створення кулі
        bullets.add(b)


class Enemy(GameSprite):
    """Клас ворога"""
    def __init__(self, image, x, y, w, h, speed):
        super().__init__(image, x, y, w, h, speed)
        """Базові властивості"""
        self.max_hp = 1  # Початковий стан здоров'я
        self.hp = self.max_hp
        self.text = f"Health: {self.hp}/{self.max_hp}"  # Текст для підпису

    def spawn(self):
        """Метод переспавну ворога. Випадкова позиція. Онулення поранень. Випадкове зображення"""
        self.hp = self.max_hp
        self.change_image(random.choice(asteroid_images))  # Випадкове зображення зі списку

        """Випадкове розташування за межами єкрану"""
        place = random.randint(1, 4)

        if place == 1:
            self.rect.x = random.randint(0, win_width)
            self.rect.y = -100
        elif place == 2:
            self.rect.x = win_width + 100
            self.rect.y = random.randint(0, win_height)
        elif place == 3:
            self.rect.x = random.randint(0, win_width)
            self.rect.y = win_height + 100
        elif place == 4:
            self.rect.x = -100
            self.rect.y = random.randint(0, win_height)

    def update(self, angle):
        """Оновлення ворога. Рух під кутом до гравця"""
        self.hitbox.center = self.rect.center  # Оновлення хіт-бокса
        self.label = self.font.render(f"Health: {self.hp}/{self.max_hp}", True, (100, 50, 50))  # Оновлення підпису

        self.rotate(math.degrees(-angle) - 90)
        self.rect.x += math.cos(angle) * self.speed
        self.rect.y += math.sin(angle) * self.speed


class Bullet(GameSprite):
    """Клас кулі"""
    def __init__(self, image, x, y, w, h, speed, angle):
        super().__init__(image, x, y, w, h, speed)
        """Базова властивість. Кут руху"""
        self.angle = angle

    def update(self):
        """Оновлення кулі. Рух по прямій траекторії під кутом"""
        self.hitbox.center = self.rect.center  # Оновлення хіт-бокса
        self.rotate(math.degrees(-self.angle) - 90)  # Поворот в напрямі руху
        self.rect.x += math.cos(self.angle) * self.speed
        self.rect.y += math.sin(self.angle) * self.speed


class Button(pygame.sprite.Sprite):
    """Клас кнопки"""
    def __init__(self, x, y, w, h, color, label, callback=None):
        super().__init__()
        """callback - посилання на функцію яка викликається при натиску"""

        if callback is not None:  # Якщо не вказана функція, то ставимо базову
            self.callback = callback
        else:
            self.callback = self.cb_fun

        """Базові влстивості"""
        self.color = color
        self.w = w
        self.h = h
        self.pressed = False

        """Фон кнопки"""
        self.surface = pygame.Surface((w, h))  # Поле кнопки

        self.rect = self.surface.get_rect()  # Прямокутник кнопки
        self.rect.centerx = x
        self.rect.centery = y

        """Надпис кнопки"""
        self.text = label
        label_rect = self.text.get_rect()  # Розташовуємо надпис посередені
        label_rect.centerx = w / 2
        label_rect.centery = h / 2
        self.surface.fill(self.color)
        self.surface.blit(label, label_rect)  # Малюємо напис на полі кнопки

    def cb_fun(self):
        """Заглушка, якщо не сказали функцію виклику при створенні"""
        print(self.pressed)

    def is_press(self):
        """Перевірка на натиск, та виклик функції callback"""
        x, y = pygame.mouse.get_pos()
        bt = pygame.mouse.get_pressed()
        if self.rect.collidepoint(x, y) and bt[0] and not self.pressed:  # Прапорець pressed дозволяє натиснути лише 1 раз за натиск
            self.pressed = True
            self.callback()
        if not bt[0]:  # При відпусканні онуляємо прапоцець pressed
            self.pressed = False

    def update(self):
        """Оновлення кнопки. Лише перевірка натиску"""
        self.is_press()

    def draw(self):
        """Малювання кнопки"""
        win.blit(self.surface, (self.rect.x, self.rect.y))
