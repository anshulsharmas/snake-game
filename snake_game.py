import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
GRID_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
BROWN = (139, 69, 19)
GRAY = (100, 100, 100)

# Set up the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

def calculate_grid_dimensions():
    global GRID_WIDTH, GRID_HEIGHT
    GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
    GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

calculate_grid_dimensions()

class Tooltip:
    def __init__(self, text, font):
        self.text = text
        self.font = font
        self.visible = False
        self.rect = None

    def show(self, pos):
        self.visible = True
        self.pos = pos

    def hide(self):
        self.visible = False

    def render(self, surface):
        if self.visible:
            text_surface = self.font.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect()
            
            # Create background rectangle
            padding = 5
            bg_rect = pygame.Rect(
                self.pos[0],
                self.pos[1] - text_rect.height - padding * 2,
                text_rect.width + padding * 2,
                text_rect.height + padding * 2
            )
            
            # Draw background
            pygame.draw.rect(surface, GRAY, bg_rect)
            pygame.draw.rect(surface, WHITE, bg_rect, 1)  # Border
            
            # Draw text
            surface.blit(text_surface, (self.pos[0] + padding, self.pos[1] - text_rect.height - padding))

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

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        if new in self.positions[3:]:
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

# Directional constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def main():
    global screen, WINDOW_WIDTH, WINDOW_HEIGHT, GRID_WIDTH, GRID_HEIGHT
    snake = Snake()
    food = Food()
    font = pygame.font.Font(None, 36)
    game_over = False
    speed = 5  # Initial speed level
    is_fullscreen = False

    # Create tooltip
    tooltip = Tooltip("+/- to change speed", font)
    speed_text_rect = None

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                if not is_fullscreen:
                    WINDOW_WIDTH, WINDOW_HEIGHT = event.size
                    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
                    calculate_grid_dimensions()
                    # Reset snake position to center of new grid
                    snake.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
                    food.randomize_position()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:  # Toggle fullscreen
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
                        calculate_grid_dimensions()
                        # Reset snake position to center of new grid
                        snake.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
                        food.randomize_position()
                    else:
                        screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
                        WINDOW_WIDTH, WINDOW_HEIGHT = 600, 400
                        calculate_grid_dimensions()
                        # Reset snake position to center of new grid
                        snake.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
                        food.randomize_position()
                elif event.key == pygame.K_EQUALS and speed < 10:  # Increase speed
                    speed += 1
                elif event.key == pygame.K_MINUS and speed > 1:  # Decrease speed
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
        speed_control_text = font.render('+/- to change', True, WHITE)
        
        screen.blit(score_text, (10, 10))
        
        # Position speed text in top right corner
        speed_text_rect = speed_text.get_rect()
        speed_text_rect.topleft = (WINDOW_WIDTH - speed_text_rect.width - 10, 10)
        screen.blit(speed_text, speed_text_rect)
        
        # Position speed control text below speed
        speed_control_rect = speed_control_text.get_rect()
        speed_control_rect.topleft = (WINDOW_WIDTH - speed_control_rect.width - 10, 50)
        screen.blit(speed_control_text, speed_control_rect)

        # Show tooltip if mouse is over speed indicator
        if speed_text_rect and speed_text_rect.collidepoint(mouse_pos):
            tooltip.show((speed_text_rect.right + 5, speed_text_rect.centery))
        else:
            tooltip.hide()
        
        # Draw tooltip last to ensure it's on top
        tooltip.render(screen)

        if game_over:
            game_over_text = font.render('Game Over! Press SPACE to restart', True, WHITE)
            screen.blit(game_over_text, (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2))

        pygame.display.update()
        clock.tick(speed * 2)  # Speed control

if __name__ == '__main__':
    main() 