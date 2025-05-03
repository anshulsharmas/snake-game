"""
Power-up entity implementation
"""
import random
import pygame
from ..constants import (
    GRID_WIDTH, GRID_HEIGHT, GRID_SIZE,
    WHITE, RED, BLUE, YELLOW, PURPLE
)

class PowerUp:
    TYPES = {
        'SPEED_BOOST': {'color': BLUE, 'duration': 10000, 'effect': 'speed'},
        'SHIELD': {'color': YELLOW, 'duration': 8000, 'effect': 'shield'},
        'DOUBLE_POINTS': {'color': PURPLE, 'duration': 12000, 'effect': 'double_points'},
        'GHOST': {'color': WHITE, 'duration': 8000, 'effect': 'ghost'}
    }

    def __init__(self):
        self.type = random.choice(list(self.TYPES.keys()))
        self.position = self._random_position()
        self.active = False
        self.start_time = 0
        self.duration = self.TYPES[self.type]['duration']
        self.color = self.TYPES[self.type]['color']

    def _random_position(self):
        return (random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1))

    def randomize_position(self, snake_positions):
        while True:
            self.position = self._random_position()
            if self.position not in snake_positions:
                break

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def is_expired(self):
        if not self.active:
            return False
        return pygame.time.get_ticks() - self.start_time > self.duration

    def render(self, surface):
        if not self.active:
            # Draw power-up
            rect = pygame.Rect(
                self.position[0] * GRID_SIZE,
                self.position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(surface, self.color, rect)
            # Draw a border
            pygame.draw.rect(surface, WHITE, rect, 1)
            
            # Draw power-up symbol
            font = pygame.font.Font(None, 24)
            if self.type == 'SPEED_BOOST':
                text = font.render('⚡', True, WHITE)
            elif self.type == 'SHIELD':
                text = font.render('🛡️', True, WHITE)
            elif self.type == 'DOUBLE_POINTS':
                text = font.render('2x', True, WHITE)
            else:  # GHOST
                text = font.render('👻', True, WHITE)
            
            text_rect = text.get_rect(center=rect.center)
            surface.blit(text, text_rect) 