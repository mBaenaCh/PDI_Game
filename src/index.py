#-----------------------------------------------------------------------------
#------------------------------- Entrega 1 -----------------------------------
#--------------------------------- P0ng game V.1 -----------------------------
#------ Por: Cristian Camilo Mendoza Mancera || ccamilo.mendoza@udea.edu.co --
#--------       C.C. 1020479827                                             --
#--------      Mateo Baena Chavarriaga       ||   mateo.baena@udea.edu.co   --
#--------       C.C. 1098781540                                             --
#--------   Estudientes de ingenieria de Sistemas ----------------------------
#------------------ Curso de procesamiento digital de imagenes ---------------
#-----------------------------------------------------------------------------

#-------------------------------- Importando librerias -----------------------
from player import Player # Modulo del jugador 
from ball import Ball     # Modulo de la pelota
import pygame             
import cv2                
import numpy as np

#---------------------------- Definiendo tamaños de la ventana ---------------
WIDTH = 640               #Ancho
HEIGHT = 480              #Alto

#----------------------- Definicion de colores a usar (Formato RGB) ----------
WHITE = (255, 255, 255)

#----------------------- Inicializacion del juego ----------------------------
pygame.init()              #Inicializacion de los modulos importados de pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))   #Inicializacion de la ventana de juego
pygame.display.set_caption("Pong")  #Asignacion del nombre a la ventana de juego
clock = pygame.time.Clock()         #Instanciacion del objeto que ratrea el tiempo de juego

background = pygame.image.load("src/assets/bg.jpg").convert()   #Carga del sprite del fondo de pantalla

all_sprites = pygame.sprite.Group() #Instanciacion del grupo de sprites que se cargara en el juego

player_1 = Player(10, HEIGHT // 2, "src/assets/player1.png") #Instanciacion del objeto del jugador 1
player_2 = Player(WIDTH - 30, HEIGHT // 2, "src/assets/player2.png") #Instancaicion del objeto del jugador 2
ball = Ball(0, 10, WIDTH // 2, HEIGHT // 2) #Instanciacion del objeto pelota

#--------------------- Adicion de objetos del juego al grupo de sprites ------
#--------------------- Usado para el control de colisiones entre objetos -----
all_sprites.add(player_1)
all_sprites.add(player_2)
all_sprites.add(ball)

#-------------- Adicion del objeto pelota al grupo de sprites de la pelota ---
#--- Usado para el control de colisiones entre la pelota y los bordes de la ventana
ball_group = pygame.sprite.GroupSingle()
ball_group.add(ball)

#-------------- Metodo para la impresion de texto en la ventana --------------
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("arial", size)   #Definicion de la fuente de pygame a usar 
    text_surface = font.render(text, True, WHITE)   #Asignacion del texto a escribir 
    text_rect = text_surface.get_rect()         #Obtencion del area rectangular del texto a escribir
    text_rect.midtop = (x, y)                   #Ubicacion del texto a ubicar en las coordenadas X y Y
    surface.blit(text_surface, text_rect)       #Dibujado del texto a escribir en la ventana

#---------- Metodo para el cambio de ventana a "fin de juego" ----------------
def show_end_game_screen(text):
    screen.blit(background, [0, 0])             #Dibujado de la pantalla de fondo en la ventana
    #Dibujado del texto que sea enviado como parametro, con un tamaño y posicion en la ventana    
    draw_text(screen, text, 50, WIDTH // 2, HEIGHT // 2)    
    draw_text(screen, "Presione cualquier tecla para volver a jugar", 30, WIDTH // 2, (HEIGHT // 2) + 70)
    
    pygame.display.flip()   #Actualizacion de la ventana con los textos dibujados
    restart = True          #Flag para determinar el reinicio del juego
    while restart:
        clock.tick(30)      #Actualizacion del objeto de reloj cada 30 milisegundos      
        for event in pygame.event.get():    #Revision de eventos de teclado
            if event.type == pygame.QUIT:   #Condicion para cierre de ventana 
                pygame.quit()               #Cierre de la ventana
            if event.type == pygame.KEYUP:  #Condicion de reinicio presionando cualquier tecla (Se captura el evento  release de la tecla)
                restart = False             #Se anula el flag de reinicio de juego para finalizar ciclo

#--------- Metodo obtener las coordenadas del objeto de interes --------------
def get_position(mask, color):
    #Inicializacion de variables de posicion del objeto de interes
    x = 0   
    y = 0

    font = cv2.FONT_HERSHEY_SIMPLEX #Definicion de la fuente a mostrar 
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))  #Definicion del elemento estructurante cuadrado de 10x10
    #-------- Definicion de la operacion morfologica y la obtencion de contornos sobre la imagen resultante con la operacion morfologica ------
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations = 8)   #Realizacion de la operacion morfologica
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    #Obtencion de los contornos encontrados con el resultado de la operacion morfologica

    #Iteracion sobre todos los contornos encontrados
    for c in contours:
        M = cv2.moments(c)  #Retorno del momento de imagen sobre el contorno encontrado en una iteracion
        #------- Obtencion del centroide del contorno de la iteracion --------
        if (M["m00"] == 0): M["m00"] = 1    #Validacion del centroide en caso de que se retorne un denominador igual a 0
        x = int(M["m10"] / M["m00"])        #Asignacion de valor al centroide en la coordenada X
        y = int(M['m01'] / M['m00'])        #Asignacion de valor al centroide en la coordenada Y
        new_contour = cv2.convexHull(c)     #Obtencion de un contorno suavizado con la operacion Convex Hull
        #------ Dibujado del contorno y centroide del objeto de interes -----
        cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)   #Dibujado de una figura circular en la posicion del centroide 
        cv2.putText(frame,f"{x}, {y}", (x + 10, y), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)    #Dibujado del texto con las coordenadas del centroide del contorno
        cv2.drawContours(frame, [new_contour], 0, color, 3)     #Dibujado del contorno suavizado en la pantalla
    return x, y     #Retorno de las posiciones del centroide


cap = cv2.VideoCapture(0)   #Captura de video con el dispositivo de captura 0


#---- Definicion de los rangos de color a usar en la segmentacion de color (Formato HSV) ----
#---- Rangos de color para el azul (Valor de Hue entre 100 y 125)
azulBajo = np.array([100, 100, 20], np.uint8)   
azulAlto = np.array([125, 255, 255], np.uint8)

#---- Rangos de color para el rojo (En los dos espectros posibles en HSV)
#---- Primer espectro de rojo (Valor de Hue entre 0 y 5)
redBajo1 = np.array([0, 100, 20], np.uint8)
redAlto1 = np.array([5, 255, 255], np.uint8)
#---- Segundo espectro de rojo (Valor de Hue entre 175 y 179)
redBajo2 = np.array([175, 100, 20], np.uint8)
redAlto2 = np.array([179, 255, 255], np.uint8)

#---- Inicializacion de variables para la inicializacion de la logica en el juego ----
end_game = False        #Flag para el control de fin de juego
end_game_message = ""   #Variable para albergar el texto que sera mostrado en el fin del juego
running = True          #Flag para el control del funcionamiento del juego

while running:  #Ciclo continuo para el funcionamiento del juego

    #Obtencion de captura de video
    #------------- ret: Variable para validar la captura de un fotograma -------------
    #------------- frame: Fotograma capturado ----------------------------------------
    ret, frame = cap.read() 

    #Inicializacion de las posiciones de los objetos de cada jugador
    player_1_x = 0 
    player_1_y = 0
    player_2_x = 0 
    player_2_y = 0

    #Validacion de captura de un fotograma
    if ret == True:
        
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Cambio del espacio de color de la captura de RGB a HSV

        #Obtencion de las mascaras para la segmentacion de color en funcion de los rangos de color de los objetos de interes
        maskAzul = cv2.inRange(frameHSV, azulBajo, azulAlto)    #Mascara para el color azul

        #Mascaras para el color rojo en los dos espectros de HSV
        maskRed1 = cv2.inRange(frameHSV, redBajo1, redAlto1)
        maskRed2 = cv2.inRange(frameHSV, redBajo2, redAlto2)
        #Suma de las dos mascaras obtenidas en rojo
        maskRed = cv2.add(maskRed1, maskRed2)

        #Obtencion de las coordenadas de los objetos de los jugadores con las mascaras en cada color necesario
        player_1_x, player_1_y = get_position(maskRed, (0, 0, 255)) 
        player_2_x, player_2_y = get_position(maskAzul, (255, 0, 0))

        cv2.imshow('frame', frame)  #Se muestra la ventana que corresponde a la muestra de la captura de video para ambas mascaras, sus centroides y contornos

        #Definicion de la tecla para cerrar la ventana anterior
        key = cv2.waitKey(1) 
        if key == ord('q') or key == ord('Q'):
            break

    #Condicion de fin de juego
    if end_game:
        show_end_game_screen(end_game_message)  #Se muestra la ventana de fin de juego
        #Se reinician valores de puntaje a cada jugador
        player_1.restart_score()
        player_2.restart_score()
        #Se reinicia el valor de la flag que determina el fin de juego
        end_game = False

    clock.tick(30)  #Actualizacion del objeto de reloj cada 30 milisegundos
    
    #Captura del evento de cierre de ventana
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

    #Actualizacion de los grupos de sprites de la pelota
    ball_group.update()
    
    #Actualizacion de la posicion de los objetos de jugadores en funcion del centroide hallado anteriormente
    player_1.update_position(player_1_x, player_1_y)
    player_2.update_position(player_2_x, player_2_y)
    
    #Definicion de la colision entre los objetos jugador 1 y pelota
    hit_ball_player1 = pygame.sprite.spritecollide(player_1, ball_group, False)
    for hit in hit_ball_player1:
        #Cambio de direccion en la posicion X de la pelota (de izquierda -> derecha)
        ball.change_x_dir() #Direccion en Y no cambia de sentido, solo cambia el sentido de X

    #Definicion de la colision entre los objetos jugador 2 y pelota
    hit_ball_player2 = pygame.sprite.spritecollide(player_2, ball_group, False)
    for hit in hit_ball_player2:
        #Cambio de direccion en la posicion de X de la pelota (de derecha -> izquierda)
        ball.change_x_dir() #Direccion en Y no cambia de sentido, solo cambia el sentido de X

    #--------------Condicion para que el jugador 2 marque 1 punto------------------
    if (ball.get_x_pos() < 0): #Si se supera el margen izquierdo de la ventana
        ball.set_pos(WIDTH // 2, HEIGHT // 2)   #Se reinicia la posicion de la pelota a la mitad de la ventana
        player_2.sum_score()    #Se suma 1 punto al puntaje del jugador 2
        score = player_2.get_score()    #Se actualiza el puntaje de ese jugador en el juego
        #Se reinician las posicion de los jugadores luego de marcar un punto
        player_1.set_pos(HEIGHT // 2)   
        player_2.set_pos(HEIGHT // 2)

    #--------------Condicion para que el jugador 1 marque 1 punto------------------
    if (ball.get_x_pos() > WIDTH):  #Si se supera el margen derecho de la ventana
        ball.set_pos(WIDTH // 2, HEIGHT // 2)   #Se reinicia la posicion de la pelota a la mitad de la ventana
        player_1.sum_score()    #Se suma 1 punto al puntaje del jugador 1
        score = player_1.get_score()    #Se actualiza el puntaje de ese jugador en el juego
        #Se reinician las posicion de los jugadores luego de marcar un punto
        player_1.set_pos(HEIGHT // 2)
        player_2.set_pos(HEIGHT // 2)

    #Obtenemos puntajes que tiene cada jugador    
    player_1_score = player_1.get_score()
    player_2_score = player_2.get_score()


    #--------------Condicion de FIN DE JUEGO------------------
    #Si un jugador supera 10 puntos es porque gano
    if player_1_score == 10:
        end_game = True
        end_game_message = "El jugador 1 ha ganado la partida"
    elif player_2_score == 10:
        end_game = True
        end_game_message = "El jugador 2 ha ganado la partida"

    #Variables para la actualizacion del puntaje de cada jugador en pantalla
    text_1 = f"Score: {player_1_score}"
    text_2 = f"Score: {player_2_score}"
    
    screen.blit(background, [0, 0]) #Actualizacion de pantalla para los cambios en posiciones de jugadores, pelota e incremento de puntaje
    all_sprites.draw(screen)    #Actualizacion en pantalla de los sprits del juego

    #Dibujado en pantalla de los puntajes de cada jugador
    draw_text(screen, text_1, 50, 90, 20)
    draw_text(screen, text_2, 50, WIDTH - 90, 20)

    #Llamado del metodo Update de cada objeto del juego
    pygame.display.update() 

#--------------Cierre del programa------------------
pygame.quit()
cap.release()
cv2.destroyAllWindows()
