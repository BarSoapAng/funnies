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
        self.FONT = pygame.font.Font("src/assets/PixelifySans-Regular.ttf", 18)
        self.message = message
        if message:
            self._make_popup()

    def _make_popup(self):
        text = self.FONT.render(self.message, True, (255, 255, 255))
        pad = 10
        w, h = text.get_size()
        surf = pygame.Surface((w+pad*2, h+pad*2))
        surf.fill((0, 0, 0))
        pygame.draw.rect(surf, (255, 255, 255), surf.get_rect(), 2)
        surf.blit(text, (pad, pad))
        self.popup_surf = surf

    def draw(self, surface, cam_off):
        pass

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
    def __init__(self, specs, scene_manager, player):
        class_map = {
            "Notes":    "src.objects.notes",
            "DoorOne":      "src.objects.doorOne",
            "DoorTwo":      "src.objects.doorTwo",
            "Collectible": "src.objects.collectible",
            "Vase" : "src.objects.vase",
            "DoorRose" : "src.objects.doorRose",
            "FrontDoor" : "src.objects.frontDoor",
            "FakeDoor" : "src.objects.fakeDoor",
        }

        self.objects = []
        for spec in specs:
            module_name = class_map[spec["class"]]
            module = importlib.import_module(module_name)
            cls = getattr(module, spec["class"])
            
            if spec["class"] in ("DoorOne", "DoorTwo", "FakeDoor"):
                obj = cls(spec["pos"], spec["leads_to"], scene_manager, spec["spawn_point"])
            
            elif spec["class"] == "FrontDoor":
                obj = cls(spec["pos"], spec["leads_to"], scene_manager, spec["spawn_point"], player)
            
            elif spec["class"] == "DoorRose":
                obj = cls(spec["pos"], spec["leads_to"], scene_manager, spec["spawn_point"])
                roseDoor_obj = obj

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
                    
                    if hasattr(obj, "leads_to"):
                        if obj.interact(screen):
                            return {"type":"door", "obj":obj}
                        else:
                            return {"type":"popup", "obj": obj}

                    if hasattr(obj, "item_id"):
                        item_id = obj.interact(screen)  # shows popup & returns item_id
                        self.objects.remove(obj)        # <<< remove it immediately
                        return {"type":"collectible",
                                "item_id": item_id,
                                "obj": obj}

                    if hasattr(obj, "required_item"):
                        item_id = obj.interact(screen)  # shows popup & returns item_id
                        self.objects.remove(obj)        # <<< remove it immediately
                        return {"type":"collrequirerectible",
                                "item_id": item_id,
                                "obj": obj}
                        
                    return {"type":"popup", "obj": obj}
        return None