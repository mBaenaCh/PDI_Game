import pygame
BLACK = pygame.Color(0,0,0)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__()
        self.image = pygame.image.load(img).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.x = x
        self.speed_y = 0
        
    def update(self):
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speed_y = -2
        if keystate[pygame.K_DOWN]:
            self.speed_y = 2
        self.rect.y += self.speed_y
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 800:
            self.rect.bottom = 800
        
