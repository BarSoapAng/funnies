from .doorTwo import DoorTwo
from src.main import screen, TILE_SIZE
import pygame

class FakePadPopup:
    def __init__(self):
        self.correct_code = "."
        self.input_code = ""
        self.active = True
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
                self.input_code = ""
            elif event.key == pygame.K_BACKSPACE:
                self.input_code = self.input_code[:-1]
            elif event.key == pygame.K_x:
                self.active = False
            elif event.unicode.isdigit():
                self.input_code += event.unicode

class FakeDoor(DoorTwo):
    def __init__(self, tile_pos, leads_to, scene_manager, spawn_point):
        super().__init__(tile_pos, leads_to, scene_manager, spawn_point)
        self.pinPad = FakePadPopup()

    def interact(self, screen):
        self.pinPad.active = True
        return False
