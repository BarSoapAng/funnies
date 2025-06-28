from .objectHandler import InteractiveObject, TILE_SIZE
import pygame

class Vase(InteractiveObject):
    def __init__(self, tile_pos, scene_manager, door):
        super().__init__(tile_pos, TILE_SIZE, TILE_SIZE, message=None)
        self.locked = "Something's missing..."
        self.unlocked = "Thank you for the roses!"
        self.scene_manager = scene_manager
        self.door = door

    def interact(self,screen):
        if "rose" in self.scene_manager.collected_items:
            self.message = self.unlocked
            self.door.open = True
        else:
            self.message = self.locked

        self._make_popup()
        sw, sh = screen.get_size()
        pw, ph = self.popup_surf.get_size()
        screen.blit(self.popup_surf, ((sw-pw)//2, (sh-ph)//2))
