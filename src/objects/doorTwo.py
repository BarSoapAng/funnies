from .doors import Doors, TILE_SIZE
import pygame

class DoorTwo(Doors):
    def __init__(self, tile_pos, leads_to, scene_manager):
        super().__init__(tile_pos, leads_to, scene_manager)
        self.leads_to = leads_to
        self.scene_manager = scene_manager
        self.unlocked = False

    def draw(self, surface, cam_off):
        pos = (self.rect.x - cam_off.x, self.rect.y - cam_off.y - TILE_SIZE)
        pygame.draw.rect(surface, (150,75,0), (*pos, TILE_SIZE, TILE_SIZE*2))

