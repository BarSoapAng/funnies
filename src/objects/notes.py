from .objectHandler import InteractiveObject, TILE_SIZE
import pygame
class Notes(InteractiveObject):
    def __init__(self, tile_pos, message="You see a tree stump."):
        super().__init__(tile_pos, TILE_SIZE, TILE_SIZE, message)
        # if you had a special sprite, you could load it here

