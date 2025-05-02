"""
Food entity implementation
"""
import random
import pygame
from ..constants import GRID_WIDTH, GRID_HEIGHT, GRID_SIZE, BROWN

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = BROWN
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                        random.randint(0, GRID_HEIGHT - 1))

    def render(self, surface):
        # Draw rat body
        x, y = self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE
        pygame.draw.ellipse(surface, self.color,
                          (x, y, GRID_SIZE, GRID_SIZE))
        
        # Draw rat ears
        ear_size = GRID_SIZE // 3
        pygame.draw.circle(surface, self.color,
                         (x + ear_size, y + ear_size), ear_size)
        pygame.draw.circle(surface, self.color,
                         (x + GRID_SIZE - ear_size, y + ear_size), ear_size)
        
        # Draw rat tail
        tail_length = GRID_SIZE
        tail_width = GRID_SIZE // 4
        pygame.draw.rect(surface, self.color,
                        (x + GRID_SIZE // 2, y + GRID_SIZE // 2,
                         tail_length, tail_width)) 