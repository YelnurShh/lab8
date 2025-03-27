import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

# Backround music
pygame.mixer.music.load('/Users/elnrsahar/Desktop/Python tasks/lab8/racer/background.wav')
pygame.mixer.music.play(-1)

# FPS 
FPS = 60
FramePerSec = pygame.time.Clock()


BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0


font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

#function load_images
def load_images():
    images = {
        "background": pygame.image.load('/Users/elnrsahar/Desktop/Python tasks/lab8/racer/AnimatedStreet.png'),
        "enemy": pygame.image.load('/Users/elnrsahar/Desktop/Python tasks/lab8/racer/Enemy.png'),
        "player": pygame.image.load('/Users/elnrsahar/Desktop/Python tasks/lab8/racer/Player.png'),
        "coin": pygame.image.load('/Users/elnrsahar/Desktop/Python tasks/lab8/racer/Coin.png'),
        "crash_sound": pygame.mixer.Sound('/Users/elnrsahar/Desktop/Python tasks/lab8/racer/crash.wav')
    }
    images["coin"] = pygame.transform.scale(images["coin"], (30, 30))  
    return images

images = load_images()

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

#Enemy player
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = images["enemy"]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

#My car
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = images["player"]
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

#Money
class Coin(pygame.sprite.Sprite):
    def __init__(self, enemy_rects):
        super().__init__()
        self.image = images["coin"]
        self.rect = self.image.get_rect()
        self.spawn_coin(enemy_rects)

    def spawn_coin(self, enemy_rects):
        while True:
            x = random.randint(40, SCREEN_WIDTH - 40)
            y = 0
            new_rect = pygame.Rect(x, y, self.rect.width, self.rect.height)
            if not any(new_rect.colliderect(enemy_rect) for enemy_rect in enemy_rects):
                self.rect.center = (x, y)
                break

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn_coin([enemy.rect for enemy in enemies])

P1 = Player()
E1 = Enemy()
C1 = Coin([E1.rect])

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(images["background"], (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    coins_text = font_small.render("Coins: " + str(COINS_COLLECTED), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(coins_text, (300,10))

    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()
        images["crash_sound"].play()
        time.sleep(1)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    if pygame.sprite.spritecollideany(P1, coins):
        COINS_COLLECTED += 1
        for coin in coins:
            coin.spawn_coin([enemy.rect for enemy in enemies])
    
    pygame.display.update()
    FramePerSec.tick(FPS)
