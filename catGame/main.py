
import pygame
import time
import random
import sys

pygame.mixer.init()
pygame.mixer.music.load("background_sound.mp3")
fail_sound =pygame.mixer.Sound("catfight.mp3")
fail_sound.set_volume(.50)
happy_sound = pygame.mixer.Sound("kitten.mp3")
happy_sound.set_volume(.50)
pygame.mixer.music.play(-1)

pygame.display.set_caption("KITTIE GAME <3")
pygame.font.init()
clock = pygame.time.Clock()
CAT_SPEED =4
OBJECT_SPEED =5
OBJECT_WIDTH = 100
OBJECT_HEIGHT = 100
LIVES_SIZE =30
LIVES_SPACING = 40
STARTING_LIVES = 9
LIVES_COLOR=(255,0,0)
FPS = 40
# Pencere boyutu
WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH,HEIGHT))

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (200, 100, 200)
COLOR = (250,100,150)
#Resimler
background_picture = pygame.transform.scale(pygame.image.load("pictures/background.jpg"), (1000, 700))
screen.blit(background_picture,(0,0))
pygame.display.update()
cat_picture = pygame.transform.scale(pygame.image.load("pictures/cat.png"),(50,50))


food = pygame.transform.scale(pygame.image.load("pictures/food.png"),(100,100))
food2 = pygame.transform.scale(pygame.image.load("pictures/food2.png"),(100,100))
food3 = pygame.transform.scale(pygame.image.load("pictures/food3.png"),(100,100))

trash = pygame.transform.scale(pygame.image.load("pictures/trash.png"),(100,100))
trash2 = pygame.transform.scale(pygame.image.load("pictures/trash2.png"),(100,100))
trash3 = pygame.transform.scale(pygame.image.load("pictures/trash3.png"),(100,100))

OBJECT_TYPES ={'good':{
    'images':{
    "pictures/food.png",
    "pictures/food2.png",
    "pictures/food3.png"},
    'points':1},
'bad':{
    'images':{
    "pictures/trash.png",
    "pictures/trash2.png",
    "pictures/trash3.png"},
    'points':-3

}}

# Kedi sınıfı
class Cat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image =pygame.transform.scale(pygame.image.load("pictures/cat.png"),(250,250)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 460
        self.life = 9
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -=CAT_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x +=CAT_SPEED
        if self.rect.left<0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        screen.fill((0,0,0),self.rect)
        screen.blit(background_picture,(0,0))

class Object(pygame.sprite.Sprite):
    def __init__(self,object_type):
        pygame.sprite.Sprite.__init__(self)
        self.type = object_type
        self.images = []

        for image_path in OBJECT_TYPES[object_type]['images']:
            image = pygame.image.load(image_path).convert_alpha()
            self.images.append(pygame.transform.scale(image,(90,80)))

        self.image_index = 0
        self.image =self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH -OBJECT_WIDTH)
        self.rect.y = random.randrange(-200,-OBJECT_HEIGHT)
        self.speedy = random.randrange(OBJECT_SPEED-2 , OBJECT_SPEED+3)


    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(0,WIDTH - OBJECT_WIDTH)
            self.rect.y = random.randrange(-200, -OBJECT_HEIGHT)
            self.speedy = random.randrange(OBJECT_SPEED - 2 , OBJECT_SPEED+3)

pygame.display.update()

all_sprites = pygame.sprite.Group()
objects = pygame.sprite.Group()
lives = pygame.sprite.Group()
cat = Cat()
all_sprites.add(cat)


for i in range(3):
    for i in range(2):
        obj = Object(list(OBJECT_TYPES.keys())[i])
        all_sprites.add(obj)
        objects.add(obj)

def draw_text(surface, text, size,x, y) :
    font = pygame.font.SysFont("Times new roman", 35)
    text_surface = font.render(text, True, COLOR )
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)
    font = pygame.font.SysFont("Times new roman",25)
    text = font.render("LIFE : ", True , COLOR)
    screen.blit(text,(405,15))
def new_game():

    pygame.mixer.music.load("background_sound.mp3")
    pygame.mixer.music.play(-1)

    lives = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    objects = pygame.sprite.Group()
    cat = Cat()
    all_sprites.add(cat)

    life = 9
    for i in range(2):
        obj = Object('good')
        all_sprites.add(obj)
        objects.add(obj)
    for i in range(3):
        obj = Object('bad')
        all_sprites.add(obj)
        objects.add(obj)

    # Start game loop
    running = True
    while running:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update()
        hits = pygame.sprite.spritecollide(cat, objects, True)
        for hit in hits:
            if hit.type == 'good':
                cat.life += OBJECT_TYPES[hit.type]['points']
                obj = Object('good')
                all_sprites.add(obj)
                objects.add(obj)
                happy_sound.play()
            elif hit.type == 'bad':
                cat.life += OBJECT_TYPES[hit.type]['points']
                obj = Object('bad')
                all_sprites.add(obj)
                objects.add(obj)
                fail_sound.play()
                if cat.life == 0:
                    running = False
                    game_over()

        all_sprites.draw(screen)
        draw_text(screen, str(cat.life), 18, WIDTH / 2, 10)
        pygame.display.flip()
# Update
        all_sprites.update()
        hits = pygame.sprite.spritecollide(cat, objects, True)
        for hit in hits:
            if hit.type == 'good':
                cat.life += OBJECT_TYPES[hit.type]['points']
                obj = Object('good')
                all_sprites.add(obj)
                objects.add(obj)
                happy_sound.play()
            elif hit.type == 'bad':
               # score += OBJECT_TYPES[hit.type]['points']
                obj = Object('bad')
                all_sprites.add(obj)
                objects.add(obj)
                #life = lives.sprites()[-1]
                cat.life += OBJECT_TYPES[hit.type]['points']
                fail_sound.play()
                #life.kill()
                if cat.life == 0 or cat.life<0:
                    running = False
                    game_over()

def game_over():
    draw_text(screen, "G A M E   O V E R", 100, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Press space to play again", 70, WIDTH / 2, HEIGHT / 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE :
                    waiting = False
    new_game()

def Menu():
    font = pygame.font.SysFont("Times new roman", 50)

    running = True
    while running:
        screen.blit(background_picture,(0,0))
        title_writing = font.render("Click to start the game ", 1, COLOR)
        screen.blit(title_writing, (WIDTH / 2 - title_writing.get_width() / 2, 200))
        pygame.display.update()

        for event in pygame.event.get(): 
            pygame.display.flip()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                   new_game()
        clock.tick(FPS)

        pygame.display.update()
        all_sprites.draw(screen)

    pygame.quit()

Menu()










