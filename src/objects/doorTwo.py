from .objectHandler import InteractiveObject, TILE_SIZE
import pygame

class DoorTwo(InteractiveObject):
    def __init__(self, tile_pos, leads_to, scene_manager):
        super().__init__(tile_pos, TILE_SIZE, TILE_SIZE, message=None)
        self.leads_to = leads_to
        self.scene_manager = scene_manager

    def draw(self, surface, cam_off):
        pos = (self.rect.x - cam_off.x, self.rect.y - cam_off.y - TILE_SIZE)
        pygame.draw.rect(surface, (150,75,0), (*pos, TILE_SIZE, TILE_SIZE*2))

    def interact(self, screen):
        self.scene_manager.load_room(self.leads_to)
        return True

