import pygame

TILE_SIZE = 32

def load_and_scale(path, w, h):
  img = pygame.image.load(path).convert_alpha()
  return pygame.transform.scale(img, (w, h))
  

class Player:
    def __init__(self, spawn):
        # spawn is (x_tile, y_tile)
        self.x = spawn[0] * TILE_SIZE
        self.y = spawn[1] * TILE_SIZE - TILE_SIZE  # two tiles tall
        self.speed = 120  # pixels per second
        self.dir = "down"
        self.frame = 0
        self.images = {
            "down":  load_and_scale("src\\assets\\player\\down.png",  TILE_SIZE, TILE_SIZE*2),
            "up":    load_and_scale("src\\assets\\player\\top.png",    TILE_SIZE, TILE_SIZE*2),
            "left":  load_and_scale("src\\assets\\player\\left.png",  TILE_SIZE, TILE_SIZE*2),
            "right": load_and_scale("src\\assets\\player\\right.png", TILE_SIZE, TILE_SIZE*2),
        }

    @property
    def camera_offset(self):
        # center camera on bottom‐center of player
        screen_w, screen_h = pygame.display.get_surface().get_size()
        cam_x = self.x + TILE_SIZE/2 - screen_w/2
        cam_y = self.y + TILE_SIZE - screen_h/2
        return pygame.Vector2(cam_x, cam_y)

    def update(self, dt, keys, room):
        dx = dy = 0
        
        if keys[pygame.K_LSHIFT]:
            self.speed = 240
        else:
            self.speed = 120

        if keys[pygame.K_UP]:
            dy = -self.speed * dt; self.dir = "up"
        elif keys[pygame.K_DOWN]:
            dy = self.speed * dt;  self.dir = "down"
        elif keys[pygame.K_LEFT]:
            dx = -self.speed * dt; self.dir = "left"
        elif keys[pygame.K_RIGHT]:
            dx = self.speed * dt;  self.dir = "right"

        # simulate 1×1 collision at foot:
        new_x = self.x + dx
        new_y = self.y + dy
        foot_rect = pygame.Rect(new_x + 1, new_y + TILE_SIZE - 1, TILE_SIZE - 1, TILE_SIZE - 1)
        if not room.collides(foot_rect):
            self.x = new_x
            self.y = new_y

        # step animation (if you have sprite sheets, advance self.frame here)
        
    def draw(self, surf):
        img = self.images[self.dir]
        # we draw at world position minus camera
        offset = self.camera_offset
        draw_pos = (self.x - offset.x, self.y - offset.y)
        surf.blit(img, draw_pos)
