"""
Game constants and configuration
"""

# Window settings
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Directional constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game settings
INITIAL_SPEED = 5
MIN_SPEED = 1
MAX_SPEED = 10
POWERUP_SPAWN_CHANCE = 0.2  # Increased from 0.1 to 0.2 (20% chance)
POWERUP_DURATION = 10000  # 10 seconds in milliseconds

# Visual effects
PARTICLE_COLORS = [
    (255, 255, 255),  # White
    (255, 255, 0),    # Yellow
    (255, 165, 0),    # Orange
    (255, 0, 0)       # Red
]
PARTICLE_LIFETIME = 1000  # 1 second in milliseconds
PARTICLE_SPEED = 2
PARTICLE_COUNT = 10 