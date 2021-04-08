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
        self.score = 0
        
    def update(self):
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speed_y = -5
        if keystate[pygame.K_DOWN]:
            self.speed_y = 5
        self.rect.y += self.speed_y
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 800:
            self.rect.bottom = 800
        
    def sum_score(self):
        self.score += 1

    def get_score(self):
        return self.score
    
    def restart_score(self):
        self.score = 0
    
    def set_pos(self, y):
        self.rect.centery = y