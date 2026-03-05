
import random

# Pygame initalisieren
pygame.init()

####################################################################################
# Baupläne (=Klassendefinitionen)
# ----------------------------------------------------------------------------------

class SpaceShip(pygame.sprite.Sprite):                                        
    def __init__(self, x_coordinate, y_coordinate):                                                  
        super().__init__()														# brauchst du nicht zu wissen
        self.image  = pygame.image.load("res/images/plane.png").convert_alpha()	# Bild laden
        self.image = pygame.transform.scale(self.image, (150,150))				# Bild skalieren (vergrössern/verkleinern)
        self.rect   = self.image.get_rect()										# Umrechteck bestimmen
        self.rect.x = x_coordinate												# x-Startpunkt
        self.rect.y = y_coordinate												# y-Startpunkt
        self.speed  = 2                                      					# Geschwindigkeit des Spielers

####################################################################################
# Funktionsdefinitionen
# ----------------------------------------------------------------------------------

def move_players():
    keys = pygame.key.get_pressed()						# Abfrage aller Tasten
    if keys[pygame.K_w]: 							 	# True falls w gedrückt wird
        space_ship.rect.y -= space_ship.speed			# Änderung der y-Koordinate des Space Ship


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
pygame.display.set_caption("Fighting Plane")						# Titel des Fensters setzen
clock = pygame.time.Clock() 					   					# Eine Pygame-Uhr um die Framerate zu kontrollieren

# Hintergrundbilder auf https://www.freepik.com/
background_image_game = pygame.image.load("res/images/background_start.jpg")		# Hintergrundbild laden
background_image_game = pygame.transform.scale(background_image_game, (300, 300))	# Hintergrundbild skalieren

# Spielstatus zu Beginn
game_status = "game"
space_ship = SpaceShip(100, 400)			 # Erstellen eines Space Ships

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
        move_players()
        draw_game()
         

    pygame.display.update()  								# Fenster updaten
    pygame.time.Clock().tick(60)  							# Setzt die Anzahl Frames per Second auf 60

pygame.quit()