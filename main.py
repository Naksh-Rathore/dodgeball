from random import randint, choice
from os import path
from time import sleep
import pygame

pygame.init()

screen_width, screen_height = 700, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dodgeball by Naksh Rathore")

playing = True
clock = pygame.time.Clock()
fps = 60
screen_background_color = (255, 179, 0)

player_width, player_height = 50, 50
player_x, player_y = 100, 100
player_vel = 15
player_image = pygame.transform.scale(pygame.image.load(path.join("images", "player.png")), (player_width, player_height))
player_rect = pygame.Rect(player_x, player_y, player_width - 30, player_height - 30)

enemies = []
enemy_vel = 5
enemy_width, enemy_height = 40, 40

game_over_sfx = pygame.mixer.Sound(path.join("sounds", "game-over.mp3"))

score = 0
font = pygame.font.SysFont("Sans Serif", 35)
text = font.render(f"Score: {score}", True, (0, 0, 0))

class Enemy:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load(path.join("images", "enemy.png")), (enemy_width, enemy_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.angle_x = choice([-1, 1]) * enemy_vel
        self.angle_y = choice([-1, 1]) * enemy_vel

    def move(self):    
        self.rect.x += self.angle_x
        self.rect.y += self.angle_y

        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.angle_x *= -1 

        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.angle_y *= -1

    def collision_check(self):
        return player_rect.colliderect(self.rect)

enemies.append(Enemy(randint(100, 300), randint(100, 300)))

def display_score(score):
    global text

    text = font.render(f"Score: {score}", True, (0, 0, 0))

def player_movement(keys_pressed):
    global player_x, player_y

    if (keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]) and player_rect.y > 15:
        player_y -= player_vel

    if (keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]) and player_rect.y < screen_height - 60:
        player_y += player_vel    

    if (keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]) and player_rect.x < screen_width - 60:
        player_x += player_vel

    if (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]) and player_rect.x > 15:
        player_x -= player_vel      

def draw_window():
    screen.fill(screen_background_color)

    player_rect.topleft = (player_x, player_y)
    screen.blit(player_image, player_rect.topleft)

    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect.topleft)

    screen.blit(text, (10, 10))    

    pygame.display.update()

while playing:
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playing = False   
                pygame.quit() 

    keys_pressed = pygame.key.get_pressed()

    for enemy in enemies:
        enemy.move()

        if enemy.collision_check():
            game_over_sfx.play()
            text = font.render(f"Final Score: {score}", True, (0, 0, 0))
            draw_window()
            sleep(2)
            playing = False
            pygame.quit()

    score += 1
    display_score(score)

    if score % 100 == 0:
        enemies.append(Enemy(randint(100, 300), randint(100, 300)))
        enemy_vel += 1

    player_movement(keys_pressed)
    draw_window()            