import pygame
import random

pygame.init()

# Screen dimensions
width = 800
height = 600

# Create game window
screen = pygame.display.set_mode((width, height))

# Variables
score = 0
level = 1
fruit_eaten = False
speed = 200  # Initial speed

# Initial snake body
squares = [
    [30, 100], [40, 100], [50, 100], [60, 100], [70, 100],
    [80, 100], [90, 100], [100, 100]
]

# Generate fruit in a valid position
def generate_fruit():
    while True:
        fr_x = random.randrange(1, width // 10) * 10
        fr_y = random.randrange(1, height // 10) * 10
        fruit_coor = [fr_x, fr_y]
        if fruit_coor not in squares:
            return fruit_coor

fruit_coor = generate_fruit()
head_square = [100, 100]

direction = "right"
next_dir = "right"
done = False

# Game Over function
def game_over(font, size, color):
    global done
    g_o_font = pygame.font.SysFont(font, size)
    g_o_surface = g_o_font.render(f"Game Over, your score: {score}", True, color)
    g_o_rect = g_o_surface.get_rect()
    g_o_rect.center = (width // 2, height // 2)
    screen.blit(g_o_surface, g_o_rect)
    pygame.display.update()
    pygame.time.delay(4000)
    pygame.quit()
    sys.exit()

# Gameplay loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                next_dir = "down"
            if event.key == pygame.K_UP:
                next_dir = "up"
            if event.key == pygame.K_LEFT:
                next_dir = "left"
            if event.key == pygame.K_RIGHT:
                next_dir = "right"
    
    # Direction logic
    if next_dir == "right" and direction != "left":
        direction = "right"
    if next_dir == "up" and direction != "down":
        direction = "up"
    if next_dir == "left" and direction != "right":
        direction = "left"
    if next_dir == "down" and direction != "up":
        direction = "down"
    
    # Move head
    if direction == "right":
        head_square[0] += 10
    if direction == "left":
        head_square[0] -= 10
    if direction == "up":
        head_square[1] -= 10
    if direction == "down":
        head_square[1] += 10
    
    new_square = list(head_square)
    
    # Check collision with itself (excluding newly added head)
    if new_square in squares[:-1]:
        game_over("times new roman", 45, (255, 0, 0))
    
    # Collision with boundaries
    if head_square[0] < 0 or head_square[0] >= width or head_square[1] < 0 or head_square[1] >= height:
        game_over("times new roman", 45, (255, 0, 0))
    
    squares.append(new_square)
    
    # Check if the snake eats the fruit
    if head_square == fruit_coor:
        fruit_eaten = True
        score += 10
        
        # Increase level and speed every 30 points
        if score % 30 == 0:
            level += 1
            speed = max(50, speed - 20)  # Increase speed but limit minimum delay
    else:
        squares.pop(0)  # Only remove tail if fruit not eaten
    
    # Generate new fruit
    if fruit_eaten:
        fruit_coor = generate_fruit()
        fruit_eaten = False
    
    # Drawing section
    screen.fill((0, 0, 0))
    
    # Display score and level
    score_font = pygame.font.SysFont("times new roman", 20)
    score_surface = score_font.render(f"Score: {score}  Level: {level}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))
    
    # Draw fruit
    pygame.draw.circle(screen, (0, 255, 0), (fruit_coor[0] + 5, fruit_coor[1] + 5), 5)
    
    # Draw snake
    for el in squares:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(el[0], el[1], 10, 10))
    
    pygame.display.flip()
    pygame.time.delay(speed)

pygame.quit()
