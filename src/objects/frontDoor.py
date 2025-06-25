from .doorTwo import DoorTwo, TILE_SIZE
import pygame

class PinPadPopup:
    def __init__(self):
        self.correct_code = "071424"
        self.input_code = ""
        self.active = True
        self.on_success = "Something unlocked."
        self.on_fail = "Hint: 6 numbers"
        # self.font = pygame.font.SysFont(None, 36)

    def handle_event(self, event):
        ################################ EDIT HERE
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                if self.input_code == self.correct_code:
                    self.message = "Unlocked!"
                    self.active = False
                    self.on_success()
                else:
                    self.message = "Incorrect"
                    self.input_code = ""
                    self.on_fail()
            elif event.key == pygame.K_BACKSPACE:
                self.input_code = self.input_code[:-1]
            elif event.unicode.isdigit():
                self.input_code += event.unicode

    def draw(self, surface):
        sw, sh = surface.get_size()
        popup_w, popup_h = 300, 150
        popup = pygame.Surface((popup_w, popup_h))
        popup.fill((30, 30, 30))
        pygame.draw.rect(popup, (255,255,255), popup.get_rect(), 2)

        code_surf = self.font.render(self.input_code, True, (255,255,255))
        popup.blit(code_surf, (20, 40))

        msg_surf = self.font.render(self.message, True, (255,0,0))
        popup.blit(msg_surf, (20, 90))

        surface.blit(popup, ((sw-popup_w)//2, (sh-popup_h)//2))

class FrontDoor(DoorTwo):
    def __init__(self, tile_pos, leads_to, scene_manager):
        super().__init__(tile_pos, leads_to, scene_manager)
        self.leads_to = leads_to
        self.scene_manager = scene_manager
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

