import pygame
import random

pygame.init()


WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint ойыны")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
current_color = (0, 0, 255)  
eraser_mode = False 


radius = 5
drawing_shape = None  
shape_start = None  
points = []


clock = pygame.time.Clock()

def draw_buttons():
    pygame.draw.rect(screen, (200, 200, 200), (10, 10, 80, 30))  
    pygame.draw.rect(screen, (200, 200, 200), (100, 10, 80, 30))  
    pygame.draw.rect(screen, current_color, (540, 10, 80, 30))  
    pygame.draw.rect(screen, (255, 200, 200) if eraser_mode else (200, 200, 200), (190, 10, 80, 30))  
    
    font = pygame.font.Font(None, 24)
    screen.blit(font.render("Rect ", True, BLACK), (20, 20))
    screen.blit(font.render("Circle ", True, BLACK), (110, 20))
    screen.blit(font.render("Eraser ", True, BLACK), (200, 20))
    screen.blit(font.render("Color", True, WHITE if sum(current_color) < 300 else BLACK), (550, 20))


running = True
prev_pos = None

while running:
    screen.fill(WHITE)  
    draw_buttons() 

    
    for item in points:
        if item["type"] == "line":
            pygame.draw.line(screen, item["color"], item["start"], item["end"], item["size"])
        elif item["type"] == "rect":
            pygame.draw.rect(screen, item["color"], item["rect"], 3)
        elif item["type"] == "circle":
            pygame.draw.circle(screen, item["color"], item["center"], item["radius"], 3)

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()

    
    if mouse_pressed[0] and prev_pos:
        color = WHITE if eraser_mode else current_color
        points.append({"type": "line", "color": color, "start": prev_pos, "end": mouse_pos, "size": radius})
    prev_pos = mouse_pos if mouse_pressed[0] else None

    
    if mouse_pressed[2] and not drawing_shape:
        shape_start = mouse_pos
        drawing_shape = "circle" if keys[pygame.K_LALT] else "rect"

    
    elif not mouse_pressed[2] and drawing_shape:
        x1, y1 = shape_start
        x2, y2 = mouse_pos
        width, height = abs(x2 - x1), abs(y2 - y1)

        if keys[pygame.K_LSHIFT]:  
            width = height = max(width, height)
        
        if drawing_shape == "rect":
            points.append({"type": "rect", "color": current_color, "rect": pygame.Rect(min(x1, x2), min(y1, y2), width, height)})
        elif drawing_shape == "circle":
            radius = max(width, height) // 2
            center = (x1 + width // 2, y1 + height // 2)
            points.append({"type": "circle", "color": current_color, "center": center, "radius": radius})
        
        drawing_shape = None  

   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t: 
                current_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            elif event.key == pygame.K_e:  
                eraser_mode = not eraser_mode
            elif event.key == pygame.K_ESCAPE:
                running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                radius = max(1, radius - 2)
            elif event.button == 3:  
                radius = min(50, radius + 2)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
