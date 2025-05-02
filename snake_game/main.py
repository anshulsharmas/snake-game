"""
Main game file
"""
import sys
import pygame
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE,
    BLACK, WHITE,
    INITIAL_SPEED, MIN_SPEED, MAX_SPEED,
    UP, DOWN, LEFT, RIGHT
)
from .entities.snake import Snake
from .entities.food import Food
from .utils.game_utils import (
    calculate_grid_dimensions,
    handle_window_resize,
    toggle_fullscreen
)

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
    font = pygame.font.Font(None, 36)
    
    # Game state
    game_over = False
    speed = INITIAL_SPEED
    is_fullscreen = False
    width, height = WINDOW_WIDTH, WINDOW_HEIGHT

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
                        game_over = False
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
            if not snake.update():
                game_over = True

            # Check if snake eats food
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                food.randomize_position()
                # Make sure food doesn't appear on snake
                while food.position in snake.positions:
                    food.randomize_position()

        # Draw everything
        screen.fill(BLACK)
        snake.render(screen)
        food.render(screen)

        # Display score and speed
        score_text = font.render(f'Score: {snake.score}', True, WHITE)
        speed_text = font.render(f'Speed: {speed}', True, WHITE)
        speed_control_text = font.render('(+/- to change)', True, WHITE)
        
        screen.blit(score_text, (10, 10))
        
        # Position speed text in top right corner
        speed_text_rect = speed_text.get_rect()
        speed_text_rect.topleft = (width - speed_text_rect.width - 10, 10)
        screen.blit(speed_text, speed_text_rect)
        
        # Position speed control text below speed
        speed_control_rect = speed_control_text.get_rect()
        speed_control_rect.topleft = (width - speed_control_rect.width - 10, 50)
        screen.blit(speed_control_text, speed_control_rect)

        if game_over:
            game_over_text = font.render('Game Over! Press SPACE to restart', True, WHITE)
            screen.blit(game_over_text, (width // 4, height // 2))

        pygame.display.update()
        clock.tick(speed * 2)  # Speed control

if __name__ == '__main__':
    main() 