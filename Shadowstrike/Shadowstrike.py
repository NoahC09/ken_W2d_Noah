import pygame
import random

# Pygame initalisieren
pygame.init()

####################################################################################
# Baupläne (=Klassendefinitionen)
# ----------------------------------------------------------------------------------

class Player_mit_Gewehr(pygame.sprite.Sprite):                                        
    def __init__(self, x_coordinate, y_coordinate):                                                  
        super().__init__()
        load_image_gewehr = pygame.image.load("res/images/Figur_mit_Gewehr.png").convert_alpha()
        self.image_gewehr = pygame.transform.scale(load_image_gewehr, (64, 64))
        load_image_granate = pygame.image.load("res/images/Figur_mit_Granate.png").convert_alpha()
        self.image_granate = pygame.transform.scale(load_image_granate, (64, 64))
        self.image = self.image_gewehr
        self.rect = self.image.get_rect()
        self.rect.x = x_coordinate
        self.rect.y = y_coordinate
        self.speed = 3

import pygame
import random

class Enemy(pygame.sprite.Sprite):                                        
    def __init__(self, enemy_speed):                                                  
        super().__init__()                                                                                                   
        self.image = pygame.image.load("res/images/Enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        i = random.randint(1, 4)

        if i == 1:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = -self.rect.height
        
        elif i == 2: 
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = screen_height
        
        elif i == 3:
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, screen_height - self.rect.height)

        elif i == 4:
            self.rect.x = screen_width
            self.rect.y = random.randint(0, screen_height - self.rect.height)
        self.speed = enemy_speed

class Icons(pygame.sprite.Sprite):                                        
    def __init__(self, x_coordinate, y_coordinate):                                                  
        super().__init__()
        load_image_rifle = pygame.image.load("res/images/rifle_icon.png").convert_alpha()
        self.image_rifle = pygame.transform.scale(load_image_rifle, (96, 64))
        load_image_grenade = pygame.image.load("res/images/grenade_icon.png").convert_alpha()
        self.image_grenade = pygame.transform.scale(load_image_grenade, (64, 64))
        self.image = self.image_rifle
        self.rect = self.image.get_rect()
        self.rect.x = x_coordinate
        self.rect.y = y_coordinate

####################################################################################
# Funktionsdefinitionen
# ----------------------------------------------------------------------------------

def move_players():
    keys = pygame.key.get_pressed()                    # Abfrage aller Tasten
    if keys[pygame.K_2]:
        Figur.image = Figur.image_granate
        Icon.image = Icon.image_grenade
    if keys[pygame.K_1]:
        Figur.image = Figur.image_gewehr
        Icon.image = Icon.image_rifle
    if keys[pygame.K_w] and Figur.rect.y > 0:  # True falls w gedrückt wird
        Figur.rect.y -= Figur.speed           # Änderung der y-Koordinate des Space Ship
    if keys[pygame.K_s] and Figur.rect.y + Figur.rect.height < screen_height:
        Figur.rect.y += Figur.speed
    if keys[pygame.K_a] and Figur.rect.x > 0:
        Figur.rect.x -= Figur.speed
    if keys[pygame.K_d] and Figur.rect.x + Figur.rect.width < screen_width:
        Figur.rect.x += Figur.speed                   

def move_enemys():
    for enemy in enemy_sprites:
        enemy.rect.y += enemy.speed
        if enemy.rect.y > screen_height:
            enemy.kill()

def create_enemys(last_spawn_time):
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > 1000 + random.randint(0, 0):
        enemy = Enemy(2)
        enemy_sprites.add(enemy)
        last_spawn_time = current_time
    return last_spawn_time

def draw_game():
    screen.blit(background_image_game, (0,0))
    player_sprites.draw(screen)
    icon_sprites.draw(screen)
    enemy_sprites.draw(screen)
    
####################################################################################
# Globale variablen initialisieren
# ----------------------------------------------------------------------------------

# Grösse des Spielfenster setzen
screen_width = 1200
screen_height = 800
icon_x = screen_width - 120
icon_y = screen_height - 150

screen = pygame.display.set_mode((screen_width, screen_height))     # Fenstergrösse festlegen
pygame.display.set_caption("SHADOWSTRIKE")                     # Titel des Fensters setzen
clock = pygame.time.Clock()                                         # Eine Pygame-Uhr um die Framerate zu kontrollieren

my_font = pygame.font.SysFont('Comic Sans MS', 96)
game_over_text = "Game Over"
text = my_font.render(game_over_text, True, (255, 165, 0))

# Hintergrundbilder auf https://www.freepik.com/
background_image_game = pygame.image.load("res/images/Map.png")     # Hintergrundbild laden
background_image_game = pygame.transform.scale(background_image_game, (screen_width, screen_height))    # Hintergrundbild skalieren

game_status = "game"
Figur = Player_mit_Gewehr(screen_width/2, screen_height/2)          # Erstellen eines Space Ships  
Icon = Icons(icon_x, icon_y)

player_sprites = pygame.sprite.Group()       # Gruppe der player Sprites
player_sprites.add(Figur)               # Die Spieler in die Gruppe legen
icon_sprites = pygame.sprite.Group()
icon_sprites.add(Icon)

enemy = Enemy(2)
enemy_sprites = pygame.sprite.Group()
enemy_sprites.add(enemy)

last_spawn_time = pygame.time.get_ticks()

####################################################################################
# Spielschleife
# ----------------------------------------------------------------------------------

is_game_running = True
while is_game_running:
    for event in pygame.event.get():                        # Events wie Mausklick werden abgearbeitet
        if event.type == pygame.QUIT:                       # Falls auf x geklickt wird
            is_game_running = False
   
    if game_status == "game":
        move_players()
        last_spawn_time = create_enemys(last_spawn_time)
        draw_game()
        move_enemys()

    pygame.display.update()                                 # Fenster updaten
    clock.tick(60)                                          # Setzt die Anzahl Frames per Second auf 60

pygame.quit()