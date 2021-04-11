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
        self.score = 0
        
    def update(self):
        pass

    def update_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        
    def sum_score(self):
        self.score += 1

    def get_score(self):
        return self.score
    
    def restart_score(self):
        self.score = 0
    
    def set_pos(self, y):
        self.rect.centery = y
    