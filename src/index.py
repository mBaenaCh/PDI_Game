from player import Player
from ball import Ball
import pygame
import cv2
import numpy as np

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

def show_end_game_screen(text):
    screen.blit(background, [0, 0])
    draw_text(screen, text, 50, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Presione cualquier tecla para volver a jugar", 50, WIDTH // 2, (HEIGHT // 2) + 70)
    pygame.display.flip()
    restart = True
    while restart:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                restart = False

def get_position(mask, color):
    font = cv2.FONT_HERSHEY_SIMPLEX
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))  
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations = 4)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        M = cv2.moments(c)
        if (M["m00"] == 0): M["m00"] = 1
        x = int(M["m10"] / M["m00"])
        y = int(M['m01'] / M['m00'])
        new_contour = cv2.convexHull(c)
        cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
        cv2.putText(frame,f"{x}, {y}", (x + 10, y), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.drawContours(frame, [new_contour], 0, color, 3)
    return x, y

cap = cv2.VideoCapture(0)
azulBajo = np.array([100, 100, 20], np.uint8)
azulAlto = np.array([125, 255, 255], np.uint8)

redBajo1 = np.array([0, 100, 20], np.uint8)
redAlto1 = np.array([5, 255, 255], np.uint8)
redBajo2 = np.array([175, 100, 20], np.uint8)
redAlto2 = np.array([179, 255, 255], np.uint8)
  
end_game = False
end_game_message = ""
running = True

while running:
    ret, frame = cap.read()
    player_1_x = 0 
    player_1_y = 0
    player_2_x = 0 
    player_2_y = 0
    if ret == True:
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        maskAzul = cv2.inRange(frameHSV, azulBajo, azulAlto)
        maskRed1 = cv2.inRange(frameHSV, redBajo1, redAlto1)
        maskRed2 = cv2.inRange(frameHSV, redBajo2, redAlto2)
        maskRed = cv2.add(maskRed1, maskRed2)
        player_1_x, player_1_y = get_position(maskRed, (0, 0, 255)) 
        player_2_x, player_2_y = get_position(maskAzul, (255, 0, 0))
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        if key == ord('q') or key == ord('Q'):
            break

    if end_game:
        show_end_game_screen(end_game_message)
        player_1.restart_score()
        player_2.restart_score()
        end_game = False

    clock.tick(30)
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

    ball_group.update()
    player_1.update_position(player_1_x, player_1_y)
    player_2.update_position(player_2_x, player_2_y)

    hit_ball_player1 = pygame.sprite.spritecollide(player_1, ball_group, False)
    for hit in hit_ball_player1:
        ball.change_x_dir()

    hit_ball_player2 = pygame.sprite.spritecollide(player_2, ball_group, False)
    for hit in hit_ball_player2:
        ball.change_x_dir()

    if (ball.get_x_pos() < 0):
        ball.set_pos(WIDTH // 2, HEIGHT // 2)
        player_2.sum_score()
        score = player_2.get_score()
        player_1.set_pos(HEIGHT // 2)
        player_2.set_pos(HEIGHT // 2)

    if (ball.get_x_pos() > WIDTH):
        ball.set_pos(WIDTH // 2, HEIGHT // 2)
        player_1.sum_score()
        score = player_1.get_score()
        player_1.set_pos(HEIGHT // 2)
        player_2.set_pos(HEIGHT // 2)
        
    player_1_score = player_1.get_score()
    player_2_score = player_2.get_score()

    if player_1_score == 3:
        end_game = True
        end_game_message = "El jugador 1 ha ganado la partida"
    elif player_2_score == 3:
        end_game = True
        end_game_message = "El jugador 2 ha ganado la partida"

    text_1 = f"Score: {player_1_score}"
    text_2 = f"Score: {player_2_score}"
    
    screen.blit(background, [0, 0])
    all_sprites.draw(screen)

    draw_text(screen, text_1, 50, 90, 20)
    draw_text(screen, text_2, 50, WIDTH - 90, 20)

    pygame.display.update()

pygame.quit()
cap.release()
cv2.destroyAllWindows()
