from .doorTwo import DoorTwo
from src.main import screen, TILE_SIZE
import pygame

class PinPadPopup:
    def __init__(self, door):
        self.correct_code = "070424"
        self.input_code = ""
        self.active = True
        self.door = door
        self.FONT = pygame.font.Font("src/assets/PixelifySans-Regular.ttf", 18)

    def draw(self):
        sw, sh = screen.get_size()
        popup_w, popup_h = 200, 50
        popup = pygame.Surface((popup_w, popup_h))
        popup.fill((30, 30, 30))
        pygame.draw.rect(popup, (255,255,255), popup.get_rect(), 2)

        code_surf = self.FONT.render(self.input_code, True, (255,255,255))
        popup.blit(code_surf, (20, 15))

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
                    self.input_code = ""
            elif event.key == pygame.K_BACKSPACE:
                self.input_code = self.input_code[:-1]
            elif event.key == pygame.K_x:
                self.active = False
            elif event.unicode.isdigit():
                self.input_code += event.unicode

class FrontDoor(DoorTwo):
    def __init__(self, tile_pos, leads_to, scene_manager, spawn_point, player):
        super().__init__(tile_pos, leads_to, scene_manager, spawn_point)
        self.open = False
        self.pinPad = PinPadPopup(self)
        self.player = player

    def interact(self, screen):
        if self.open:
            self.scene_manager.load_room(self.leads_to)
            x, y = self.spawn
            self.player.x = x * TILE_SIZE
            self.player.y = y * TILE_SIZE - TILE_SIZE
            return True
        else:
            self.pinPad.active = True
            return False

