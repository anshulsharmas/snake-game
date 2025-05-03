"""
Main game file
"""
import sys
import random
import pygame
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE,
    BLACK, WHITE, RED, GREEN, DARK_GREEN,
    BLUE, YELLOW, PURPLE,
    INITIAL_SPEED, MIN_SPEED, MAX_SPEED,
    UP, DOWN, LEFT, RIGHT,
    POWERUP_SPAWN_CHANCE
)
from .entities.snake import Snake
from .entities.food import Food
from .entities.powerup import PowerUp
from .utils.game_utils import (
    calculate_grid_dimensions,
    handle_window_resize,
    toggle_fullscreen
)
from .utils.particles import ParticleSystem

def main():
    # Initialize Pygame
    pygame.init()
    
    # Set up the game window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()
    
    # Initialize game objects
    snake = Snake()
    food = Food()
    powerup = PowerUp()
    particles = ParticleSystem()
    font = pygame.font.Font(None, 36)
    
    # Game state
    game_over = False
    speed = INITIAL_SPEED
    is_fullscreen = False
    width, height = WINDOW_WIDTH, WINDOW_HEIGHT
    score_multiplier = 1
    ghost_mode = False
    shield_active = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen, width, height = handle_window_resize(event, screen, is_fullscreen)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:  # Toggle fullscreen
                    screen, width, height, is_fullscreen = toggle_fullscreen(screen, is_fullscreen)
                elif event.key == pygame.K_EQUALS and speed < MAX_SPEED:
                    speed += 1
                elif event.key == pygame.K_MINUS and speed > MIN_SPEED:
                    speed -= 1
                elif game_over:
                    if event.key == pygame.K_SPACE:
                        snake.reset()
                        food.randomize_position()
                        powerup = PowerUp()
                        game_over = False
                        score_multiplier = 1
                        ghost_mode = False
                        shield_active = False
                else:
                    if event.key == pygame.K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT

        if not game_over:
            # Update power-up
            if not powerup.active and random.random() < POWERUP_SPAWN_CHANCE:
                powerup.randomize_position(snake.positions)
            
            # Check power-up collision
            if snake.get_head_position() == powerup.position and not powerup.active:
                powerup.activate()
                if powerup.type == 'SPEED_BOOST':
                    speed = min(speed + 2, MAX_SPEED)
                elif powerup.type == 'DOUBLE_POINTS':
                    score_multiplier = 2
                elif powerup.type == 'GHOST':
                    ghost_mode = True
                elif powerup.type == 'SHIELD':
                    shield_active = True
                particles.add_particles(
                    powerup.position[0] * GRID_SIZE + GRID_SIZE // 2,
                    powerup.position[1] * GRID_SIZE + GRID_SIZE // 2
                )

            # Check if power-up expired
            if powerup.active and powerup.is_expired():
                if powerup.type == 'SPEED_BOOST':
                    speed = max(speed - 2, INITIAL_SPEED)
                elif powerup.type == 'DOUBLE_POINTS':
                    score_multiplier = 1
                elif powerup.type == 'GHOST':
                    ghost_mode = False
                elif powerup.type == 'SHIELD':
                    shield_active = False
                powerup = PowerUp()

            # Update snake
            if not snake.update(ghost_mode):
                if not shield_active:
                    game_over = True
                else:
                    shield_active = False
                    particles.add_particles(
                        snake.get_head_position()[0] * GRID_SIZE + GRID_SIZE // 2,
                        snake.get_head_position()[1] * GRID_SIZE + GRID_SIZE // 2,
                        count=20
                    )

            # Check if snake eats food
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1 * score_multiplier
                food.randomize_position()
                particles.add_particles(
                    food.position[0] * GRID_SIZE + GRID_SIZE // 2,
                    food.position[1] * GRID_SIZE + GRID_SIZE // 2
                )
                # Make sure food doesn't appear on snake
                while food.position in snake.positions:
                    food.randomize_position()

        # Update particles
        particles.update()

        # Draw everything
        screen.fill(BLACK)
        snake.render(screen)
        food.render(screen)
        if not powerup.active:
            powerup.render(screen)
        particles.render(screen)

        # Display score and speed
        score_text = font.render(f'Score: {snake.score}', True, WHITE)
        speed_text = font.render(f'Speed: {speed} (+/- to change)', True, WHITE)
        
        screen.blit(score_text, (10, 10))
        
        # Position speed text in top right corner
        speed_text_rect = speed_text.get_rect()
        speed_text_rect.topleft = (width - speed_text_rect.width - 10, 10)
        screen.blit(speed_text, speed_text_rect)

        # Display active power-ups
        y_offset = 50
        if score_multiplier > 1:
            powerup_text = font.render('2x Points Active!', True, PURPLE)
            screen.blit(powerup_text, (10, y_offset))
            y_offset += 30
        if ghost_mode:
            powerup_text = font.render('Ghost Mode Active!', True, WHITE)
            screen.blit(powerup_text, (10, y_offset))
            y_offset += 30
        if shield_active:
            powerup_text = font.render('Shield Active!', True, YELLOW)
            screen.blit(powerup_text, (10, y_offset))

        if game_over:
            game_over_text = font.render('Game Over! Press SPACE to restart', True, WHITE)
            screen.blit(game_over_text, (width // 4, height // 2))

        pygame.display.update()
        clock.tick(speed * 2)  # Speed control

if __name__ == '__main__':
    main() 