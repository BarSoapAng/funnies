from .doors import Doors, TILE_SIZE

class DoorOne(Doors):
    def __init__(self, tile_pos, leads_to, scene_manager, spawn_point):
        super().__init__(tile_pos, leads_to, scene_manager, spawn_point)