from player import Player
from ball import Ball
import pygame

WIDTH = 800
HEIGHT = 800
#BLACK = (0, 0, 0)
#WHITE = ( 255, 255, 255)
#GREEN = (0, 255, 0)

pygame.init()
#pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

background = pygame.image.load("assets/bg.jpg").convert()

all_sprites = pygame.sprite.Group()

player_1 = Player(10, HEIGHT // 2, "assets/player1.png")
player_2 = Player(WIDTH - 30, HEIGHT // 2, "assets/player2.png")
ball = Ball(0, 10, WIDTH // 2, HEIGHT // 2)

all_sprites.add(player_1)
all_sprites.add(player_2)
all_sprites.add(ball)

ball_group = pygame.sprite.GroupSingle()
ball_group.add(ball)

running = True
while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

    all_sprites.update()

    hit_ball_player1 = pygame.sprite.spritecollide(player_1, ball_group, False)
    for hit in hit_ball_player1:
        ball.change_x_dir()

    hit_ball_player2 = pygame.sprite.spritecollide(player_2, ball_group, False)
    for hit in hit_ball_player2:
        ball.change_x_dir()

    

    screen.blit(background, [0, 0])
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
