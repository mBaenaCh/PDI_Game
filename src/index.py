from player import Player
from ball import Ball
import pygame

WIDTH = 800
HEIGHT = 800
#BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
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

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("arial", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

running = True
while running:
    clock.tick(120)
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

    if (ball.get_x_pos() < 0):
        ball.set_pos(WIDTH // 2, HEIGHT // 2)
        player_2.sum_score()

    if (ball.get_x_pos() > WIDTH):
        ball.set_pos(WIDTH // 2, HEIGHT // 2)
        player_1.sum_score()

    player_1_score = player_1.get_score()
    player_2_score = player_2.get_score()

    text_1 = f"Score: {player_1_score}"
    text_2 = f"Score: {player_2_score}"
    
    screen.blit(background, [0, 0])
    all_sprites.draw(screen)

    draw_text(screen, text_1, 50, 90, 20)
    draw_text(screen, text_2, 50, WIDTH - 90, 20)

    pygame.display.update()

pygame.quit()
