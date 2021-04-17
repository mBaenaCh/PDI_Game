import pygame
BLACK = pygame.Color(0,0,0)

class Player(pygame.sprite.Sprite):
    #--------------Constructor de la clase------------------
    #self -> this.object
    #x -> Posicion en X del objeto
    #Y -> Posicion en Y del objeto
    #img -> Ubicacion y archivo del sprite del objeto
    def __init__(self, x, y, img):
        super().__init__()
        self.image = pygame.image.load(img).convert()   #Se carga al objeto el sprite que se recibe como imagen
        self.image.set_colorkey(BLACK)  #Definicion de la transparencia del sprite
        self.rect = self.image.get_rect()   #Obtencion del area rectangular del sprite
        self.rect.centery = y   #Obtencion del centroide en Y del objeto
        self.rect.x = x #Posicion en X del objeto
        self.score = 0  #Inicializacion de la propiedad Score del objeto
    
    def update(self):
        pass
    
    #--------Actualizacion de la ubicacion del objeto (Coordenadas en X y Y)--------
    def update_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    #--------Actualizacion de la propiedad Score del objeto
    def sum_score(self):
        self.score += 1

    #--------Retorno del valor de la propiedad Score del objeto--------
    def get_score(self):
        return self.score
    #--------Reset del valor de la propiedad Score del objeto
    def restart_score(self):
        self.score = 0
    
    #--------Actualizacion de la posicion del centroide en Y del objeto
    def set_pos(self, y):
        self.rect.centery = y
    