import pygame
import random
import math

pygame.init()
pygame.mixer.init()
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
        self.base_image = self.image_gewehr  
        self.image = self.image_gewehr
        self.rect = self.image.get_rect()
        self.rect.centerx = x_coordinate
        self.rect.centery = y_coordinate
        self.speed = 5
        self.angle = 0  
        self.rotation_speed = 3
        self.last_shot_time = 0
        self.aktuelle_waffe = "gewehr"  

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
        
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)
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

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.art = Figur.aktuelle_waffe 

        if self.art == "gewehr":
            load_projectile_image = pygame.image.load("res/images/projectile.png").convert_alpha()
            scaled_image = pygame.transform.scale(load_projectile_image, (12, 36))
            drehen_image = pygame.transform.rotate(scaled_image, 90)
            self.image = pygame.transform.rotate(drehen_image, angle)
            self.speed = 15
        
        elif self.art == "granate":
            load_projectile_image = pygame.image.load("res/images/granate.png").convert_alpha()
            scaled_image = pygame.transform.scale(load_projectile_image, (12, 8))
            self.image = pygame.transform.rotate(scaled_image, angle)
            self.speed = 7
    
        self.rect = self.image.get_rect(center=(x, y))
        rad = math.radians(angle)
        self.dir_x = math.cos(rad)
        self.dir_y = -math.sin(rad)
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)

    def update(self):
        self.pos_x += self.dir_x * self.speed
        self.pos_y += self.dir_y * self.speed
        self.rect.centerx = int(self.pos_x)
        self.rect.centery = int(self.pos_y)
        if self.rect.x < 0 or self.rect.x > screen_width or self.rect.y < 0 or self.rect.y > screen_height:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__ (self, x, y):
        super().__init__()
        self.bilder = [
            pygame.transform.scale(pygame.image.load("res/images/frame_1.png").convert_alpha(), (128, 128)),
            pygame.transform.scale(pygame.image.load("res/images/frame_2.png").convert_alpha(), (128, 128)),
            pygame.transform.scale(pygame.image.load("res/images/frame_3.png").convert_alpha(), (128, 128)),
            pygame.transform.scale(pygame.image.load("res/images/frame_4.png").convert_alpha(), (128, 128)),
            pygame.transform.scale(pygame.image.load("res/images/frame_5.png").convert_alpha(), (128, 128)),
            pygame.transform.scale(pygame.image.load("res/images/frame_6.png").convert_alpha(), (128, 128))
        ]
        self.aktueller_frame = 0
        self.image = self.bilder[self.aktueller_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 3  
        self.timer = 0
        
    def update(self):
        self.timer += 1
        if self.timer >= self.animation_speed:
            self.timer = 0
            self.aktueller_frame += 1
            
            if self.aktueller_frame >= len(self.bilder):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.bilder[self.aktueller_frame]
                self.rect = self.image.get_rect(center=center)

####################################################################################
# Funktionsdefinitionen
# ----------------------------------------------------------------------------------
 
def move_players():
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
 
    
    if keys[pygame.K_2]:
        Figur.base_image = Figur.image_granate
        Icon.image = Icon.image_grenade
        Figur.aktuelle_waffe = "granate"
        sound_switch.play()
    if keys[pygame.K_1]:
        Figur.base_image = Figur.image_gewehr
        Icon.image = Icon.image_rifle
        Figur.aktuelle_waffe = "gewehr"
        sound_switch.play()
 
    
    if keys[pygame.K_d]:
        Figur.angle -= Figur.rotation_speed
    if keys[pygame.K_a]:
        Figur.angle += Figur.rotation_speed
 
    
    rad = math.radians(Figur.angle)
    dir_x = math.cos(rad)
    dir_y = -math.sin(rad)
 
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

    
    if keys[pygame.K_SPACE] and current_time - Figur.last_shot_time > 430:
            projectile = Projectile(Figur.rect.centerx, Figur.rect.centery, Figur.angle)
            projectile_sprites.add(projectile)
            sound_schuss.play()
            Figur.last_shot_time = current_time
            
    
    center = Figur.rect.center
    Figur.image = pygame.transform.rotate(Figur.base_image, Figur.angle)
    Figur.rect = Figur.image.get_rect(center=center)

def check_projectile_collisions():
    for projectile in projectile_sprites:
        for enemy in enemy_sprites:
            geschrumpfte_hitbox = enemy.rect.inflate(-20, -20)
            
            if geschrumpfte_hitbox.colliderect(projectile.rect):
                if projectile.art == "granate":
                    pos_x = projectile.rect.centerx
                    pos_y = projectile.rect.centery
                    projectile.kill()
                    
                    booom = Explosion(pos_x, pos_y)
                    explosion_sprites.add(booom)
                    sound_explosion.play()
                    
                    for naher_enemy in enemy_sprites:
                        if naher_enemy.rect.colliderect(booom.rect):
                            naher_enemy.kill()
                else:
                    enemy.kill()
                    projectile.kill()
                break

def check_collisions(current_status):
    hitbox = Figur.rect.inflate(-30, -30)  
    for enemy in enemy_sprites:
        if enemy.rect.colliderect(hitbox):
            sound_hurt.play()
            return "game_over"     
    return current_status

 
def move_enemys():
    for enemy in enemy_sprites:
        diffx = Figur.rect.centerx - enemy.rect.centerx
        diffy = Figur.rect.centery - enemy.rect.centery
        distanz = math.sqrt(diffx**2 + diffy**2)

        if distanz != 0:
            enemy.pos_x += (diffx / distanz) * enemy.speed
            enemy.pos_y += (diffy / distanz) * enemy.speed
            enemy.rect.centerx = int(enemy.pos_x)
            enemy.rect.centery = int(enemy.pos_y)

        enemy.rect.y += enemy.speed
        if enemy.rect.y > screen_height:
            enemy.kill()

 
def create_enemys(last_spawn_time):
    current_time = pygame.time.get_ticks()
    if current_time - Figur.last_difficulty_time > 20000:
        if Figur.spawn_cooldown > 400:  
            Figur.spawn_cooldown -= 200 
        Figur.last_difficulty_time = current_time 
    if current_time - last_spawn_time > Figur.spawn_cooldown:
        enemy_new = Enemy(2)
        enemy_sprites.add(enemy_new)
        last_spawn_time = current_time
        
    return last_spawn_time

def reset_game():
    enemy_sprites.empty()
    projectile_sprites.empty()
    explosion_sprites.empty()
    
    Figur.rect.centerx = screen_width / 2
    Figur.rect.centery = screen_height / 2
    Figur.angle = 0
    Figur.aktuelle_waffe = "gewehr"
    Figur.base_image = Figur.image_gewehr
    Figur.image = Figur.image_gewehr
    
    Figur.spawn_cooldown = 1500
    Figur.last_difficulty_time = pygame.time.get_ticks()
    
    return pygame.time.get_ticks()

def draw_game():
    screen.blit(background_image_game, (0, 0))
    player_sprites.draw(screen)
    icon_sprites.draw(screen)
    enemy_sprites.draw(screen)
    projectile_sprites.draw(screen)
    explosion_sprites.draw(screen) 

def draw_game_over(): 
    screen.fill((0,0,0))
    screen.blit(text_game_over,(screen_width/2 - text_game_over.get_width()/2, screen_height/3))
    

def draw_restart_game():
    screen.blit(text_restart, (screen_width/2 - text_game_over.get_width()/2, screen_height/2))

####################################################################################
# Globale Variablen initialisieren
# ----------------------------------------------------------------------------------
 
screen_width = 1200
screen_height = 800
icon_x = screen_width - 120
icon_y = screen_height - 150
 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SHADOWSTRIKE")
clock = pygame.time.Clock()
 
my_font_game_over = pygame.font.SysFont('Comic Sans MS', 96)
my_font_restart = pygame.font.SysFont('Comic Sans MS', 30)
game_over_text = "Game Over"
restart_text = "Drücke die Leertaste um neu zu starten"
text_game_over = my_font_game_over.render(game_over_text, True, (255, 165, 0))
text_restart = my_font_restart.render(restart_text, True, (255, 165, 0))
 
background_image_game = pygame.image.load("res/images/Map.png")
background_image_game = pygame.transform.scale(background_image_game, (screen_width, screen_height))
 
game_status = "game"
Figur = Player_mit_Gewehr(screen_width / 2, screen_height / 2)
Figur.spawn_cooldown = 1500
Figur.last_difficulty_time = pygame.time.get_ticks()
Icon = Icons(icon_x, icon_y)
 
player_sprites = pygame.sprite.Group()
player_sprites.add(Figur)
icon_sprites = pygame.sprite.Group()
icon_sprites.add(Icon)
 
enemy_sprites = pygame.sprite.Group()
projectile_sprites = pygame.sprite.Group()
explosion_sprites = pygame.sprite.Group() 
last_spawn_time = pygame.time.get_ticks()
 
sound_schuss = pygame.mixer.Sound("res/sounds/schuss.wav")
sound_switch = pygame.mixer.Sound("res/sounds/weapons_switch.wav")
sound_explosion = pygame.mixer.Sound("res/sounds/explosion.wav")
sound_hurt = pygame.mixer.Sound("res/sounds/hurt.wav")

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
        last_spawn_time = create_enemys(last_spawn_time)
        move_enemys()
        projectile_sprites.update()
        explosion_sprites.update() 
        check_projectile_collisions() 
        game_status = check_collisions(game_status)
        draw_game()
    
    elif game_status == "game_over":
        draw_game_over()
        draw_restart_game()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            last_spawn_time = reset_game()
            game_status = "game"
 
    pygame.display.update()
    clock.tick(60)
 
pygame.quit()