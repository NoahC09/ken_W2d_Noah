import pygame
import random
import math

# Pygame initalisieren
pygame.init()

####################################################################################
# Baupläne (=Klassendefinitionen)
# ----------------------------------------------------------------------------------

class Player_mit_Gewehr(pygame.sprite.Sprite):                                        
    def __init__(self, x_coordinate, y_coordinate):                                                  
        super().__init__()    
        # Wir laden das Bild und speichern es als ORIGINAL
        self.original_image = pygame.image.load("res/images/Figur_mit_Gewehr.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (64,64)) 
        
        self.image = self.original_image # Das ist das Bild, das angezeigt wird
        self.rect = self.image.get_rect()
        self.rect.center = (x_coordinate, y_coordinate) # Wir nutzen das Zentrum für die Position
        
        self.angle = 0 # Unser Startwinkel
        self.speed = 4                                                 
        # Stelle sicher, dass das Bild wirklich so heisst (sonst anpassen)
        self.image  = pygame.image.load("res/images/Figur_mit_Gewehr.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (64,64)) 
        self.rect   = self.image.get_rect()
        self.rect.x = x_coordinate
        self.rect.y = y_coordinate
        self.speed  = 3 

####################################################################################
# Funktionsdefinitionen
# ----------------------------------------------------------------------------------

def move_players():
    keys = pygame.key.get_pressed()
    
    # 1. Drehung (A und D)
    if keys[pygame.K_a]:
        Figur.angle += 5
    if keys[pygame.K_d]:
        Figur.angle -= 5
    # 2. Bild rotieren (Zentrum fixieren)
    Figur.image = pygame.transform.rotate(Figur.original_image, Figur.angle)
    old_center = Figur.rect.center
    Figur.rect = Figur.image.get_rect()
    Figur.rect.center = old_center
    # 3. Bewegung berechnen (Trigonometrie)
    # math.radians wandelt Grad (0-360) in das Bogenmass um, das math.cos/sin brauchen
    radians = math.radians(Figur.angle)
    move_x = math.cos(radians) * Figur.speed
    move_y = -math.sin(radians) * Figur.speed # Minus, weil Y-Achse nach unten geht
    # W = Vorwärts
    if keys[pygame.K_w]:
        Figur.rect.x += move_x
        Figur.rect.y += move_y
    # S = Rückwärts (einfach die Gegenrichtung der Berechnung oben)
    if keys[pygame.K_s]:
        Figur.rect.x -= move_x
        Figur.rect.y -= move_y
    # 4. Wand-Kollision (damit er nicht abhaut)
    if Figur.rect.left < 0: Figur.rect.left = 0
    if Figur.rect.right > screen_width: Figur.rect.right = screen_width
    if Figur.rect.top < 0: Figur.rect.top = 0
    if Figur.rect.bottom > screen_height: Figur.rect.bottom = screen_height          
    
def draw_game():
    screen.blit(background_image_game, (0,0))
    player_sprites.draw(screen)

####################################################################################
# Globale variablen initialisieren
# ----------------------------------------------------------------------------------

screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SHADOWSTRIKE")
clock = pygame.time.Clock()

# Hintergrundbild laden und korrekt skalieren
background_image_game = pygame.image.load("res/images/Map.png")
background_image_game = pygame.transform.scale(background_image_game, (screen_width, screen_height))

game_status = "game"

# Spieler erstellen
Figur = Player_mit_Gewehr(screen_width/2, screen_height/2) 
player_sprites = pygame.sprite.Group()
player_sprites.add(Figur)

####################################################################################
# Spielschleife
# ----------------------------------------------------------------------------------

is_game_running = True
while is_game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_game_running = False
   
    if game_status == "game":
        move_players()
        draw_game()
        
    pygame.display.update()
    clock.tick(60) # Korrekte Nutzung der Uhr

pygame.quit()