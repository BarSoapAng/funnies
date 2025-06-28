import pygame

TILE_SIZE = 32

def load_and_scale(path, w, h):
  img = pygame.image.load(path).convert_alpha()
  return pygame.transform.scale(img, (w, h))
  

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0  # two tiles tall
        self.speed = 120  # pixels per second
        self.dir = "down"
        self.frame = 0
        self.images = {
            "down": [
                load_and_scale("src/assets/player/down1.png", TILE_SIZE, TILE_SIZE*2),
                load_and_scale("src/assets/player/down2.png", TILE_SIZE, TILE_SIZE*2)
            ],
            "up": [
                load_and_scale("src/assets/player/up1.png", TILE_SIZE, TILE_SIZE*2),
                load_and_scale("src/assets/player/up2.png", TILE_SIZE, TILE_SIZE*2)
            ],
            "left": [
                load_and_scale("src/assets/player/left1.png", TILE_SIZE, TILE_SIZE*2),
                load_and_scale("src/assets/player/left2.png", TILE_SIZE, TILE_SIZE*2)
            ],
            "right": [
                load_and_scale("src/assets/player/right1.png", TILE_SIZE, TILE_SIZE*2),
                load_and_scale("src/assets/player/right2.png", TILE_SIZE, TILE_SIZE*2)
            ],
            "idle": [
                load_and_scale("src/assets/player/idle1.png", TILE_SIZE, TILE_SIZE*2),
                load_and_scale("src/assets/player/idle2.png", TILE_SIZE, TILE_SIZE*2)
            ]
        }
        self.anim_timer = 0
        self.anim_speed = 0.35

    @property
    def camera_offset(self):
        # center camera on bottom‐center of player
        screen_w, screen_h = pygame.display.get_surface().get_size()
        cam_x = self.x + TILE_SIZE/2 - screen_w/2
        cam_y = self.y + TILE_SIZE - screen_h/2
        return pygame.Vector2(cam_x, cam_y)

    def update(self, dt, keys, room):
        dx = dy = 0
        self.moving = False

        if keys[pygame.K_LSHIFT]:
            self.speed = 240
            self.anim_speed = 0.25
        else:
            self.speed = 120
            self.anim_speed = 0.35

        if keys[pygame.K_UP]:
            dy = -self.speed * dt; self.dir = "up"; self.moving = True
        elif keys[pygame.K_DOWN]:
            dy = self.speed * dt;  self.dir = "down"; self.moving = True
        elif keys[pygame.K_LEFT]:
            dx = -self.speed * dt; self.dir = "left"; self.moving = True
        elif keys[pygame.K_RIGHT]:
            dx = self.speed * dt;  self.dir = "right"; self.moving = True

        new_x = self.x + dx
        new_y = self.y + dy
        foot_rect = pygame.Rect(new_x + 1, new_y + TILE_SIZE - 1, TILE_SIZE - 1, TILE_SIZE - 1)
        if not room.collides(foot_rect):
            self.x = new_x
            self.y = new_y

        # Animation logic
        if self.moving:
            self.anim_timer += dt
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0
                self.frame = (self.frame + 1) % 2
        else:
            self.anim_timer += dt
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0
                self.frame = (self.frame + 1) % 2
        
    def draw(self, surf):
        if self.moving:
            img = self.images[self.dir][self.frame]
        else:
            img = self.images["idle"][self.frame]
        offset = self.camera_offset
        draw_pos = (self.x - offset.x, self.y - offset.y)
        surf.blit(img, draw_pos)
