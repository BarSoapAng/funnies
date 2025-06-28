from .objectHandler import InteractiveObject, TILE_SIZE
import pygame

class Doors(InteractiveObject):
    def __init__(self, tile_pos, leads_to, scene_manager, spawn_point):
        super().__init__(tile_pos, TILE_SIZE, TILE_SIZE, message=None)
        self.leads_to = leads_to
        self.scene_manager = scene_manager
        self.unlocked = True
        self.spawn = spawn_point

    def interact(self, screen):
        self.scene_manager.load_room(self.leads_to)
        return True
