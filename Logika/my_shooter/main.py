from objects import *
import database as db  # Імпорт бази данних

pygame.init()

pygame.draw.rect(win, background, UI)  # Малювання нижнього прямокутника для інтерфейсу
win.blit(main_screen_image, (0, 0))  # Малювання фону

bt_start_text = ui_font.render("Start", True, (100, 255, 255))  # Текст кнопки
bt_shop_text = ui_font.render("Shop", True, (100, 255, 255))  # Текст кнопки
bt_exit_to_menu_text = ui_font.render("Exit to menu", True, (100, 255, 255))  # Текст кнопки


finish = True  # Гра не почата одразу
pause = False  # Прапорець паузи

def callback_start():  # Функція яка викликається при натиску на кнопку Start
    """Зміна всіх значень до "по замовчуванню". Початкове налаштування гри"""
    global finish, player, scores, enemys, boss_round, game

    player = Player(rocket_image, 350, 250, 50, 50, 5)  # Гравець

    pygame.mixer.music.play(100)  # Ввімкнути фонову музику
    scores = 0  # Рахунок (монети)
    enemys.empty()  # Онулення списку ворогів

    finish = False
    boss_round = False
    game = True

    for i in range(15):  # Створення ворогів
        enemy = Enemy(random.choice(asteroid_images), 100, 100, 50, 50, 2)
        enemy.spawn()
        enemys.add(enemy)

def callback_shop():
    global shop, finish, balance, game
    shop = True
    finish = False
    game = False
    balance = db.get_balance()

def callback_to_menu():
    global shop, finish, balance, game
    pygame.draw.rect(win, background, UI)
    win.blit(main_screen_image, (0, 0))  # Малювання фону
    shop = False
    finish = True
    game = False


bt_start = Button(win_width / 2, 100, 100, 50, (50, 50, 100), bt_start_text, callback=callback_start)  # Кнопка Start
bt_shop = Button(win_width / 2, 170, 100, 50, (50, 50, 100), bt_shop_text, callback=callback_shop)  # Кнопка Start

menu_buttons.add(*(bt_start, bt_shop))

bt_exit_to_menu = Button(130, win_height, 220, 50, (50, 50, 100), bt_exit_to_menu_text, callback=callback_to_menu)

boss_round = False  # Предіод коли на єкрані є міні-бос
level = 1  # Лічільник складності
game = False
shop = False

while True:
    """Основний цикл"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                """Натиск паузи"""
                pause = not pause
                if pause:  # Призупинка та продовження музики
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

    if finish:
        for button in menu_buttons:  # Оновлення кнопок, якщо гра не почата
            button.update()
            button.draw()

    elif not pause and game:  # Якщо гра почата та не в паузі
        win.blit(background_image, (0, 0))  # Фон

        for enemy in enemys:  # оновлення ворогів
            '''Вирахування кута ворога до гравця'''
            dx = enemy.rect.centerx - player.rect.centerx
            dy = enemy.rect.centery - player.rect.centery
            ang = -math.atan2(-dy, dx) - math.pi

            enemy.update(ang)  # рух ворога за кутом
            enemy.draw()

            if player.hitbox.colliderect(enemy.hitbox):  # Зіткнення з гравцем за хітбоксами
                damage_sound.play()
                if enemy.max_hp == 15:  # Якщо це міні-бос (у нього більше хп)
                    enemy.kill()
                    player.hp -= 20
                    boss_round = False  # Закінчення бос раунду (для того щоб одночасно був лише 1 міні-бос)
                else:
                    enemy.spawn()
                    player.hp -= 10

        '''Оновлення куль'''
        for b in bullets:
            b.update()
            if math.sqrt((b.rect.x - player.rect.x) ** 2 + (b.rect.y - player.rect.y) ** 2) > 1000:  # Якщо куля занадто далеко - видаляємо
                b.kill()
                break
            b.draw()

        '''Перевірка коллізії куль та ворогів'''
        collide = pygame.sprite.groupcollide(bullets, enemys, True, False)  # словник колізій груп (кулі вбиваємо)

        if collide:  # Якщо не порожній (є колізія з кимось)
            enemy = list(collide.values())[0][0]  # Дістаємо ворога до якого доторкнулась куля
            enemy.hp -= 1  # Знімаємо хп ворогу
            if enemy.hp == 0:  # Якщо вбили ворога
                if enemy.max_hp == 15:  # Якщо це міні-бос
                    coins_sound.play()
                    enemy.kill()
                    boss_round = False  # Закінчення бос раунду (для того щоб одночасно був лише 1 міні-бос)
                    scores += 10
                else:  # Інакше це звичайний ворог
                    coin_sound.play()
                    enemy.spawn()
                    scores += 1

        '''міні-бос кожні 15 балів. Створення міні-боса'''
        if scores % 15 == 0 and scores != 0 and not boss_round:
            boss = Enemy(random.choice(asteroid_images), -100, -200, 120, 120, 2)
            boss.max_hp = 15  # Встановлюємо міні-босу більше хп
            boss.spawn()
            enemys.add(boss)
            boss_round = True  # Вмикаємо бос раунд (для того щоб одночасно був лише 1 міні-бос)

        elif scores % 30 == 0 and scores != 0:
            """Ускладнення гри (підняття рівня). Кожні 30 балів"""
            scores += 1  # Додання 1 бала, для того щоб умова не спрацьовувала декілька раз (винагорода за рівень)
            level += 1  # Підвищення рівня
            levelup_sounds.play()
            if level >= 4:
                enemy = Enemy(random.choice(asteroid_images), 100, 100, 50, 50, 2)
                enemy.spawn()
                enemys.add(enemy)
            for enemy in enemys:  # Ускладнення кожного ворога
                if enemy.max_hp != 15:  # Додаємо +1 до макс здоров'я всім окрім міні-боса
                    enemy.max_hp += 1
                if level in [6, 9]:  # На 6му рівні підвищуємо швидкість
                    enemy.speed += 1

        pygame.draw.rect(win, background, UI)  # Малювання прямокутника інтерфейса (знизу)

        scores_text = ui_font.render(f"Coins: {scores}", True, (150, 200, 50))  # Відображання рахунку
        win.blit(scores_text, (win_width - 180, win_height + 5))

        health = ui_font.render(f"HP: {player.hp}", True, (255, 50, 50))  # Відображання здоров'я
        win.blit(health, (0, win_height + 5))

        player.update()  # Оновлення гравця
        player.draw()

        '''Поразка'''
        if player.hp <= 0:
            finish = True
            lose_text = ui_font.render("You died...", True, (255, 50, 50))
            win.blit(lose_text, (250, win_height + 5))
            pygame.mixer.music.stop()
            death_sound.play()

            '''Запис та вивід рекорду'''
            db.add_result(scores)  # Додавання результату в таблицю
            record_text = ui_font.render(f"The best result: {db.get_record()}", True, (100, 100, 255))  # Вивід найкращего результату за всі ігри

            record_rect = record_text.get_rect(center=(win_width / 2, win_height - 50))  # Розташевання надпису посередні

            win.blit(record_text, record_rect)

            db.update_balance(scores)  # Оновлення балансу
        else:
            """Текст поразки відображається ні місці тексту рівня.
            Тому малюємо рівень, тільки коли ще не програли"""
            level_text = ui_font.render(f"Level: {level}", True, (200, 200, 200))
            win.blit(level_text, (280, win_height + 5))

    elif pause:  # Якщо ми на паузі
        pygame.draw.rect(win, background, UI)  # замальовуємо інтерфейс (очищаємо)
        pause_text = ui_font.render("Pause", True, (200, 200, 200))
        win.blit(pause_text, (290, win_height + 5))

    elif shop:
        win.fill(background)
        bt_exit_to_menu.draw()
        bt_exit_to_menu.update()


    pygame.display.update()
    clock.tick(FPS)
