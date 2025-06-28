from .doors import Doors, TILE_SIZE
import pygame

class DoorTwo(Doors):
    def __init__(self, tile_pos, leads_to, scene_manager, spawn_point):
        super().__init__(tile_pos, leads_to, scene_manager, spawn_point)
        self.leads_to = leads_to
        self.scene_manager = scene_manager
        self.unlocked = False

