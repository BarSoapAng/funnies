from .doorTwo import DoorTwo

class DoorRose(DoorTwo):
    def __init__(self, tile_pos, leads_to, scene_manager, spawn_point):
        super().__init__(tile_pos, leads_to, scene_manager, spawn_point)
        self.open = False
        self.message = "It's locked."

    def interact(self, screen):
        if self.open:
            self.scene_manager.load_room(self.leads_to)
            return True
        else:
            self._make_popup()
            sw, sh = screen.get_size()
            pw, ph = self.popup_surf.get_size()
            screen.blit(self.popup_surf, ((sw-pw)//2, (sh-ph)//2))
            return False

