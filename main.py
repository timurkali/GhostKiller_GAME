import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((618, 359))
pygame.display.set_caption("First Game")
icon = pygame.image.load('images/bunny.png')
pygame.display.set_icon(icon)

background = pygame.image.load('images/forest.png').convert_alpha()

walk_left = [
    pygame.image.load('images/player_left/left1.png').convert_alpha(),
    pygame.image.load('images/player_left/left2.png').convert_alpha(),
    pygame.image.load('images/player_left/left3.png').convert_alpha(),
    pygame.image.load('images/player_left/left4.png').convert_alpha(),
]

walk_right = [
    pygame.image.load('images/player_right/right1.png').convert_alpha(),
    pygame.image.load('images/player_right/right2.png').convert_alpha(),
    pygame.image.load('images/player_right/right3.png').convert_alpha(),
    pygame.image.load('images/player_right/right4.png').convert_alpha(),
]

ghost = pygame.image.load('images/ghost.png').convert_alpha()
ghost_x = 620
ghost_list_in_game = []

player_anim_count = 0
background_x = 0

players_speed = 15
players_x = 150
players_y = 250

is_jump = False
jump_count = 8
runnerfit = False

bg_sound = pygame.mixer.Sound('sounds/music1.mp3')
bg_sound.play()

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

label = pygame.font.Font('fonts/static/PlayfairDisplay-Black.ttf', 40)
label1 = pygame.font.Font('fonts/static/PlayfairDisplay-Black.ttf', 20)
lose_label = label.render('YOU LOSE!', True, (193, 196, 199))
restart_label = label1.render('Начать Заново', True, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(230, 200))

bullets_left = 5
bullet = pygame.image.load('images/bullet2.png').convert_alpha()
bullets = []


gameplay = True


running = True
while running:

    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + 618, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(players_x, players_y))

        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10

                if el.x < -10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (players_x, players_y))
        else:
            screen.blit(walk_right[player_anim_count], (players_x, players_y))

        if keys[pygame.K_LEFT] and players_x > 50:
            players_x -= players_speed
        elif keys[pygame.K_RIGHT] and players_x < 400:
            players_x += players_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    players_y -= (jump_count ** 2) / 2
                else:
                    players_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        background_x -= 2
        if background_x == -618:
            background_x = 0


        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4

                if el.x > 630:
                    bullets.pop(i)

                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)


    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (200, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            players_x = 150
            ghost_list_in_game.clear()
            bullets.clear()
            bullets_left = 5


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(620, 250)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(players_x + 30, players_y + 10)))
            bullets_left -= 1



    clock.tick(15)




