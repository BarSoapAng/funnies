from .collectible import Collectible
import pygame

class Rose(Collectible):
    def __init__(self, tile_pos, item_id, message=""):
        super().__init__(tile_pos, tile_pos, item_id, message)
        self.picture = pygame.image.load("src/assets/objects/rose.png").convert_alpha()
    
    def draw(self, surface, cam_off):
        pos = (self.rect.x - cam_off.x, self.rect.y - cam_off.y)
        surface.blit(self.picture, pos)