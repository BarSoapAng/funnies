import pygame
from .objectHandler import InteractiveObject, TILE_SIZE

class ConditionalObject(InteractiveObject):
    
    def __init__(self, tile_pos, required_item,
                 locked_message, unlock_message,
                 action_callable=None):
        super().__init__(tile_pos, TILE_SIZE, TILE_SIZE, message=None)
        self.required_item  = required_item
        self.locked_message = locked_message
        self.unlock_message = unlock_message
        self.action_callable = action_callable

    def interact(self, screen):
        # Decide which message to show
        if self.required_item in self.scene_manager.collected_items:
            self.message = self.unlock_message
            self._make_popup()
            super().interact(screen)
            if self.action_callable:
                self.action_callable()
        else:
            self.message = self.locked_message
            self._make_popup()
            super().interact(screen)
        return self
