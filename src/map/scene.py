import pygame
import csv
from src.objects.objectHandler import ObjectHandler
import json

TILE_SIZE = 32
WALL_TILE = "1"

with open("src\map\specs.json") as f:
    ALL_SPECS = json.load(f)

class Room:
    def __init__(self, grid, spawn, SceneManager, map_name, collected):
        self.grid = grid        # 2D list of strings
        self.spawn_point = spawn
        
        specs = ALL_SPECS.get(map_name, [])
        filtered = []
        
        for s in specs:
            if s.get("item_id") and s["item_id"] in collected:
                continue
            filtered.append(s)
        self.objects = ObjectHandler(filtered, SceneManager)


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
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == WALL_TILE:
                    world_pos = (x*TILE_SIZE - camera_offset.x,
                                 y*TILE_SIZE - camera_offset.y)
                    pygame.draw.rect(surf, (100,100,100), (*world_pos, TILE_SIZE, TILE_SIZE))
        self.objects.draw(surf, camera_offset)

class SceneManager:
    def __init__(self, screen_size):
        self.current_room = None
        self.screen_size = screen_size
        self.collected_items = set()

    def load_room(self, filename):
        grid = []
        spawn = (1,1)
        with open(f"src/map/rooms/{filename}", newline="") as f:
            reader = csv.reader(f)
            for y,row in enumerate(reader):
                grid.append(row)
                for x,cell in enumerate(row):
                    if cell == "S":  # mark spawn in your CSV
                        spawn = (x, y)
        self.current_room = Room(grid, spawn, self, filename, self.collected_items)
