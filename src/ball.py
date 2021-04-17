import pygame, random
BLACK = pygame.Color(0,0,0)

class Ball(pygame.sprite.Sprite):
    #--------------Constructor de la clase------------------
    #self -> this.object
    #speed_x -> Velocidad en X del objeto
    #speed_y -> Velocidad en Y del objeto
    #img -> Ubicacion y archivo del sprite del objeto
    def __init__(self, speed_x, speed_y, x, y):
        super().__init__()
        self.image = pygame.image.load('src/assets/ball.png').convert() #Se carga al objeto el sprite que se recibe como imagen
        self.image.set_colorkey(BLACK)  #Definicion de la transparencia del sprite
        self.rect = self.image.get_rect() #Obtencion del area rectangular del sprite
        self.rect.y = y #Posicion en X del objeto
        self.rect.x = x #Posicion en Y del objeto
        #Definicion y asignacion de valor a la propiedad de velocidad en X y Y del objeto
        self.speed_x = 5  
        self.speed_y = 5

    #------Control del rebote de la pelota al chochar con los margenes superiores e inferiores de la ventana------
    def update(self):
        #Asignacion de velocidad en X y Y de la pelota
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        #------Condicion de choque con margen superior o inferior del area rectangular de la pelota------
        #Si el margen superior del rectangulo supera el margen superior de la ventana, hay un rebote y cambio de direccion en la velocidad de Y
        #Si el margen inferior del rectangulo supera el margen inferior de la ventana, hay un rebote y cambio de direccion en la velocidad de Y
        if (self.rect.top < 0) or (self.rect.bottom > 480):
            self.speed_y = -self.speed_y
    
    #------Cambio de direccion en la velocidad en X del objeto------
    def change_x_dir(self):
        self.speed_x = -self.speed_x
    #------Obtencion de la posicion en X del objeto
    def get_x_pos(self):
        return self.rect.x
    #------Asignacion de posicion en X y Y del objeto------
    def set_pos(self, x, y):
        self.rect.x = x 
        self.rect.y = y
    