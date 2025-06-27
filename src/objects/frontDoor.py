from .doorTwo import DoorTwo
from src.main import screen
import pygame

class PinPadPopup:
    def __init__(self, door):
        self.correct_code = "070424"
        self.input_code = ""
        self.active = True
        self.door = door
        self.message = ""
        # self.on_success = "Something unlocked."
        # self.on_fail = "Hint: 6 numbers"
        self.font = pygame.font.SysFont(None, 36)

    def draw(self):
        sw, sh = screen.get_size()
        popup_w, popup_h = 300, 150
        popup = pygame.Surface((popup_w, popup_h))
        popup.fill((30, 30, 30))
        pygame.draw.rect(popup, (255,255,255), popup.get_rect(), 2)

        code_surf = self.font.render(self.input_code, True, (255,255,255))
        popup.blit(code_surf, (20, 40))

        msg_surf = self.font.render(self.message, True, (255,0,0))
        popup.blit(msg_surf, (20, 90))

        screen.blit(popup, ((sw-popup_w)//2, (sh-popup_h)//2))
        
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.input_code == self.correct_code:
                    self.active = False
                    self.door.open = True
                else:
                    self.message = "Hint: 6#"
                    self.input_code = ""
            elif event.key == pygame.K_BACKSPACE:
                self.input_code = self.input_code[:-1]
            elif event.key == pygame.K_x:
                self.active = False
            elif event.unicode.isdigit():
                self.input_code += event.unicode

class FrontDoor(DoorTwo):
    def __init__(self, tile_pos, leads_to, scene_manager):
        super().__init__(tile_pos, leads_to, scene_manager)
        self.open = False
        self.pinPad = PinPadPopup(self)

    def interact(self, screen):
        if self.open:
            self.scene_manager.load_room(self.leads_to)
            return True
        else:
            self.pinPad.active = True
            return False

