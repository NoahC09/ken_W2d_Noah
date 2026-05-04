import pygame
import math
import random

# 1. Pygame initialisieren
pygame.init()

# --- VOLLBILD-LOGIK ANFANG ---
# Wir holen uns die Info vom aktuellen Monitor
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Wir erstellen das Fenster im FULLSCREEN-Modus
# pygame.DOUBLEBUF sorgt für flüssigere Grafik bei hoher Auflösung
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.DOUBLEBUF)
# --- VOLLBILD-LOGIK ENDE ---

pygame.display.set_caption("SHADOWSTRIKE - Fullscreen Edition")
clock = pygame.time.Clock()

# Schriften (Größe leicht angepasst für große Bildschirme)
font_ui = pygame.font.SysFont("Arial", 28, bold=True)
font_big = pygame.font.SysFont("Arial", int(screen_height/8), bold=True)
font_small = pygame.font.SysFont("Arial", int(screen_height/20), bold=False)

####################################################################################
# Klassen
####################################################################################

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radius = 10
        self.max_radius = 80
        self.image = pygame.Surface((self.max_radius*2, self.max_radius*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 0
        self.duration = 15 

    def update(self):
        self.image.fill((0, 0, 0, 0))
        self.radius += 5
        pygame.draw.circle(self.image, (255, 165, 0, 150), (self.max_radius, self.max_radius), self.radius)
        pygame.draw.circle(self.image, (255, 255, 100, 200), (self.max_radius, self.max_radius), self.radius//2)
        self.timer += 1
        if self.timer >= self.duration:
            self.kill()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, is_grenade=False):
        super().__init__()
        self.is_grenade = is_grenade
        if is_grenade:
            self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (50, 100, 50), (6, 6), 6)
            self.speed = 12
            self.range_timer = 40 
        else:
            self.image = pygame.Surface((12, 4))
            self.image.fill((255, 255, 0))
            self.speed = 22
            self.range_timer = 100 

        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=(x, y))
        
        rad = math.radians(angle)
        self.vx = math.cos(rad) * self.speed
        self.vy = -math.sin(rad) * self.speed

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.range_timer -= 1
        if self.is_grenade and self.range_timer <= 0:
            self.explode()
        elif not screen.get_rect().contains(self.rect):
            self.kill()

    def explode(self):
        explosion_group.add(Explosion(self.rect.centerx, self.rect.centery))
        self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, (40, 40, 40), (20, 20), 18)
        pygame.draw.circle(self.image, (200, 0, 0), (20, 20), 18, 3)
        pygame.draw.circle(self.image, (255, 50, 50), (20, 20), 8)
        
        self.radius = 15 
        self.speed = speed 

        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top": self.rect.center = (random.randint(0, screen_width), -50)
        elif side == "bottom": self.rect.center = (random.randint(0, screen_width), screen_height + 50)
        elif side == "left": self.rect.center = (-50, random.randint(0, screen_height))
        else: self.rect.center = (screen_width + 50, random.randint(0, screen_height))

    def update(self, player_center):
        dx = player_center[0] - self.rect.centerx
        dy = player_center[1] - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.rect.x += (dx / dist) * self.speed
            self.rect.y += (dy / dist) * self.speed

class Player(pygame.sprite.Sprite):                                         
    def __init__(self):                                                   
        super().__init__()
        # Wir skalieren die Figur leicht größer für 4K Bildschirme falls nötig
        p_size = int(screen_height / 12.5) # Dynamische Größe basierend auf Höhe
        self.img_gewehr = pygame.transform.scale(pygame.image.load("res/images/Figur_mit_Gewehr.png").convert_alpha(), (p_size, p_size))
        self.img_granate = pygame.transform.scale(pygame.image.load("res/images/Figur_mit_Granate.png").convert_alpha(), (p_size, p_size))
        
        self.original_image = self.img_gewehr
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(screen_width/2, screen_height/2))
        self.radius = int(p_size * 0.35) 
        
        self.weapon_mode = "rifle"
        self.angle = 0
        self.speed = 5 # Etwas schneller für große Bildschirme
        self.ammo_max = 30
        self.ammo_current = 30
        self.is_reloading = False
        self.reload_timer = 0
        self.shoot_cooldown = 0

    def start_reload(self):
        if not self.is_reloading and self.ammo_current < self.ammo_max:
            self.is_reloading = True
            self.reload_timer = pygame.time.get_ticks()

    def check_reload(self):
        if self.is_reloading:
            if pygame.time.get_ticks() - self.reload_timer > 1500:
                self.ammo_current = self.ammo_max
                self.is_reloading = False

####################################################################################
# Spiel-Funktionen
####################################################################################

def reset_game():
    global player, enemy_group, projectile_group, explosion_group, spawn_timer, speed_update_timer, current_enemy_speed, game_active
    player = Player()
    enemy_group.empty()
    projectile_group.empty()
    explosion_group.empty()
    spawn_timer = pygame.time.get_ticks()
    speed_update_timer = pygame.time.get_ticks()
    current_enemy_speed = 1.2 
    game_active = True

# Setup
background = pygame.transform.scale(pygame.image.load("res/images/Map.png"), (screen_width, screen_height))
player = Player()
enemy_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

spawn_timer = 0
speed_update_timer = 0
current_enemy_speed = 1.2
game_active = True
running = True

####################################################################################
# Main Loop
####################################################################################

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # ESCAPE Taste zum schnellen Beenden (Wichtig im Vollbild!)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if not game_active and event.key == pygame.K_SPACE:
                reset_game()
            if game_active and event.key == pygame.K_r:
                player.start_reload()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_active and event.button == 1:
                reset_game()

    if game_active:
        if current_time - speed_update_timer > 45000:
            current_enemy_speed += 0.3
            speed_update_timer = current_time

        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        
        if keys[pygame.K_1]:
            player.original_image = player.img_gewehr
            player.weapon_mode = "rifle"
        if keys[pygame.K_2]:
            player.original_image = player.img_granate
            player.weapon_mode = "grenade"

        # Schießen
        is_shooting = keys[pygame.K_SPACE] or mouse_buttons[0]
        if is_shooting and not player.is_reloading:
            if player.ammo_current > 0:
                if player.weapon_mode == "rifle":
                    if current_time - player.shoot_cooldown > 150:
                        projectile_group.add(Projectile(player.rect.centerx, player.rect.centery, player.angle, False))
                        player.ammo_current -= 1
                        player.shoot_cooldown = current_time
                elif player.weapon_mode == "grenade":
                    if current_time - player.shoot_cooldown > 1000:
                        projectile_group.add(Projectile(player.rect.centerx, player.rect.centery, player.angle, True))
                        player.ammo_current -= 3
                        player.shoot_cooldown = current_time
            else:
                player.start_reload()

        # Steuerung
        if keys[pygame.K_a]: player.angle += 5
        if keys[pygame.K_d]: player.angle -= 5
        player.image = pygame.transform.rotate(player.original_image, player.angle)
        player.rect = player.image.get_rect(center=player.rect.center)

        rad = math.radians(player.angle)
        if keys[pygame.K_w]:
            player.rect.x += math.cos(rad) * player.speed
            player.rect.y -= math.sin(rad) * player.speed
        if keys[pygame.K_s]:
            player.rect.x -= math.cos(rad) * player.speed
            player.rect.y += math.sin(rad) * player.speed

        # Rand-Check
        if player.rect.left < 0: player.rect.left = 0
        if player.rect.right > screen_width: player.rect.right = screen_width
        if player.rect.top < 0: player.rect.top = 0
        if player.rect.bottom > screen_height: player.rect.bottom = screen_height

        # Updates
        player.check_reload()
        projectile_group.update()
        explosion_group.update()
        enemy_group.update(player.rect.center)

        if current_time - spawn_timer > 1200:
            enemy_group.add(Enemy(current_enemy_speed))
            spawn_timer = current_time

        # Kollisionen
        hits = pygame.sprite.groupcollide(projectile_group, enemy_group, False, False)
        for proj, en_list in hits.items():
            if proj.is_grenade:
                proj.explode()
            else:
                proj.kill()
                for en in en_list: en.kill()

        pygame.sprite.groupcollide(explosion_group, enemy_group, False, True)

        if pygame.sprite.spritecollideany(player, enemy_group, pygame.sprite.collide_circle):
            game_active = False

    # Zeichnen
    screen.blit(background, (0, 0))
    if game_active:
        projectile_group.draw(screen)
        explosion_group.draw(screen)
        enemy_group.draw(screen)
        screen.blit(player.image, player.rect)

        # UI
        ui_ammo = f"AMMO: {max(0, player.ammo_current)}" if not player.is_reloading else "RELOADING..."
        screen.blit(font_ui.render(ui_ammo, True, (255, 255, 255)), (20, screen_height - 60))
        screen.blit(font_ui.render(f"SPEED: {round(current_enemy_speed, 1)}", True, (255, 100, 100)), (20, 20))
        screen.blit(font_ui.render(f"WAFFE: {player.weapon_mode.upper()}", True, (200, 200, 255)), (20, screen_height - 100))
        screen.blit(font_ui.render("ESC zum Beenden", True, (150, 150, 150)), (screen_width - 220, 20))
    else:
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        screen.blit(overlay, (0,0))
        go_surf = font_big.render("GAME OVER", True, (255, 50, 50))
        screen.blit(go_surf, go_surf.get_rect(center=(screen_width/2, screen_height/2 - 50)))
        restart_surf = font_small.render("LEERTASTE zum Neustart | ESC zum Beenden", True, (255, 255, 255))
        screen.blit(restart_surf, restart_surf.get_rect(center=(screen_width/2, screen_height/2 + 70)))

    pygame.display.update()
    clock.tick(60)

pygame.quit()