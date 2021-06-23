import pygame
import os
import sys
import random

#----------------------Creating exe
dirpath = os.getcwd()
sys.path.append(dirpath)
if getattr(sys, "frozen", False):
    os.chdir(sys.MEIPASS)

#----------------------self-explained

player_lives = 5
score = 0
enemies = ['001', '002', '003', '004', 'bomb']

#----------------------Inicialize pygame and create window
WIDTH = 890
HEIGHT = 680
FPS = 24
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Secret Samurai')
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#----------------------Sound Settings

pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.load('data/intro.mp3')
pygame.mixer.music.play()
pygame.mixer.fadeout(1)
pygame.mixer.pause()



#----------------------Define color
WHITE = (255,255,255)
BLACK = (0,0,0,)
RED = (255,0,0)
YELLOW = (254,254,51)
GREEN = (30, 207, 107)

#----------------------Background
background = pygame.image.load('data/back.jpg')
background2 = pygame.image.load('data/game_over.png')
font = pygame.font.Font(os.path.join(os.getcwd(),'data/Beyond Wonderland.ttf'), 92)#####################
score_text = font.render('Score: ' + str(score), True,(YELLOW))
lives_icon = pygame.image.load('data/white_lives.png')

#----------------------Generalized structure of the enemies list
def generate_random_enemies(enemies):
    enemies_path = "data/" + enemies + ".png"
    data[enemies] = {
        'img': pygame.image.load(enemies_path),
        'x' : random.randint(100, 500),
        'y' : 800,
        'speed_x': random.randint(-10, 10),
        'speed_y': random.randint(-80, -20),
        'throw': False,
        't': 0,
        'hit': False,

    }

# ----------------------Return the next random floating point number in the range [0.0, 1.0)

    if random.random() >= 0.75:
        data[enemies]['throw'] = True
    else:
        data[enemies]['throw'] = False

# ----------------------Dictionary to hold the data the random enemy generation

data = {}
for enemy in enemies:
    generate_random_enemies(enemy)

def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("data/red_lives.png"), (x, y))

# ----------------------Draw fonts on the screen

font_name = pygame.font.match_font('data/Beyond Wonderland.ttf')
def draw_text(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, YELLOW)####################################
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)



# ----------------------draw players lives

def draw_lives(display, x, y, lives, image) :
    for i in range(lives) :
        img = pygame.image.load(image)
        img_rect = img.get_rect()       #gets the (x, y) coordinates of the cross icons
        img_rect.x = int(x + 35 * i)    #sets the next cross icon 35 pixels awt
        img_rect.y = y                  #takes care of how many pixels the cross icon should be positioned from the top
        display.blit(img, img_rect)

# ----------------------Show game over display & front display

def show_gameover_screen():
    gameDisplay.blit(background, (0, 0))
    draw_text(gameDisplay, "Secret", 119, 180, HEIGHT / 5)
    draw_text(gameDisplay, "Samurai", 119, 320, HEIGHT / 3)

    if not game_over :
        draw_text(gameDisplay,"Score : " + str(score), 90, WIDTH / 2, HEIGHT / 4)

    draw_text (gameDisplay, "Aperte qualquer tecla para iniciar :)", 50, 670, 610)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# ----------------------Game Loop

first_round = True
game_over = True        #terminates the game While loop if more than 5 Bombs are cut
game_running = True     #used to manage the game loop
while game_running:
    if game_over:
        if first_round:
            show_gameover_screen()
            pygame.mixer.music.load('data/themeloop.mp3')
            pygame.mixer.music.play()
            first_round = False
        game_over = False
        player_lives = 5
        draw_lives(gameDisplay, 570, 5, player_lives, 'data/red_lives.png')
        score = 0

    for event in pygame.event.get():

        # ----------------------checking for closing window
        if event.type == pygame.QUIT:
            game_running = False

    gameDisplay.blit(background, (0, 0))
    gameDisplay.blit(score_text, (0, 0))
    draw_lives(gameDisplay, 690, 5, player_lives, 'data/red_lives.png')

    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']  # moving the enemies in x-coordinates
            value['y'] += value['speed_y']  # moving the enemiess in y-coordinate
            value['speed_y'] += (1 * value['t'])  # increasing y-corrdinate
            value['t'] += 0.1  # increasing speed_y for next loop

            if value['y'] <= 800:
                gameDisplay.blit(value['img'],
                                 (value['x'], value['y']))  # displaying the enemy inside screen dynamically
            else:
                generate_random_enemies(key)

            current_position = pygame.mouse.get_pos()  # gets the current coordinate (x, y) in pixels of the mouse

            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x'] + 60 \
                    and current_position[1] > value['y'] and current_position[1] < value['y'] + 60:
                if key == 'bomb':
                    player_lives -= 1
                    if player_lives == 0:

                        hide_cross_lives(690, 15)
                    elif player_lives == 1:
                        hide_cross_lives(725, 15)
                    elif player_lives == 2:
                        hide_cross_lives(760, 15)

# ----------------------if the user clicks bombs for five time, GAME OVER message should be displayed and the window should be reset
                    if player_lives < 0:
                        show_gameover_screen()
                        game_over = True


                    half_enemy_path = "data/explosion.png"
                else:
                    half_enemy_path = "data/half_" + key + ".png"

                value['img'] = pygame.image.load(half_enemy_path)
                value['speed_x'] += 10
                if key != 'bomb':
                    score += 100
                score_text = font.render('Score : ' + str(score), True, (255, 255, 51))
                value['hit'] = True
        else:
            generate_random_enemies(key)

    pygame.display.update()
    clock.tick(FPS)  # keep loop running at the right speed (manages the frame/second. The loop should update afer every 1/12th pf the sec

pygame.quit()
