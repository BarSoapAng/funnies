import pygame
import sys
from src.map.scene    import SceneManager
from src.entity.player import Player
from src.objects.conditionalObject import ConditionalObject

SCREEN_W, SCREEN_H = 800, 600
TILE_SIZE = 32
FPS = 60

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()
    popup_obj = None
    inventory = []

    # load first room
    scenes = SceneManager(screen.get_size())
    scenes.load_room("courtyard.csv")

    player = Player(scenes.current_room.spawn_point)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # seconds since last frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              running = False
          
            res = scenes.current_room.objects.handle_event(event, player, screen)
            if res:
                if res["type"] == "pin":
                    ####################################### EDIT HERE
                    popup_obj = True
                    continue
                elif res["type"] == "door":
                    x,y = res["spawn"]
                    player.x = x * TILE_SIZE
                    player.y = y * TILE_SIZE - TILE_SIZE
                    popup_obj = None
                elif res["type"] == "collectible":
                    item_id=res["item_id"]
                    inventory.append(item_id)
                    scenes.collected_items.add(item_id)
                    popup_obj = res["obj"]
                    print(inventory)
                else:
                    popup_obj = res["obj"]
                    
                    if isinstance(popup_obj, ConditionalObject):
                        co = popup_obj
                        # if they had the key, co.interact already ran action()
                        if co.required_item in scenes.collected_items:
                            scenes.current_room.objects.objects.remove(co)

            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                popup_obj = None

        # movement only when no popup is showing
        if not popup_obj:
            keys = pygame.key.get_pressed()
            player.update(dt, keys, scenes.current_room)

        # draw
        screen.fill((0, 0, 0))  # the “void” outside rooms
        scenes.current_room.draw(screen, player.camera_offset)
        scenes.current_room.objects.draw(screen, player.camera_offset)
        player.draw(screen)
        
        if popup_obj:
            popup_obj.interact(screen)
            
        # event loop
        scenes.current_room.objects.handle_event(event, player, screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
