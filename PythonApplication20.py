
import pygame
import time
import random
import os
from pygame import mixer

pygame.font.init()
mixer.init()




WIDTH, HEIGHT = 940, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle for Gallifrey")
icon = pygame.image.load('doctor.png')
pygame.display.set_icon(icon)

mixer.music.load("whomusic.mp3")
mixer.music.play(-1)


# Load images
DALEK_1 = pygame.image.load(os.path.join( "dalek8.png"))
DALEK_2 = pygame.image.load(os.path.join( "dalek3.png"))
DALEK_3 = pygame.image.load(os.path.join( "dalek5.png"))

# tardis tardis
TARDIS = pygame.image.load(os.path.join("TARDIS5.png"))

# Lasers
LASER_1 = pygame.image.load(os.path.join( "bullet4.png"))
LASER_2 = pygame.image.load(os.path.join( "bullet9.png"))
LASER_3 = pygame.image.load(os.path.join( "bullet6.png"))
YELLOW_LASER = pygame.image.load(os.path.join( "bulletT.png"))

# Background

BG = pygame.transform.scale(pygame.image.load(os.path.join( "1.jpg")), (WIDTH, HEIGHT))


class Laser:
    def __init__ (self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        
        return collide(obj, self)
        
class Ship:
    COLDOWN = 30
    def __init__(self, x, y, health = 10):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0



    def draw(self, window):
      window.blit(self.ship_img, (self.x, self.y))
      for laser in self.lasers:
          laser.draw(window)


    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)


    def cooldown(self):
        if self.cool_down_counter >=self.COLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

        

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
      
      
    def get_width(self):
        return self.ship_img.get_width()
   
    def get_height(self):
        return self.ship_img.get_height()

class Tardis(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = TARDIS
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        
        
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,44,69), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,193,91), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


class Dalek(Ship):
    COLOR_MAP = {
                "1": (DALEK_1, LASER_1),
                "2": (DALEK_2, LASER_2),
                "3": (DALEK_3, LASER_3)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+15, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None  # Check collision



def main():
    run = True        
    FPS = 60
    clock = pygame.time.Clock()
    level = 1
    lives = 12

    daleks = []
    wave_length = 5
    dalek_vel = 1

    tardis_vel = 6
    laser_vel = 6

    tardis= Tardis(400,380)

    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    ship = Ship

    lost = False
    lost_count = 0

    def redraw_window():
     WIN.blit(BG, (0, 0))
     

    # draw text
     lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
     level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

     WIN.blit(lives_label, (10, 10))
     WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
     
     for dalek in daleks:
         dalek.draw(WIN)
          
     tardis.draw(WIN)

     if lost:
         lost_label = lost_font.render("Battle for Gallifrey lost !!!", 1, (255, 255, 255))
         WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 300))
         
     pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or tardis.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
                
                
            else:
                continue
        if len(daleks) == 0:
            explosion_Sound = mixer.Sound('exterminate.mp3')
            explosion_Sound.play()
            level += 1
            wave_length += 2
            for i in range(wave_length):
                dalek = Dalek(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["1", "2", "3"]))
                daleks.append(dalek)
                explosion_Sound = mixer.Sound('exterminate.mp3')
                explosion_Sound.play()
        for event in pygame.event.get():
            if event.type ==pygame. QUIT:
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and tardis.x - tardis_vel > 0: # left
            tardis.x -= tardis_vel
        if keys[pygame.K_d] and tardis.x + tardis_vel + tardis.get_width() < WIDTH: # right
            tardis.x += tardis_vel
        if keys[pygame.K_w] and tardis.y - tardis_vel > 0: # up
            tardis.y -= tardis_vel
        if keys[pygame.K_s] and tardis.y + tardis_vel + tardis.get_height() + 15 < HEIGHT: # down
            tardis.y += tardis_vel
        if keys[pygame.K_SPACE]:
            tardis.shoot()
            laser_Sound = mixer.Sound('laser.wav')
            laser_Sound.play()
              
       

        for dalek in  daleks[:]:
            dalek.move(dalek_vel)
            dalek.move_lasers(laser_vel, tardis)

            if random.randrange(0, 2*60 )==1:
                dalek.shoot()

            if collide(dalek, tardis):
                tardis.health -= 10              
                daleks.remove(dalek)

            elif dalek.y + dalek.get_height() > HEIGHT:
                lives -= 1
                daleks.remove(dalek)

        tardis.move_lasers(-laser_vel, daleks)

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

           
        
main_menu()
   
    














































