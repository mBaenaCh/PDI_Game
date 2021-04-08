import pygame, random
BLACK = pygame.Color(0,0,0)

class Ball(pygame.sprite.Sprite):
    def __init__(self, speed_x, speed_y, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/ball.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.speed_x = 5#random.randrange(-5, 5)
        self.speed_y = 5#random.randrange(-5, 5)
        
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if (self.rect.top < 0) or (self.rect.bottom > 800):
            self.speed_y = -self.speed_y
    
    def change_x_dir(self):
        self.speed_x = -self.speed_x

    def get_x_pos(self):
        return self.rect.x
    
    def set_pos(self, x, y):
        self.rect.x = x 
        self.rect.y = y
    