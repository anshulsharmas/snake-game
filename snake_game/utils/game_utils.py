"""
Game utility functions
"""
import pygame
from ..constants import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE

def calculate_grid_dimensions():
    """Calculate grid dimensions based on window size"""
    return WINDOW_WIDTH // GRID_SIZE, WINDOW_HEIGHT // GRID_SIZE

def handle_window_resize(event, screen, is_fullscreen):
    """Handle window resize events"""
    if not is_fullscreen:
        new_width, new_height = event.size
        screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
        return screen, new_width, new_height
    return screen, WINDOW_WIDTH, WINDOW_HEIGHT

def toggle_fullscreen(screen, is_fullscreen):
    """Toggle between fullscreen and windowed mode"""
    if is_fullscreen:
        screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
        return screen, 600, 400, False
    else:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        width, height = screen.get_size()
        return screen, width, height, True 