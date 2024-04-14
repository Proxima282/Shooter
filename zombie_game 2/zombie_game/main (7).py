from objects import*

pg.init()

pg.draw.rect(win, background, UI) #Малювання нижнього прямокутника для інтерфейсу
win.blit(background_image, (0,0)) #Малювання фону

bt_text = ui_font.render("Start", True, (100, 255, 255)) 

finish = True #Гра не почата одразу
pause = False #Прапорець паузи

level = 1 

boss_round = False

def callback():
    #Зміна всіх значень за замовчуванням. 
    global finish, player, scores, zombies, boss_round

    pg.mixer.music.play(100)

    player = Player(player_image, 350, 250, 50, 50, 5)

    scores = 0
    finish = False
    boss_round = False
    zombies.empty()

    for i in range(10):
        zombie = Enemy(random.choice(zombie_images), 100, 100, 50, 50, 2)
        zombie.spawn()
        zombies.add(zombie)

bt = Button(win_width/2, 100, 100, 50, (50, 50, 100), bt_text, callback=callback)

while True:
    #Основний цикл
    for e in pg.event.get():
        if e.type == pg.QUIT:
            exit()
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_p:
                pause = not pause
                if pause:
                    pg.mixer.music.pause()
                else:
                    pg.mixer.music.unpause()
    
    if finish:
        bt.update()
        bt.draw()
    elif not pause:
        win.blit(background_image, (0,0)) #Малювання фону

        for zombie in zombies:
            dx = zombie.rect.centerx - player.rect.centerx
            dy = zombie.rect.centery - player.rect.centery
            ang = -math.atan2(-dy, dx) - math.pi

            zombie.update(ang)
            zombie.draw()

            if player.hitbox.colliderect(zombie.hitbox):
                damage_sound.play()
                if zombie.max_hp == 15:
                    zombie.kill()
                    player.hp -= 20
                    boss_round = False
                else:
                    zombie.spawn()
                    player.hp -= 10
        for b in bullets:
            #Якщо куля занадто далеко
            if math.sqrt((b.rect.x - player.rect.x)**2 + (b.rect.y - player.rect.y)**2) > 1000:
                b.kill()
                break
        
        player.draw()
        player.update()
        
        bullets.draw(win)
        bullets.update()

    pg.display.update()
    clock.tick(FPS)
