import pygame
import random
<<<<<<< HEAD

=======
 
>>>>>>> 284187bb6798e89b6aab7240a1a80c7c959c509f
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
<<<<<<< HEAD
        self.base_image = self.image_gewehr  # Originalbild für Rotation
=======
        self.base_image = self.image_gewehr  # Originalbild (unverdreht) für Rotation
>>>>>>> 284187bb6798e89b6aab7240a1a80c7c959c509f
        self.image = self.image_gewehr
        self.rect = self.image.get_rect()
        self.rect.centerx = x_coordinate
        self.rect.centery = y_coordinate
        self.speed = 5
        self.angle = 0  # 0° = schaut nach rechts (wie das Originalbild)
        self.rotation_speed = 3
<<<<<<< HEAD

=======
 
>>>>>>> 284187bb6798e89b6aab7240a1a80c7c959c509f
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
<<<<<<< HEAD
        elif i == 2: 
=======
        elif i == 2:
>>>>>>> 284187bb6798e89b6aab7240a1a80c7c959c509f
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
    keys = pygame.key.get_pressed()
<<<<<<< HEAD

=======
 
>>>>>>> 284187bb6798e89b6aab7240a1a80c7c959c509f
    # Waffenwechsel
    if keys[pygame.K_2]:
        Figur.base_image = Figur.image_granate
        Icon.image = Icon.image_grenade
    if keys[pygame.K_1]:
        Figur.base_image = Figur.image_gewehr
        Icon.image = Icon.image_rifle
<<<<<<< HEAD

=======
 
>>>>>>> 284187bb6798e89b6aab7240a1a80c7c959c509f
    # Rotation: D = rechtsherum, A = linksherum
    if keys[pygame.K_d]:
        Figur.angle -= Figur.rotation_speed  # Minus = Uhrzeigersinn in pygame
    if keys[pygame.K_a]:
        Figur.angle += Figur.rotation_speed  # Plus = Gegenuhrzeigersinn
<<<<<<< HEAD

=======
 
>>>>>>> 284187bb6798e89b6aab7240a1a80c7c959c509f
    # Bewegungsrichtung aus Winkel berechnen
    # angle=0 → schaut nach rechts → cos(0)=1, sin(0)=0
    import math
    rad = math.radians(Figur.angle)
    dir_x = math.cos(rad)
    dir_y = -math.sin(rad)  # Minus weil pygame Y-Achse nach unten geht
<<<<<<< HEAD

=======
 
>>>>>>> 284187bb6798e89b6aab7240a1a80c7c959c509f
    # W = vorwärts (in Blickrichtung), S = rückwärts
    if keys[pygame.K_w]:
        new_x = Figur.rect.centerx + dir_x * Figur.speed
        new_y = Figur.rect.centery + dir_y * Figur.speed
        if 0 <= new_x <= screen_width and 0 <= new_y <= screen_height:
            Figur.rect.centerx = int(new_x)
            Figur.rect.centery = int(new_y)
    if keys[pygame.K_s]:
        new_x = Figur.rect.centerx - dir_x * Figur.speed
        new_y = Figur.rect.centery - dir_y * Figur.speed
        if 0 <= new_x <= screen_width and 0 <= new_y <= screen_height:
            Figur.rect.centerx = int(new_x)
            Figur.rect.centery = int(new_y)
<<<<<<< HEAD

=======
 
>>>>>>> 284187bb6798e89b6aab7240a1a80c7c959c509f
    # Bild rotieren (Mittelpunkt bleibt erhalten)
    center = Figur.rect.center
    Figur.image = pygame.transform.rotate(Figur.base_image, Figur.angle)
    Figur.rect = Figur.image.get_rect(center=center)
<<<<<<< HEAD

def check_collisions(current_status):
    hitbox = Figur.rect.inflate(-20, -20)  
    for enemy in enemy_sprites:
        if enemy.rect.colliderect(hitbox):
            return "game_over"     
    return current_status

=======
 
>>>>>>> 284187bb6798e89b6aab7240a1a80c7c959c509f
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
    screen.blit(background_image_game, (0, 0))
    player_sprites.draw(screen)
    icon_sprites.draw(screen)
    enemy_sprites.draw(screen)
<<<<<<< HEAD

def draw_game_over(): 
    screen.fill((0,0,0))
    screen.blit(text,(screen_width/2 - text.get_width()/2, screen_height/3))

####################################################################################
# Globale Variablen initialisieren
# ----------------------------------------------------------------------------------

=======
 
####################################################################################
# Globale Variablen initialisieren
# ----------------------------------------------------------------------------------
 
>>>>>>> 284187bb6798e89b6aab7240a1a80c7c959c509f
screen_width = 1200
screen_height = 800
icon_x = screen_width - 120
icon_y = screen_height - 150
<<<<<<< HEAD

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SHADOWSTRIKE")
clock = pygame.time.Clock()

my_font = pygame.font.SysFont('Comic Sans MS', 96)
game_over_text = "Game Over"
text = my_font.render(game_over_text, True, (255, 165, 0))

background_image_game = pygame.image.load("res/images/Map.png")
background_image_game = pygame.transform.scale(background_image_game, (screen_width, screen_height))

game_status = "game"
Figur = Player_mit_Gewehr(screen_width / 2, screen_height / 2)
Icon = Icons(icon_x, icon_y)

=======
 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SHADOWSTRIKE")
clock = pygame.time.Clock()
 
my_font = pygame.font.SysFont('Comic Sans MS', 96)
game_over_text = "Game Over"
text = my_font.render(game_over_text, True, (255, 165, 0))
 
background_image_game = pygame.image.load("res/images/Map.png")
background_image_game = pygame.transform.scale(background_image_game, (screen_width, screen_height))
 
game_status = "game"
Figur = Player_mit_Gewehr(screen_width / 2, screen_height / 2)
Icon = Icons(icon_x, icon_y)
 
>>>>>>> 284187bb6798e89b6aab7240a1a80c7c959c509f
player_sprites = pygame.sprite.Group()
player_sprites.add(Figur)
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_game_running = False
<<<<<<< HEAD

=======
 
>>>>>>> 284187bb6798e89b6aab7240a1a80c7c959c509f
    if game_status == "game":
        move_players()
        last_spawn_time = create_enemys(last_spawn_time)
        move_enemys()
<<<<<<< HEAD
        game_status= check_collisions(game_status)
        draw_game()
    
    if game_status == "game_over":
        draw_game_over()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
=======
 
    pygame.display.update()
    clock.tick(60)
 
pygame.quit()
 
>>>>>>> 284187bb6798e89b6aab7240a1a80c7c959c509f
