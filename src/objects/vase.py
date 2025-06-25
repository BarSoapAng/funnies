from .objectHandler import InteractiveObject, TILE_SIZE
import pygame

class Vase(InteractiveObject):
    def __init__(self, tile_pos, scene_manager, door):
        super().__init__(tile_pos, TILE_SIZE, TILE_SIZE, message=None)
        self.locked = "Something's missing..."
        self.unlocked = "Thank you for the roses!"
        self.scene_manager = scene_manager
        self.door = door

################# EDIT THIS #############################3
    def _make_popup(self):
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.message, True, (255, 255, 255))
        pad = 10
        w, h = text.get_size()
        surf = pygame.Surface((w+pad*2, h+pad*2))
        surf.fill((0, 0, 0))
        pygame.draw.rect(surf, (255, 255, 255), surf.get_rect(), 2)
        surf.blit(text, (pad, pad))
        self.popup_surf = surf

    def draw(self, surface, cam_off):
        pos = (self.rect.x - cam_off.x, self.rect.y - cam_off.y)
        pygame.draw.rect(surface, (150,75,0), (*pos, TILE_SIZE, TILE_SIZE))

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
