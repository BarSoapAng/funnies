from .objectHandler import InteractiveObject, TILE_SIZE

class Collectible(InteractiveObject):
    def __init__(self, tile_pos, item_id, message="You picked up an item!"):
        super().__init__(tile_pos, TILE_SIZE, TILE_SIZE, message)
        self.item_id = item_id
        self.collidable = False

    def interact(self, screen):
        # When you pick it up, show the popup (super does that)
        super().interact(screen)
        # Return a signal that we should add it to inventory & remove it
        return self.item_id