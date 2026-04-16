import pygame
import random

# Pygame initalisieren
pygame.init()

####################################################################################
# Baupläne (=Klassendefinitionen)
# ----------------------------------------------------------------------------------

class SpaceShip(pygame.sprite.Sprite):                                        
    def __init__(self, x_coordinate, y_coordinate):                                                  
        super().__init__()														# brauchst du nicht zu wissen
        self.image  = pygame.image.load("res/images/space_ship.png").convert_alpha()	# Bild laden
        self.image = pygame.transform.scale(self.image, (46,100))				# Bild skalieren (vergrössern/verkleinern)
        self.rect   = self.image.get_rect()										# Umrechteck bestimmen
        self.rect.x = x_coordinate												# x-Startpunkt
        self.rect.y = y_coordinate												# y-Startpunkt


def draw_game():
    screen.blit(background_image_game, (0,0))			# Hintergrund wird gezeichnet an Stelle 0,0
    player_sprites.draw(screen)         				# Objekte in Gruppe player_sprites werden gezeichnet


####################################################################################
# Globale variablen initialisieren
# ----------------------------------------------------------------------------------

# Grösse des Spielfenster setzen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))		# Fenstergrösse festlegen
pygame.display.set_caption("Space Shooter")							# Titel des Fensters setzen
clock = pygame.time.Clock() 					   					# Eine Pygame-Uhr um die Framerate zu kontrollieren


# Hintergrundbilder auf https://www.freepik.com/
background_image_game = pygame.image.load("res/images/background_game.jpg")		# Hintergrundbild laden
background_image_game = pygame.transform.scale(background_image_game, (screen_width, screen_height))	# Hintergrundbild skalieren

# Spielstatus zu Beginn
game_status = "game"
space_ship = SpaceShip(screen_width / 3, screen_height * 3 / 4)			 # Erstellen eines Space Ships

player_sprites = pygame.sprite.Group()       # Gruppe der player Sprites
player_sprites.add(space_ship)               # Die Spieler in die Gruppe legen

####################################################################################
# Spielschleife
# ----------------------------------------------------------------------------------

is_game_running = True
while is_game_running:
    for event in pygame.event.get():						# Events wie Mausklick werden abgearbeitet
        if event.type == pygame.QUIT:						# Falls auf x geklickt wird
            is_game_running = False
   
    if game_status == "game":
        draw_game()

         
    pygame.display.update()  								# Fenster updaten
    clock.tick(60)  							# Setzt die Anzahl Frames per Second auf 60

pygame.quit()