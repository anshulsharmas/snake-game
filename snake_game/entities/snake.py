"""
Snake entity implementation
"""
import random
import pygame
from ..constants import (
    GRID_WIDTH, GRID_HEIGHT, GRID_SIZE,
    GREEN, DARK_GREEN, WHITE,
    UP, DOWN, LEFT, RIGHT
)

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.head_color = DARK_GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self, ghost_mode=False):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        
        if not ghost_mode and new in self.positions[3:]:
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    def reset(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def render(self, surface):
        # Draw the body
        for i, p in enumerate(self.positions[1:], 1):
            # Make the tail segments gradually smaller
            size = GRID_SIZE * (1 - (i / (self.length * 2)))
            if size < GRID_SIZE // 2:
                size = GRID_SIZE // 2
            pygame.draw.rect(surface, self.color, 
                           (p[0] * GRID_SIZE + (GRID_SIZE - size) // 2,
                            p[1] * GRID_SIZE + (GRID_SIZE - size) // 2,
                            size, size))
        
        # Draw the head
        head = self.positions[0]
        pygame.draw.rect(surface, self.head_color,
                        (head[0] * GRID_SIZE, head[1] * GRID_SIZE,
                         GRID_SIZE, GRID_SIZE))
        
        # Draw eyes on the head
        eye_size = GRID_SIZE // 4
        eye_offset = GRID_SIZE // 4
        
        # Calculate eye positions based on direction
        if self.direction == RIGHT:
            eye_positions = [
                (head[0] * GRID_SIZE + GRID_SIZE - eye_offset, head[1] * GRID_SIZE + eye_offset),
                (head[0] * GRID_SIZE + GRID_SIZE - eye_offset, head[1] * GRID_SIZE + GRID_SIZE - eye_offset)
            ]
        elif self.direction == LEFT:
            eye_positions = [
                (head[0] * GRID_SIZE + eye_offset, head[1] * GRID_SIZE + eye_offset),
                (head[0] * GRID_SIZE + eye_offset, head[1] * GRID_SIZE + GRID_SIZE - eye_offset)
            ]
        elif self.direction == UP:
            eye_positions = [
                (head[0] * GRID_SIZE + eye_offset, head[1] * GRID_SIZE + eye_offset),
                (head[0] * GRID_SIZE + GRID_SIZE - eye_offset, head[1] * GRID_SIZE + eye_offset)
            ]
        else:  # DOWN
            eye_positions = [
                (head[0] * GRID_SIZE + eye_offset, head[1] * GRID_SIZE + GRID_SIZE - eye_offset),
                (head[0] * GRID_SIZE + GRID_SIZE - eye_offset, head[1] * GRID_SIZE + GRID_SIZE - eye_offset)
            ]
        
        for eye_pos in eye_positions:
            pygame.draw.circle(surface, WHITE, eye_pos, eye_size) 