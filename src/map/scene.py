import pygame
import csv
from src.objects.objectHandler import ObjectHandler
import json

TILE_SIZE = 32
WALL_TILE = "1"

with open("src\map\specs.json") as f:
    ALL_SPECS = json.load(f)

class Room:
    def __init__(self, grid, SceneManager, map_name, collected, player):
        self.grid = grid
        self.map_image = pygame.image.load(f"src/map/rooms/{map_name}.png").convert_alpha()
        
        specs = ALL_SPECS.get(map_name, [])
        filtered = []
        
        for s in specs:
            if s.get("item_id") and s["item_id"] in collected:
                continue
            filtered.append(s)
        self.objects = ObjectHandler(filtered, SceneManager, player)


    def collides(self, rect):
        # check any tile marked "1" intersects rect
        x0 = int(rect.left // TILE_SIZE)
        y0 = int(rect.top  // TILE_SIZE)
        x1 = int(rect.right // TILE_SIZE)
        y1 = int(rect.bottom// TILE_SIZE)
        for y in range(y0, y1+1):
            for x in range(x0, x1+1):
                if (0 <= y < len(self.grid) and 0 <= x < len(self.grid[0])
                    and self.grid[y][x] == WALL_TILE):
                    return True
        for obj in self.objects.objects:
            if rect.colliderect(obj.rect):
                return True
        return False

    def draw(self, surf, camera_offset):
        map_width = self.map_image.get_width() // TILE_SIZE
        map_height = self.map_image.get_height() // TILE_SIZE
        for y in range(map_height):
            for x in range(map_width):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                tile = self.map_image.subsurface(rect)
                world_pos = (x * TILE_SIZE - camera_offset.x, y * TILE_SIZE - camera_offset.y)
                surf.blit(tile, world_pos)
        self.objects.draw(surf, camera_offset)

class SceneManager:
    def __init__(self, screen_size, player):
        self.current_room = None
        self.screen_size = screen_size
        self.collected_items = set()
        self.player = player

    def load_room(self, filename):
        grid = []
        with open(f"src/map/rooms/{filename}.csv", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                grid.append(row)
        self.current_room = Room(grid, self, filename, self.collected_items, self.player)
