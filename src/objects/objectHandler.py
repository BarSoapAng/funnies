import pygame
import importlib

TILE_SIZE = 32

class InteractiveObject:
    """Base class for anything the player can interact with."""
    def __init__(self, tile_pos, width, height, message=None):
        self.rect = pygame.Rect(
            tile_pos[0] * TILE_SIZE,
            tile_pos[1] * TILE_SIZE,
            width, height
        )
        self.message = message
        if message:
            self._make_popup()

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
        # default placeholder; override in subclasses as needed
        pos = (self.rect.x - cam_off.x, self.rect.y - cam_off.y)
        pygame.draw.rect(surface, (200, 200, 0), (*pos, self.rect.w, self.rect.h))

    def is_player_facing(self, player):
        px, py = player.x, player.y
        dir = player.dir
        tx = int((px + TILE_SIZE/2) // TILE_SIZE)
        ty = int((py + TILE_SIZE*1.5) // TILE_SIZE)
        if dir == "up":    ty -= 1
        if dir == "down":  ty += 1
        if dir == "left":  tx -= 1
        if dir == "right": tx += 1
        return (self.rect.x // TILE_SIZE, self.rect.y // TILE_SIZE) == (tx, ty)

    def interact(self, screen):
        # default behavior: show popup if available
        if hasattr(self, "popup_surf"):
            sw, sh = screen.get_size()
            pw, ph = self.popup_surf.get_size()
            screen.blit(self.popup_surf, ((sw-pw)//2, (sh-ph)//2))


class ObjectHandler:
    def __init__(self, specs, scene_manager):
        class_map = {
            "TreeStump":        "src.objects.treeStump",
            "DoorOne":      "src.objects.doorOne",
            "DoorTwo":      "src.objects.doorTwo",
            "Collectible": "src.objects.collectible",
            "Vase" : "src.objects.vase",
            "DoorRose" : "src.objects.doorRose",
            "FrontDoor" : "src.objects.frontDoor",
        }

        self.objects = []
        for spec in specs:
            module_name = class_map[spec["class"]]
            module = importlib.import_module(module_name)
            cls = getattr(module, spec["class"])
            
            if spec["class"] in ("DoorOne", "DoorTwo"):
                obj = cls(spec["pos"], spec["leads_to"], scene_manager)
            
            elif spec["class"] == "DoorRose":
                obj = cls(spec["pos"], spec["leads_to"], scene_manager)
                roseDoor_obj = obj

            elif spec["class"] == "FrontDoor":
                obj = cls(spec["pos"], spec["leads_to"], scene_manager)
                frontDoor_obj = obj
            
            elif spec["class"] == "Collectible":
                obj = cls(spec["pos"], spec["item_id"], spec.get("message"))
                
            elif spec["class"] == "Vase":
                obj = cls(spec["pos"], scene_manager, roseDoor_obj)
            
            else:
                obj = cls(spec["pos"], spec.get("message"))
                
            self.objects.append(obj)

    def draw(self, surface, cam_off):
        for obj in self.objects:
            obj.draw(surface, cam_off)

    def handle_event(self, event, player, screen):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            for obj in self.objects:
                if obj.is_player_facing(player):
                    # duck-type check for Door
                    if hasattr(obj, "leads_to"):
                        if obj.interact(screen):
                            return {"type":"door",
                                    "spawn": obj.scene_manager.current_room.spawn_point}
                        else:
                            return {"type":"popup", "obj": obj}

                    # collectible: pick up and remove
                    if hasattr(obj, "item_id"):
                        item_id = obj.interact(screen)  # shows popup & returns item_id
                        self.objects.remove(obj)        # <<< remove it immediately
                        return {"type":"collectible",
                                "item_id": item_id,
                                "obj": obj}

                    # otherwise, just a popup object
                    return {"type":"popup", "obj": obj}
        return None