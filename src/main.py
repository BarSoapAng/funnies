import pygame
import sys
from src.map.scene    import SceneManager
from src.entity.player import Player

SCREEN_W, SCREEN_H = 800, 600
TILE_SIZE = 32
FPS = 60
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

def main():
    pygame.init()
    clock = pygame.time.Clock()
    popup_obj = None
    inventory = []

    player = Player()

    # load first room
    scenes = SceneManager(screen.get_size(), player)
    scenes.load_room("courtyard.csv")

    spawn = scenes.current_room.spawn_point
    print(spawn)
    player.x = spawn[0] * TILE_SIZE
    player.y = spawn[1] * TILE_SIZE - TILE_SIZE

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # seconds since last frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              running = False
          
            res = scenes.current_room.objects.handle_event(event, player, screen)

            if popup_obj and hasattr(popup_obj, "pinPad") and popup_obj.pinPad.active:
                popup_obj.pinPad.handle_event(event)
                # Optionally allow closing with X key globally
                if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                    popup_obj.pinPad.active = False
                    popup_obj = None
                continue 
          
            if res:
                if res["type"] == "door":
                    door = res["obj"]
                    scenes.load_room(door.leads_to)  # Make sure you load the new room here!
                    x, y = door.spawn
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
            
        if hasattr(popup_obj, "pinPad") and popup_obj.pinPad.active:
            popup_obj.pinPad.draw()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
