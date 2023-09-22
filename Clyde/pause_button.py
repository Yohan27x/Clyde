# import official modules
import random, sys, csv

from pygame import mixer

# import the different files we wrote
from button import *
from pixel_text import *
from objects_group import *
from Images import *
from Musics import *

pygame.init()
mixer.init() 

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

FPS = 60
clock = pygame.time.Clock()

flags = pygame.SCALED
game_icon = pygame.image.load('Images/game_window_icon/icon.png')
pygame.display.set_icon(game_icon)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, vsync=1)
pygame.display.set_caption('Clyde')

menu_display = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
pause_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
pause_surface.fill((0,0,0))
pause_surface.set_alpha(85)

ROWS = 60
COLS = 300
TILE_SIZE = SCREEN_HEIGHT // ROWS + 30

TILE_TYPES = 43

LEVEL = 7
MAX_LEVELS = 7

GRAVITY = 0.75
true_scroll = [0, 0]
screen_shake = 0
pause_game = False

start_game = False  # trigger
start_intro = False
game_end = True
type_of_game_end = None

moving_left = False
moving_right = False

shoot = False
shoot_cooldown = 0

attack = False
attack_cooldown = 30

save_robot = False
save_robot_cooldown = 50

dash = False

wake_up = True
wake_up_cpt = 0
wake_up_shake_cpt = 0

cant_play = False

shoot_up = False
shoot_front = False

trigger_anim = True

player_pos_x = 0
player_pos_y = 0


num_of_robots_saved = 0
player_health = 1
player_ammo = 0


# images variables --------- #

blit_button_once = True
blit_ibutton_cd = 20
ibutton_index = 0

first_game_layer = False
menu_on = True

# define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
GREEN = (24, 233, 75)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
PURPLE = (34,32,52)



def draw_bg():
    screen.fill((0, 0, 2))

    width = last_layer.get_width()

    for x in range(25):
        screen.blit(last_layer, ((x * width) - tile_bg_scroll[0] * 0.3, 0))
        screen.blit(second_layer,((x * width) - tile_bg_scroll[0] * 0.3, 0))
        screen.blit(first_layer, ((x * width) - tile_bg_scroll[0] * 0.6, 0))


# ---------------------------------- #


# Fade systems -------------- #

def draw_copy_menu():

    #draw menu animated by blitting severals images ou avec le frame index donc liste donc cooldown --> meilleure solution
    # TODO : changez et mettre nos bails
        menu_display.blit(menu_bg, (0, 0))
        menu_display.blit(title_img,(250,100))

        menu_display.blit(pygame.transform.scale(image_play_button_click, (image_play_button_click.get_width() * 5, image_play_button_mouse_on.get_height() * 5)),(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        menu_display.blit(pygame.transform.scale(image_exit_button_unclick, (image_exit_button_unclick.get_width() * 5, image_exit_button_unclick.get_height() * 5)),(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70))
        screen.blit(menu_display, (0, 0))


def draw_menu_surface():
    draw_copy_menu()


def draw_copy_game(player_pos_x, player_pos_y):
    draw_bg()

    # draw world map
    world.draw()

    screen.blit(health_icon_images[abs(player.health - 5)], (15, 15))

    # -------------------------------------------------------------

    # blit la tète verte des robots sauvés
    screen.blit(img_robot_saved, (15, 56))

    # blit le bon nombre de robot sauvé
    num_list[player.num_saved].draw()

    # blit le slash
    screen.blit(slash, (39, 70))

    # blit le 12 ou autre a définir
    Fontt_num_max_robot_saved.draw()

    if LEVEL <= MAX_LEVELS:
        player.update(0)

    player.draw()

    player.rect.x = player_pos_x
    player.rect.y = player_pos_y


    for enemy in enemy_group:
        enemy.ai()
        enemy.update()
        enemy.draw()
        enemy.check_state()

    for roof_enemy in roof_ennemy_group:
        roof_enemy.attack()
        roof_enemy.update()
        roof_enemy.check_state()

    bullet_group.update()

    grenade_group.update()

    explosion_group.update()


    for bubble in speech_bubble_group:
        bubble.update()

    for item in health_item_group:
        item.update()

    for item in ammo_item_group:
        item.update()


    for exit in exit_group:
        exit.update()

    for decor in decors_group:
        decor.update()


def draw_game_surface():
    draw_copy_game(player_pos_x, player_pos_y)


def copy_good_end_surface(): # fail c'est thanks for playing, pas good end
    screen.fill((0, 0, 0))
    Fontt_shade_good.draw()
    Fontt_high_good.draw()

    Fontt_shade_end2.draw()
    Fontt_high_end2.draw()

    Fontt_shade_morethan.draw()
    Fontt_high_morethan.draw()




def draw_good_end_surface():
    copy_good_end_surface()



def copy_bad_end_surface(): #
    screen.fill((0,0,0))

    Fontt_shade_bad.draw()
    Fontt_high_bad.draw()

    Fontt_shade_end.draw()
    Fontt_high_end.draw()

    Fontt_shade_lessthan.draw()
    Fontt_high_lessthan.draw()



def draw_bad_end_surface():
    copy_bad_end_surface()



def copy_credits_surface(): # thanks for playing mais pas grave
    screen.fill((0, 0, 0))
    Fontt_shade_credits.draw()
    Fontt_high_credits.draw()

    Fontt_shade_adrien.draw()
    Fontt_high_adrien.draw()

    Fontt_shade_yohan.draw()
    Fontt_high_yohan.draw()

    #Fontt_shade_liz.draw()
    #Fontt_high_liz.draw()

    Fontt_shade_others.draw()
    Fontt_high_others.draw()

    #Fontt_shade_ytb.draw()
    #Fontt_high_ytb.draw()



def draw_credits_surface():
    copy_credits_surface()



def copy_thanks_surface():
    screen.fill((0, 0, 0))
    Fontt_shade_thanks.draw()
    Fontt_high_thanks.draw()

    Fontt_shade_for.draw()
    Fontt_high_for.draw()

    Fontt_shade_playing.draw()
    Fontt_high_playing.draw()


def draw_thanks_surface():
    copy_thanks_surface()


def fade(window,fade_what): # menu_display , MENU / screen , GAME
    fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)) # on crée une surface de la taille du screen principal
    fade.fill((0,0,0)) # on la remplit de noir

    for alpha in range(0, 255, 2):

        if alpha == 253:
            break



        fade.set_alpha(alpha) # on l'a met transparente de base et on l'a fait devenir de moins en moins transparent --> retour a sa couleur initiale
        #toutes les surfaces que nous allons être amené a fade tout au long du jeu
        if fade_what == 'MENU': # si on est sur le menu
            draw_menu_surface() # alors on veut le redessiner
        elif fade_what == 'GAME': # si on est sur le jeu
            draw_game_surface() # alors on veut le redessiner
        elif fade_what == 'GOOD END': # ...
            draw_good_end_surface()
        elif fade_what == 'BAD END':
            draw_bad_end_surface()
        elif fade_what == 'CREDITS ':
           draw_credits_surface()
        elif fade_what == 'THANKS FOR PLAYING ':
            draw_thanks_surface()

        # pas de thanks for playing car il est en dernier et on ne veut pas le fade car le jeu s'arrète

        window.blit(fade, (0,0)) # on blit sur le screen la surface fade

        if fade_what == 'MENU':
            screen.blit(window,(0,0)) # on blit sur le screen principal le menu_display qui contient 2 surfaces : le menu dessiné et la surface fade

        pygame.display.update() # on update le display

        #if fade_what == 'MENU':
            #window.set_alpha(0) # dès qu'on a finit, on met transparent la surface menu_display pour ne plus la voir



def unfade(unfade_what):

    # surface pour le fade_out
    unfade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    unfade.fill((0,0,0))


    for alpha in range(255, 0, -1,):
        unfade.set_alpha(alpha - 4) # devient de plus en plus transparent


        if unfade_what == 'MENU':
            draw_game_surface()

        elif unfade_what == 'GAME' and game_end == True:
            if type_of_game_end == 'GOOD':
                draw_good_end_surface()
            else:
                draw_bad_end_surface()

        elif unfade_what == 'GAME'and game_end == False:
            draw_game_surface()

        elif unfade_what == 'GOOD END' or unfade_what == 'BAD END':
            draw_thanks_surface()

        elif unfade_what == 'THANKS FOR PLAYING':
            draw_credits_surface()


        screen.blit(unfade, (0, 0))
        pygame.display.update()

# ------------------------------------------------------------- #


# ENEMY AND PLAYER CLASS -------------------- #


class Enemy(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)


        self.char_type = char_type

        self.speed = speed
        self.health = 4
        self.max_health = self.health

        self.direction = 1
        self.vel_y = 0
        self.flip = False

        self.animation_list = []
        animation_types = ['Idle', 'Run', 'Stun', 'Death', 'Hurt', 'Dance', 'Save', 'Attack']
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load all images for the players
        self.animation_list = (animation(self.char_type, scale, animation_types))
        self.image = self.animation_list[self.action][self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


        # ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 15, 5)
        self.idling = False
        self.idling_counter = 0

        self.alive = True

        self.stun = False
        self.stun_timer = 0
        self.stun_anim = True
        self.stun_once = True

        self.hurt = False
        self.hurt_cooldown = 0

        self.ready_to_attack = False
        self.attack_cooldown = 0
        self.attack_once = False
        self.speed_increase = False

        self.save_key_collide = False
        self.save = False
        self.save_duration = 0

        self.max_stun_cooldown = random.randint(180,230)

        self.count = 0

        self.trigger_anim = True

        self.collision_rect = pygame.Rect(0, 0, 34, 94)
        self.explosion_scale = pygame.Rect(0, 0, 115, 94)

        self.stun_sound = 1






    def move(self, moving_left, moving_right):
        # reset movement variables
        dx = 0
        dy = 0

        # assign movement variables if moving left or right
        if moving_left:
            dx -= self.speed
            self.flip = True
            self.direction = -1

        if moving_right:
            dx += self.speed
            self.flip = False
            self.direction = 1

        # apply gravity
        self.vel_y += GRAVITY



        if self.vel_y > 5:
            self.vel_y = 5

        dy += self.vel_y



        # check for collision
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                if tile[1].colliderect(self.collision_rect.x + dx, self.collision_rect.y, self.collision_rect.width,
                                       self.collision_rect.height):
                    dx = 0


            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if tile[1].colliderect(self.collision_rect.x, self.collision_rect.y + dy, self.collision_rect.width,
                                       self.collision_rect.height):
                    self.dont_collide = False
                    if self.vel_y < 0:  # donc quand il saute
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top  # on compense pour qu'il se cogne avec le tile
                        # check if above the ground
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False
                        dy = tile[1].top - self.rect.bottom



        # update rectangle position

        dx = 0 if pause_game == True else dx

        self.rect.x += dx
        self.rect.y += dy

        # on place le rect de collision rapport au rect de l'image de clyde
        self.collision_rect.midbottom = self.rect.midbottom
        self.explosion_scale.midbottom = self.rect.midbottom



    def attack(self):

        self.image = self.animation_list[7][3]  # = la dernière frame de l'animation de l'attaque
        #self.image = pygame.transform.flip(self.image, self.flip, False)
        self.mask = pygame.mask.from_surface(self.image)


        player.image = player.animation_list[0][0]
        player.image = pygame.transform.flip(player.image, player.flip, False)
        player.mask = pygame.mask.from_surface(self.image)

        if pygame.sprite.collide_rect(self, player):
            if pygame.sprite.collide_mask(self, player):
                player.hurt = True
                self.attack_once = False

    def update(self):

        if self.ready_to_attack == True and self.speed_increase == False:
            self.speed += 1
            self.speed_increase = True

        if pause_game == False:
            self.update_animation()

        self.check_stun()

        #-------------- attack part ------------------
        if self.action == 7 and self.frame_index == 3 and self.trigger_anim is True:
            self.attack()
            self.trigger_anim = False
            self.attacking = False
            self.count += 1



    def check_stun(self):

        if self.health <= 0:
            self.health = 0
            self.speed = 0


            if self.stun_once == True:
                self.stun = True
                self.stun_once = False


    def check_state(self):

        if self.stun == True and self.stun_anim == True:
            self.update_action(2)
            self.stun_anim = False



        # on augmente le timer chaque frame


        if self.alive == True:
            if self.stun == True:
                if self.save == False:
                        if self.stun_timer < self.max_stun_cooldown:  # on augmente le timer si il est inférieur a la durée maximum
                            self.stun_timer += 1




        # il explose si le timer est complet

        if self.alive == True:
            if self.stun == True:
                if self.save == False:
                    if self.stun_timer == self.max_stun_cooldown:  # 240 = 4 secondes / si il n'est pa sauvé au bout de 4 secondes
                        if self.stun_sound == 0:
                            stun_fx.stop()
                            self.stun_sound = 1
                            self.alive = False
                            self.stun_timer = 0  # on stop le stun timer
                            self.update_action(3)  # alors il explose ( ici, sa tete tombe )
                            explosion_fx.play()
                        if self.explosion_scale.colliderect(player.collision_rect):
                            player.hurt = True


        # si le robot est en période de stun
        if self.alive == True:
            if self.stun == True:
                if 0 <= self.stun_timer <= self.max_stun_cooldown : # si le stun timer est entre 0 et 240
                    if self.stun_sound == 1: # initialisé a 1 dans le init
                        stun_fx.play(-1)
                        self.stun_sound = 0 # pour ne pas repasse dans le if
                    if self.save_key_collide == True: #si la clef a touché le robot ennemi :
                        if self.stun_sound == 0: # si le son de stun a déja était joué
                            stun_fx.stop()
                            save_collide_fx.play()
                            self.stun_sound = 1
                            self.save = True
                            self.stun_timer = 400
                            self.update_action(6) # alors on met l'animation de save


        if self.alive == True:
            if self.save == True:
                if self.save_duration == 72: #si toutes les frames de l'anim save sont passés
                    self.update_action(5) # alors on met l'anim de dance
                    self.save_duration = 0
                    self.save = False


        if self.alive == True:
            if self.save == True:
                if self.save_duration < 72:
                    self.save_duration += 1


        #hurt part

        if self.hurt_cooldown < 20 and self.hurt == True:
            self.hurt_cooldown += 1

        if self.hurt_cooldown == 20:

            self.hurt = False
            self.hurt_cooldown = 0

        if self.hurt_cooldown == 1:
            self.health -= 1
            #print(self.health)
            hurt_robot_ennemyfx.play()
            self.update_action(4)

            if self.stun == True:
                self.update_action(2)

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100

        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]

        # check if enough time has passed since the last update
        if self.action == 0:  # IDLE
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN + 130:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1
        elif self.action == 1:  # RUN
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN - 7:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1
        elif self.action == 2:  # JUMP
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN + 20:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1

        elif self.action == 4:  # Hurt
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN :
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1


        elif self.action == 6:  # JUMP
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN + 70:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1

        elif self.action == 7:  # JUMP
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN + 10:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1

        elif pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:  # cooldown
            self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
            self.frame_index += 1

        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):  # si l'index dépasse ou est égale a la dernière frame de la liste
            if self.action == 3 or self.action == 4 or self.action == 5 or self.action == 6:  # anim qu'on ne veut pas répéter
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:  # si autre, on répète en rememttant le frame index a 0
                self.frame_index = 0

    def ai(self):
                if self.stun == False and player.alive and pause_game == False:

                    # check for idle stuff
                    if self.idling == False and random.randint(1, 200) == 1 and self.hurt == False and self.ready_to_attack == False:
                        self.idling = True
                        self.update_action(0)
                        self.idling_counter = 50



                    # si vision collide

                    # check if the ai is near the player


                    if self.vision.colliderect(player.collision_rect) and self.ready_to_attack == True and self.hurt == False : # and self.hurt == True # remplacer par collide rect ?
                        #self.attack_once = True

                        self.attack_cooldown += 1

                        if self.attack_cooldown == 5 :
                            self.attack_cooldown = 0

                            self.update_action(7)
                            self.trigger_anim = True
                            #pygame.draw.rect(screen,RED, (self.vision.x - tile_bg_scroll[0], self.vision.y - tile_bg_scroll[1], self.vision.width, self.vision.height))



                    else:
                        if self.idling == False and self.hurt == False:
                            if self.direction == 1:
                                ai_moving_right = True
                            else:
                                ai_moving_right = False

                            if self.hurt_cooldown == 0:
                                ai_moving_left = not ai_moving_right
                                self.move(ai_moving_left, ai_moving_right)
                                self.update_action(1)  # pour qu'ils courent
                                self.move_counter += 1

                            # update ai vision as the enemy move
                            self.vision.center = ((self.collision_rect.centerx + 30 * self.direction), self.collision_rect.centery)
                            #pygame.draw.rect(screen,RED, (self.vision.x - tile_bg_scroll[0], self.vision.y - tile_bg_scroll[1], self.vision.width, self.vision.height))

                            #if self.ready_to_attack == False:
                            if self.move_counter > 30 and self.ready_to_attack == False:
                                self.direction *= -1
                                self.move_counter *= -1

                            if self.ready_to_attack:
                                if player.collision_rect.centerx + 15 < self.collision_rect.centerx:
                                    self.direction = -1
                                else:
                                    self.direction = 1

                        else:
                            self.idling_counter -= 1
                            if self.idling_counter <= 0:
                                self.idling = False



    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),(self.rect.x - tile_bg_scroll[0], self.rect.y - tile_bg_scroll[1]))
        #pygame.draw.rect(screen, RED, (self.rect.x - true_scroll[0], self.rect.y - true_scroll[1], self.image.get_width(), self.image.get_height()), 2)
        #pygame.draw.rect(screen, PINK, (self.collision_rect.x - true_scroll[0], self.collision_rect.y - true_scroll[1], self.collision_rect.width,self.collision_rect.height), 2)
        #pygame.draw.rect(screen, GREEN, (self.explosion_scale.x - true_scroll[0], self.explosion_scale.y - true_scroll[1], self.explosion_scale.width,self.collision_rect.height), 2)



class Clyde(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, health):
        pygame.sprite.Sprite.__init__(self)

        self.alive = True
        self.char_type = char_type

        self.speed = speed
        self.health = health
        self.max_health = self.health

        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False

        self.animation_list = []
        animation_types = ['Idle', 'Run', 'Jump', 'Death', 'Attack', 'Save', 'Hurt', 'Shoot Pos', 'Dash', 'WakeUp', 'Shoot Front', 'Shoot Up','Aim Top']
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # load all images for the players
        self.animation_list = (animation(self.char_type, scale, animation_types))
        self.image = self.animation_list[self.action][self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.save_hit = pygame.Rect(0, 0, 30, 20)
        self.attack_hit = pygame.Rect(0,0,35, 15)

        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0

        self.hurt = False

        # ai specific variables

        self.collision_rect = pygame.Rect(0, 0, 34, 94)

        self.hurt_cooldown = 0

        self.dash_cpt_left = 0
        self.dash_cpt_right = 0

        self.ready_to_shoot_front = False
        self.ready_to_shoot_up = False
        self.attack_once = False
        self.lock_top = False
        self.num_saved = 0

        self.vel_cpt = 0

        self.death = False
        self.death_sound = 1



    def health_ammo_update(self, health, ammo):

        health = self.health
        ammo = self.ammo

        return health, ammo


    def update(self, screen_shake):

        if pause_game == False:
            self.update_animation()


        self.check_alive()


        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


        if self.alive:
            if self.hurt == True:
                screen_shake = 2
                self.hurt_cooldown += 1

            if self.hurt_cooldown == 20: # faire varier la valeur pour augmenter la durée de l'animation de hurt
                self.hurt_cooldown = 0
                self.hurt = False

            if self.hurt_cooldown == 1:
                self.health -= 1
                hurt_clydefx.play()

        return screen_shake




    def attack(self):


        #for robot in enemy_group:
            #robot.image = robot.animation_list[0][0]
            #robot.image = pygame.transform.flip(robot.image, robot.flip, False)
            #robot.mask = pygame.mask.from_surface(robot.image)

        self.temp_image = self.animation_list[4][3]  # = la dernière frame de l'animation de l'attaque
        self.temp_image = pygame.transform.flip(self.temp_image, self.flip, False)
        self.mask = pygame.mask.from_surface(self.temp_image)


        for robot_enemy in enemy_group:
            if pygame.sprite.collide_rect(self, robot_enemy):
                if pygame.sprite.collide_mask(self, robot_enemy) and self.attack_hit.colliderect(robot_enemy.collision_rect):
                    if robot_enemy.health > 0:
                        robot_enemy.ready_to_attack = True
                        if robot_enemy.stun == False:
                            robot_enemy.hurt = True


    def save(self):

        #for robot in enemy_group:
            #robot.image = pygame.transform.flip(robot.image, robot.flip, False)
            #robot.mask = pygame.mask.from_surface(robot.image)

        self.temp_image = self.animation_list[5][7]
        self.temp_image = pygame.transform.flip(self.temp_image, self.flip, False)
        self.mask = pygame.mask.from_surface(self.temp_image)

        for robot_enemy in enemy_group:
            if robot_enemy.stun_timer >= 0 and robot_enemy.stun_timer <= 300 and robot_enemy.stun == True:
                if pygame.sprite.collide_rect(self, robot_enemy):
                    if pygame.sprite.collide_mask(self, robot_enemy) and self.save_hit.colliderect(robot_enemy.collision_rect): # and collision rectangle vert bonne directiono
                        self.num_saved += 1
                        robot_enemy.save_key_collide = True


    def collide_exit(self, num_robot_saved):
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True
            num_robot_saved = self.num_saved

        return num_robot_saved, level_complete

    def move(self, moving_left, moving_right, dash, wake_up):

        # reset movement variables
        dx = 0
        dy = 0

        # assign movement variables if moving left or right

        if self.dash_cpt_right > 0:
            moving_left = False

        if self.dash_cpt_left > 0:
            moving_right = False

        if moving_left:
            if self.action == 4 or self.action == 5 or self.action == 10 or self.action == 11:# toutes les animations où je ne veux pas que clyde puisse bouger -> animations d'actions
                dx = 0
            else:
                dx -= self.speed
            if pause_game == False:
                self.flip = True
                self.direction = -1

        if moving_right:
            if self.action == 4 or self.action == 5 or self.action == 10 or self.action == 11:
                dx = 0
            else:
                dx += self.speed

            if pause_game == False:
                self.flip = False
                self.direction = 1

        if self.direction == -1 or moving_left :
            if dash:
                dx -= (self.speed + 2)
                self.dash_cpt_left += 1
                if moving_left:
                    dx += self.speed # contrebalance de la vitesse si l'utilisateur avance en meme temps qu'il dash

        if self.direction == 1 or moving_right :
            if dash:
                dx += self.speed + 2
                self.dash_cpt_right += 1
                if moving_right:
                    dx -= self.speed # contrebalance de la vitesse si l'utilisateur avance en meme temps qu'il dash





        if self.dash_cpt_left == 20: # la durée maximal du dash et de son animation par la même occasion
            self.dash_cpt_left = 0
            dash = False

        elif self.dash_cpt_right == 20:
            self.dash_cpt_right = 0
            dash = False


        if self.dash_cpt_right == 1 or self.dash_cpt_left == 1:
            dash_fx.play()




        if pause_game == False:

            # jump
            if self.jump == True and self.in_air == False:
                self.vel_y = -12
                self.vel_cpt = 0
                self.jump = False
                self.in_air = True
                jump_fx.play()



            # apply gravity
            self.vel_y += GRAVITY



            if self.vel_y > 0 and self.in_air == True:
                if self.vel_y > 7:
                    self.vel_y = 7
                else:
                    self.vel_cpt += 0.0005
                    self.vel_y += self.vel_cpt

            if self.action != 4 and self.action != 5 and self.action != 10 and self.action != 11: # toutes actions autre que celles ou je ne veux pas bouger
                dy += self.vel_y


            if self.in_air == True: # faire un saut vers l'avant accéléré
                if dx >= 0:
                    dx /= 0.7
                if dx <= 0:
                    dx *= 1.4

        # check for collision
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                if tile[1].colliderect(self.collision_rect.x + dx, self.collision_rect.y, self.collision_rect.width,
                                       self.collision_rect.height):
                    dx = 0

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if tile[1].colliderect(self.collision_rect.x, self.collision_rect.y + dy, self.collision_rect.width,
                                       self.collision_rect.height):
                    if self.vel_y < 0:  # donc quand il saute
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top  # on compense pour qu'il se cogne avec le tile
                        # check if above the ground
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False
                        dy = tile[1].top - self.rect.bottom

        # check collision with water


        # check collision with exit

        if pause_game == False: # pour que la caméra arrète de bouger quand le jeu est en pause
            if wake_up == False:
                true_scroll[0] += (player.rect.x - true_scroll[0] - (400 - player.image.get_width())) / 10  # jouez avec 400 ou 320 pour monter / descendre / droite / gauche caméra
                true_scroll[1] += (player.rect.y - true_scroll[1] - (450 - player.image.get_height())) / 15
            else:
                true_scroll[0] += (player.rect.x - true_scroll[0] - (300 - player.image.get_width())) / 10
                true_scroll[1] += (player.rect.y - true_scroll[1] - (480 - player.image.get_height())) / 15



        # on soustrait la postion du joueur a la position du scroll --> player.rect.x - true_scroll[0]
        # on ajoute une fraction du scroll pour créer un décalage -- > /15
        # update rectangle position

        dx = 0 if pause_game == True else dx


        dy = 0 if self.alive == False and dy != 0 else dy # pour pas qu'il continue a tomber si il meurt durant le wall jump

        self.save_hit.center = (self.collision_rect.centerx + 40 * self.direction, self.collision_rect.centery)
        self.attack_hit.center = (self.collision_rect.centerx + 25 * self.direction, self.collision_rect.centery)


        self.rect.x += dx
        self.rect.y += dy

        # on place le rect de collision rapport au rect de l'image de clyde
        self.collision_rect.midbottom = self.rect.midbottom

        return true_scroll, dash

    def shoot(self):
        if (player.ready_to_shoot_up or player.ready_to_shoot_front ) and self.shoot_cooldown == 0 and self.ammo > 0:
            shoot_fx.play()
            self.shoot_cooldown = 20
            player.attack_once = True

            if player.ready_to_shoot_up:
                player.ready_to_shoot_up = False
                bullet = Bullet(player.rect.centerx + 3, player.rect.centery - 30, player.direction, 1, 'top')

            else:
                player.ready_to_shoot_front = False
                bullet = Bullet(player.collision_rect.centerx + (0.75 * player.collision_rect.size[0] * player.direction),player.rect.centery, player.direction, 1, 'front')

            bullet_group.add(bullet)
            player.ammo -= 1


    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100

        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]

        # check if enough time has passed since the last update
        if self.action == 0:  # IDLE
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN + 130:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1

        elif self.action == 1:  # RUN
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN - 7:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1

        elif self.action == 2:  # JUMP
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN - 52:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1

        elif self.action == 3:  # JUMP
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN + 20:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1

        elif self.action == 4:  # JUMP
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN - 15: # gérer la vitese de l'animaiton de l'attaque
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1

        elif self.action == 5:  # JUMP
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN - 12:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1

        elif self.action == 6:  # Hurt
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN + 50:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1

        elif self.action == 7:  # Hurt
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN - 5:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1

        elif self.action == 8:  # Hurt
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN - 60:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1

        elif self.action == 9:  # Hurt
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN + 60:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1

        elif self.action == 10:  # Hurt
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN + 20:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1

        elif self.action == 11:  # Hurt
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN + 20:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1

        elif pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN :  # cooldown
            self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
            self.frame_index += 1

        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):  # si l'index dépasse ou est égale a la dernière frame de la liste
            if self.action == 3 or self.action == 2 or self.action == 4 or self.action == 5 or self.action == 6 or self.action == 7 or self.action == 8 or self.action == 9 or self.action == 10:  # si c'est l'animation de mort, on ne veut pas répéter l'animation
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:  # si autre, on répète en remettant le frame index a 0
                self.frame_index = 0



    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health == 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)  # death animationdd
            self.death = True
            if self.death_sound == 1:
                explosion_fx.play()
                self.death_sound = 0


        if self.death == True:
            self.death = False




    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),(self.rect.x - true_scroll[0], self.rect.y - true_scroll[1]))
        #pygame.draw.rect(screen,RED,(self.rect.x - true_scroll[0], self.rect.y - true_scroll[1], self.image.get_width(), self.image.get_height()),2)
        #pygame.draw.rect(screen, PINK, (self.collision_rect.x - true_scroll[0], self.collision_rect.y - true_scroll[1], self.collision_rect.width,self.collision_rect.height), 2)
        #pygame.draw.rect(screen,GREEN, (self.save_hit.x - true_scroll[0], self.save_hit.y - true_scroll[1], self.save_hit.width, self.save_hit.height),1)
        #pygame.draw.rect(screen, PINK, (self.attack_hit.x - true_scroll[0], self.attack_hit.y - true_scroll[1], self.attack_hit.width, self.attack_hit.height),1)



# ---------------------------------------------------------------------------

# World class to draw on the game window the level we did with the level editor ------------------  #

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):  # data = world_data

        self.level_length = len(data[0])  # prend la 1ere ligne pour savoir le nombre de colonne de la liste, donc la longueur
        # iterate throgh each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)

                    if tile >= 0 and tile <= 26 or tile == 39 or tile == 41:
                        self.obstacle_list.append(tile_data)

                    elif tile == 27:
                        decor = Decors(img, x * TILE_SIZE, y * TILE_SIZE)
                        decors_group.add(decor)

                    elif 28 <= tile <= 29 or tile == 40:  # create player
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)

                    elif tile == 30:  # create player
                        if LEVEL > 1:
                            player = Clyde('player', x * TILE_SIZE, y * TILE_SIZE, 1.8, 5, player_ammo, player_health)
                        else:
                            player = Clyde('player', x * TILE_SIZE, y * TILE_SIZE, 1.8, 5, 10, 5)
                        player.num_saved = num_of_robots_saved
                        player_group.add(player)

                    elif tile == 31:
                        enemy = Enemy('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.8, 3)
                        enemy_group.add(enemy)

                    elif tile == 32:
                        space = 1
                        for i in range(num_of_robots_saved):
                            enemy_saved = Enemy('enemy', (x * TILE_SIZE) + space * 65, y * TILE_SIZE + 63, 1.8, 3)
                            enemy_saved.flip = True
                            enemy_saved.direction = -1
                            enemy_saved.save = True
                            enemy_saved.action = 6
                            enemy_saved.health = 0
                            enemy_saved.stun_timer = 400
                            enemy_group.add(enemy_saved)
                            space += 1

                    elif tile == 33:
                        roof_ennemy = Roof_enemy("roof enemy", x * TILE_SIZE,  y * TILE_SIZE + 18, 3)
                        roof_ennemy_group.add(roof_ennemy)

                    elif 34 <= tile <= 36 or tile == 42 or tile == 43:
                        bubble_speech = Speech_bubble(x * TILE_SIZE,  y * TILE_SIZE , img )
                        speech_bubble_group.add(bubble_speech)

                    elif tile == 37:
                        health_head = Health_item(x * TILE_SIZE,  y * TILE_SIZE + 10)
                        health_item_group.add(health_head)

                    elif tile == 38:
                        ammo_item = Ammo_item(x * TILE_SIZE, y * TILE_SIZE + 10)
                        ammo_item_group.add(ammo_item)

        return player


    def draw(self):  # dessine tous les tiles avec lesquelles ont peu se cogner, les autres seronts dessiné à l'aide de leur Classes et de leurs méthod .draw(screen)
        for tile in self.obstacle_list:
            screen.blit(tile[0], (tile[1][0] - tile_bg_scroll[0], tile[1][1] - tile_bg_scroll[1]))


# ---------------------------------------------------------------------- #


# Object's classe ----------------------- #



class Decors(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):

        if self.rect.colliderect(player.collision_rect):
            player.health = 0

        screen.blit(self.image, (self.rect.x - tile_bg_scroll[0], self.rect.y - tile_bg_scroll[1]))



class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):

        screen.blit(self.image, (self.rect.x - tile_bg_scroll[0], self.rect.y - tile_bg_scroll[1]))



class Speech_bubble(pygame.sprite.Sprite):
    def __init__(self, x, y,  img ):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image = pygame.transform.scale(self.image,(self.image.get_width() * 2, self.image.get_height() * 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self):

        screen.blit(self.image,(self.rect.x - tile_bg_scroll[0], self.rect.y - tile_bg_scroll[1]))



class Roof_enemy(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y,scale,):
        pygame.sprite.Sprite.__init__(self)

        self.char_type = char_type
        self.health = 3
        self.max_health = self.health

        self.animation_list = []
        animation_types = ['Shoot', 'Hurt', 'Death']
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load all images for the players
        self.animation_list = (animation(self.char_type, scale, animation_types))
        self.image = self.animation_list[self.action][self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.alive = True
        self.hurt = False
        self.hurt_cooldown = 0
        self.shoot_cooldown = 80 # 80 pour empecher de lancer plusieurs projectile lorsqu'on met le jeu en pause


    def attack(self):

        if self.action == 0 and self.frame_index == 5 and self.shoot_cooldown == 80 and pause_game == False:
            grenade = Grenade(self.rect.centerx, self.rect.bottom - 15)
            grenade_group.add(grenade)
            self.shoot = False
            self.shoot_cooldown = 0

    def check_state(self):


        if self.alive == True:

            if self.shoot_cooldown < 80:
                self.shoot_cooldown += 1

            if self.health == 0:
                self.alive = False

            if self.alive == False:
                roof_die_fx.play()

            if self.hurt == True:
                self.hurt_cooldown += 1

            if self.hurt_cooldown == 20:  # faire varier la valeur pour augmenter la durée de l'animation de hurt
                self.hurt_cooldown = 0
                self.hurt = False

            if self.hurt_cooldown == 1:
                self.health -= 1
                #print(self.health)
                hurt_top_ennemyfx.play()


    def update(self):
        if pause_game == False :
                self.update_animation()

        if self.alive == False:
            self.update_action(2)
        elif self.hurt == True:
            self.update_action(1)
        else:
            self.update_action(0)


        screen.blit(self.image,(self.rect.x - tile_bg_scroll[0], self.rect.y - tile_bg_scroll[1]))


    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100

        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]

        # check if enough time has passed since the last update
        if self.action == 0:  # Turn
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN + 50:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1
        elif self.action == 1:  # Hurt
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN + 15:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1
        elif self.action == 2:  # Death
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN :
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):  # si l'index dépasse ou est égale a la dernière frame de la liste
            if self.action == 1 or self.action == 2:  # anim qu'on ne veut pas répéter
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:  # si autre, on répète en rememttant le frame index a 0
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()




class Health_item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = img_health_item
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.go_down = 10
        self.go_high = 0
        self.cpt_move = 0

    def update(self):

        if pause_game == False:

                if self.cpt_move < 2:
                    self.cpt_move += 1


                if self.go_high < 10 and self.go_down == 10 and self.cpt_move == 2:
                    self.rect.y -= 1
                    self.go_high += 1

                if self.go_high == 10 and self.cpt_move == 2:
                    self.rect.y += 1
                    self.go_down -= 1

                if self.go_down == 0:
                    self.go_high = 0
                    self.go_down = 10

                if self.cpt_move == 2:
                    self.cpt_move = 0


                if pygame.sprite.collide_rect(self, player):
                    if pygame.sprite.collide_mask(self, player):
                        if player.health < 5:
                            collide_objects_fx.play()
                            player.health += 1
                        self.kill()

        screen.blit(self.image, ((self.rect.x + 7) - tile_bg_scroll[0], self.rect.y - tile_bg_scroll[1]))


class Ammo_item(pygame.sprite.Sprite):
    def __init__(self, x, y, ):
        pygame.sprite.Sprite.__init__(self)

        self.image = img_ammo_item
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.go_down = 10
        self.go_high = 0
        self.cpt_move = 0

    def update(self):

        if pause_game == False:

                if self.cpt_move < 2:
                    self.cpt_move += 1


                if self.go_high < 10 and self.go_down == 10 and self.cpt_move == 2:
                    self.rect.y -= 1
                    self.go_high += 1

                if self.go_high == 10 and self.cpt_move == 2:
                    self.rect.y += 1
                    self.go_down -= 1

                if self.go_down == 0:
                    self.go_high = 0
                    self.go_down = 10

                if self.cpt_move == 2:
                    self.cpt_move = 0


                if pygame.sprite.collide_rect(self, player):
                    if pygame.sprite.collide_mask(self, player):
                        collide_objects_fx.play()
                        player.ammo += 3
                        self.kill()


        screen.blit(self.image, ((self.rect.x + 14) - tile_bg_scroll[0], self.rect.y - tile_bg_scroll[1]))




class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, scale , target):
        pygame.sprite.Sprite.__init__(self)

        self.speed = 12
        self.char_type = "projectile"
        self.animation_list = []
        animation_types = ['rotate', 'explode']
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # load all images for the players
        self.animation_list = (animation(self.char_type, scale, animation_types))
        self.image = self.animation_list[self.action][self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)


        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

        self.update_time = pygame.time.get_ticks()

        self.flip = 0
        self.image_collision = self.animation_list[0][3]  # = la dernière frame de l'animation de l'attaque
        self.mask = pygame.mask.from_surface(self.image_collision)

        self.target = target
        self.length_travel = 0

    def update_animation(self):
        ANIMATION_COOLDOWN_bullet = 100

        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]


        if self.action == 0:  # Tourne
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN_bullet - 50:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1

        elif self.action == 1:  # Explosion
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN_bullet - 20:
                self.update_time = pygame.time.get_ticks()  # on remet a jour le temps
                self.frame_index += 1


        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):  # si l'index dépasse ou est égale a la dernière frame de la liste
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update(self):
        dx = 0
        dy = 0

        if self.target == 'top':
            dy = -8
            self.flip = 90
        else:
            dx = (self.direction * self.speed)


        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.update_action(1)
                player.lock_top = False

        for enemy in enemy_group:
            if enemy.alive:
                if pygame.sprite.collide_rect(self, enemy):
                    if pygame.sprite.collide_mask(self, enemy):
                        if enemy.health > 0:
                            self.update_action(1)
                            enemy.ready_to_attack = True
                            player.lock_top = False
                            enemy.hurt = True


        for roof_enemy in roof_ennemy_group:
            if roof_enemy.alive:
                if pygame.sprite.collide_rect(self, roof_enemy):
                    if pygame.sprite.collide_mask(self, roof_enemy):
                        if roof_enemy.health > 0:
                            self.update_action(1)
                            player.lock_top = False
                            roof_enemy.hurt = True


        if self.action == 1 and self.frame_index == 0: # si il est dans l'anim d'explosion et que il est a sa dernière frame
            self.kill() # alors on tue l'objet

        self.length_travel += dx


        if abs(self.length_travel) == (SCREEN_WIDTH / 2 - 40) + 48:
            self.kill()



        self.rect.x += dx
        self.rect.y += dy





        self.update_animation()

        screen.blit(pygame.transform.rotate(self.image, self.flip),(self.rect.x - tile_bg_scroll[0], self.rect.y - tile_bg_scroll[1]))



class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 70
        self.speed = 6  # horizontal speed
        self.image = missile_img
        self.image = pygame.transform.scale(self.image,(self.image.get_width() * 3, self.image.get_height() * 3))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.acceleration = 0

    def update(self):

        dy = self.speed

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + dy + 4, self.width, self.height):
                self.speed = 0

        # update grenade postion

        dy = 0 if pause_game == True else dy

        self.rect.y += dy

        # countdown timer
        if pause_game == False:
                self.timer -= 1
                if self.timer <= 0:
                    self.kill()
                    if player.alive == True:
                        grenade_fx.play()
                    explosion = Explosion(self.rect.x, self.rect.y, 2)
                    explosion_group.add(explosion)


                    if player.rect.colliderect(self.rect):
                        #print("in")
                        player.hurt = True

                    for robot_enemy in enemy_group:
                        if pygame.sprite.collide_rect(self, robot_enemy):
                            #if pygame.sprite.collide_mask(self, robot_enemy):
                                if robot_enemy.health > 0:
                                    robot_enemy.ready_to_attack = True
                                    if robot_enemy.stun == False:
                                        robot_enemy.hurt = True



        screen.blit(self.image, (self.rect.x - tile_bg_scroll[0], self.rect.y - tile_bg_scroll[1]))




class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(7):
            img = pygame.image.load(f'Images/explosion/{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)

        self.frame_index = 0
        self.image = self.images[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.counter = 0

    def update(self):
        # update animation

        EXPLOSION_SPEED = 4
        self.counter += 1


        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0

            if pause_game == False:
                    self.frame_index += 1

        if self.frame_index >= len(self.images):
            self.kill()
        else:
            self.image = self.images[self.frame_index]

        screen.blit(self.image, ((self.rect.x + 7 ) - tile_bg_scroll[0], self.rect.y - tile_bg_scroll[1]))




# -------------------------------------------------------- #



# function to reset level
def reset_level():  # vide tous les groupes et réinitialise la map avec des -1
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    exit_group.empty()
    decors_group.empty()
    roof_ennemy_group.empty()
    health_item_group.empty()
    speech_bubble_group.empty()
    ammo_item_group.empty()

    # create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data




class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:  # whole screen fade
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour,
                             (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour,
                             (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))

        if self.direction == 2:  # vertical screen fade down
            pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))

        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True

        return fade_complete


# create screen fades

intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PURPLE, 6)



# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

# load in level data and create world
with open(f'Game_levels/level{LEVEL}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)


# create instances ---------------- #

world = World()
player = world.process_data(world_data)




# Main loop --------------------- #

run = True
while run:

    clock.tick(FPS)

    if start_game == False:
        # draw menu

        menu_display.blit(menu_bg,(0,0))
        menu_display.blit(title_img,(250,100))
        # add buttons

        if play_button.draw(menu_display):
            fade(menu_display,'MENU')
            start_game = True
            start_intro = True
            first_game_layer = True
            menu_on = False

        if exit_button.draw(menu_display):
            run = False
            pygame.quit()
            sys.exit()


    else: # si l'utilisateur a appuyé sur le bouton start, alors on lance le jeu.


        tile_bg_scroll = true_scroll.copy()

        # scroll tiles
        tile_bg_scroll[0] = int(tile_bg_scroll[0])
        tile_bg_scroll[1] = int(tile_bg_scroll[1])

        # draw bg
        draw_bg()

        # draw world map
        world.draw()




# ---------------- screen shake ----------------- #

        if screen_shake:
            if wake_up == True:
                tile_bg_scroll[0] += random.randint(0, 4) - 2
                tile_bg_scroll[1] += random.randint(0, 4) - 2
                true_scroll[0] += random.randint(0, 4) - 2
                true_scroll[1] += random.randint(0, 4) - 2

            else:
                true_scroll[0] += random.randint(0, 3) - 2
                true_scroll[1] += random.randint(0, 3) - 2

# -------------------------------------------------------#

# ---------------- wake up---------------------#

        if wake_up == True:
            player.update_action(9)
            cant_play = True

        if player.action == 9 and 0 <= player.frame_index <= 9:
            if wake_up_shake_cpt <= 60:
                screen_shake = 20

        if player.action == 9 and player.frame_index == 32 and wake_up:
            wake_up = False
            cant_play = False

        if wake_up_shake_cpt <= 60:
            wake_up_shake_cpt += 1

        # positionnez ici car on ne veut pas que clyde passe derrière le panneau quand il passe dessus
        for bubble in speech_bubble_group:
            bubble.update()

# ------------------------------------------------------------------ #


        player.draw()


        for enemy in enemy_group:

            if (player.rect.x - enemy.rect.x >= -850 and player.rect.x <= enemy.rect.x) or (enemy.rect.x - player.rect.x >= -850 and player.rect.x >= enemy.rect.x) or enemy.ready_to_attack == True or LEVEL == MAX_LEVELS :
                if (0 <= player.rect.y - enemy.rect.y <= 400 and player.rect.y >= enemy.rect.y) or (player.rect.y <= enemy.rect.y and 0 <= enemy.rect.y - player.rect.y <= 400) or enemy.ready_to_attack == True or LEVEL == MAX_LEVELS :
                    enemy.ai()
                    enemy.draw()
                    enemy.update()
                    enemy.check_state()

        for roof_enemy in roof_ennemy_group:
            if (player.rect.x - roof_enemy.rect.x >= -600 and player.rect.x <= roof_enemy.rect.x) or (roof_enemy.rect.x - player.rect.x >= -600 and player.rect.x >= roof_enemy.rect.x) or LEVEL == MAX_LEVELS:
                if (0 <= player.rect.y - roof_enemy.rect.y <= 400 and player.rect.y >= roof_enemy.rect.y) or (player.rect.y <= roof_enemy.rect.y and 0 <= roof_enemy.rect.y - player.rect.y <= 400) or LEVEL == MAX_LEVELS:

                    roof_enemy.attack()
                    roof_enemy.update()
                    roof_enemy.check_state()


        # on met les 3 lignes de clyde séparé de draw pour que l'animation de hurt est lieu si l'ennemi explose près de clyde

        screen_shake = player.update(screen_shake)

        num_of_robots_saved, level_complete = player.collide_exit(num_of_robots_saved)

        true_scroll, dash = player.move(moving_left, moving_right, dash,wake_up)  # on recupere le niveau et la valeur de scroll

        # pour ne pas actualiser la vie et les munitions de clyde après le passage d'un level à un autre
        player_health, player_ammo = player.health_ammo_update(player_health, player_ammo)

        if screen_shake > 0:
            screen_shake -= 1

# ------------------------------------------------------


# -----------------------------------------------------

        bullet_group.update()

        grenade_group.update()

        explosion_group.update()


        for item in health_item_group:
            item.update()

        for item in ammo_item_group:
            item.update()


        for exit in exit_group:
            exit.update()

        for decor in decors_group:
            decor.update()


        screen.blit(health_icon_images[abs(player.health - 5)], (15, 15))

        # for x in range(player_health):
        # screen.blit(img_health_item, (15 + (x * 31), 15))

        # -------------------------------------------------------------

        # blit la tète verte des robots sauvés
        screen.blit(img_robot_saved, (15, 56))

        # blit le bon nombre de robot sauvé
        num_list[player.num_saved].draw()

        # blit le slash
        screen.blit(slash, (39, 70))

        # blit le 12 ou autre a définir
        Fontt_num_max_robot_saved.draw()


        if pause_game == True:
            screen.blit(pause_surface,(0,0))
            Fontt_pause_high.draw()



        # show intro
        if start_intro == True:
            if intro_fade.fade():
                start_intro = False  # pour faire en sorte que cela ne se repete que une seule fois --> logique que j'aime
                intro_fade.fade_counter = 0  # back to 0 pour les autres fades

        # update player actions
        if player.alive:
            if wake_up == False:

                # shoot bullets

                if blit_button_once == True:
                    if blit_ibutton_cd < 20:
                        blit_ibutton_cd += 1

                    if blit_ibutton_cd == 20:
                        blit_ibutton_cd = 0
                        ibutton_index += 1

                    if ibutton_index == 2:
                        ibutton_index = 0




                    for robot_enemy in enemy_group:
                        if robot_enemy.stun == True and robot_enemy.stun_timer <= 300 and robot_enemy.save != True and robot_enemy.alive != False:
                            screen.blit(ibutton_list[ibutton_index], (robot_enemy.collision_rect.x - tile_bg_scroll[0] + 15 * robot_enemy.direction, robot_enemy.collision_rect.y - tile_bg_scroll[1] - 80))
                            if robot_enemy.stun_timer == 300:
                                blit_button_once = False

                        if robot_enemy.save == True:
                            blit_button_once = False



                if attack and player.dash_cpt_left == 0 and player.dash_cpt_right == 0:
                    player.update_action(4)

                    save_robot = False
                    shoot_front = False
                    shoot_up = False

                    if player.action == 4 and player.frame_index == 3 and trigger_anim == True:
                        attack_fx.play()
                        player.attack()
                        trigger_anim = False
                    if player.action == 4 and player.frame_index == 5:
                        attack = False
                        trigger_anim = True

                elif save_robot and player.dash_cpt_left == 0 and player.dash_cpt_right == 0:
                    player.update_action(5)

                    attack = False
                    shoot_front = False
                    shoot_up = False

                    if player.action == 5 and player.frame_index == 7 and trigger_anim == True:
                        player.save()
                        trigger_anim = False

                    if player.action == 5 and player.frame_index == 12:
                        save_robot = False
                        trigger_anim = True

                elif shoot_front and player.in_air == False and player.dash_cpt_left == 0 and player.dash_cpt_right == 0:
                    player.update_action(10)

                    shoot_up = False
                    save_robot = False
                    attack = False

                    if player.action == 10 and player.frame_index == 1 and trigger_anim == True:
                        player.ready_to_shoot_front = True
                        player.shoot()
                        trigger_anim = False
                    if player.action == 10 and player.frame_index == 6:
                        shoot_front = False
                        trigger_anim = True


                elif shoot_up and player.in_air == False and player.dash_cpt_left == 0 and player.dash_cpt_right == 0:
                    player.update_action(11)

                    shoot_front = False
                    save_robot = False
                    attack = False

                    if player.action == 11 and player.frame_index == 1 and trigger_anim == True:
                        player.ready_to_shoot_up = True
                        player.shoot()
                        trigger_anim = False

                    if player.action == 11 and player.frame_index == 4:
                        shoot_up = False
                        trigger_anim = True



                elif player.in_air:
                    player.update_action(2)  # 2: jump

                elif moving_left or moving_right:
                    if dash:
                        player.update_action(8)
                    else:
                        player.update_action(1)  # 1: run animation

                elif player.hurt and player.health != 0 : # != 0 pour éviter l'animation de hurt lorsqu'il explose
                    player.update_action(6)

                else:
                    if dash:
                        player.update_action(8)
                    else:
                        player.update_action(0)  # 0: idle



            player_pos_x = player.rect.x
            player_pos_y = player.rect.y

            # check if player has completed the level
            if level_complete:
                #fade en appelant la fonction
                LEVEL += 1

                if LEVEL <= MAX_LEVELS:
                    start_intro = True
                    tile_bg_scroll[0] = 0
                    tile_bg_scroll[1] = 0
                    world_data = reset_level()
                    with open(f'Game_levels/level{LEVEL}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player = world.process_data(world_data)
                else:
                    pygame.mouse.set_visible(False)
                    fade(screen, 'GAME')
                    pygame.time.delay(1000)
                    unfade('GAME')


                    if type_of_game_end == 'GOOD':
                        fade(screen, 'GOOD END')
                        pygame.time.delay(2000)
                        unfade('GOOD END')
                    else:
                        fade(screen, 'BAD END')
                        pygame.time.delay(2000)
                        unfade('BAD END')


                    # credits
                    fade(screen, 'THANKS FOR PLAYING')
                    unfade('THANKS FOR PLAYING')

                    pygame.time.delay(6000)

                    pygame.quit()
                    sys.exit()

        else:
            if player.action == 3 and player.frame_index == 11: # == 11 car derniere frame sinon marche paas
                if death_fade.fade():  # si le fade de l'écran est terminé, alors je peux faire apparaitre le boutton, ect ... :
                    pygame.mouse.set_visible(True)
                    if restart_button.draw(screen):
                        player.death_sound = 1
                        player_health = 5
                        player_ammo = 10
                        death_fade.fade_counter = 0
                        start_intro = True  # si il meurt, on veut refaire l'intro lorsque le niveau démarre
                        tile_bg_scroll[0] = 0
                        tile_bg_scroll[1] = 0
                        world_data = reset_level()
                        with open(f'Game_levels/level{LEVEL}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player = world.process_data(world_data)

    if menu_on == True:
        screen.blit(menu_display,(0,0))

    if num_of_robots_saved >= 12: #TODO ICIIIII
        type_of_game_end = 'GOOD'
    else:
        type_of_game_end = 'BAD'


# ----------- Keyboard --------------------------------


    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # keyboard presses
        if event.type == pygame.KEYDOWN:


            if (event.key == K_LEFT or event.key == K_a) and player.alive:
                if cant_play == False:
                    moving_left = True
                else:
                    moving_left = False

            if (event.key == K_RIGHT or event.key == K_d ) and player.alive:
                if cant_play == False:
                    moving_right = True
                else:
                    moving_right = False

            if (event.key == K_UP or event.key == K_w) and player.alive:
                if cant_play == False:
                    if player.in_air == False:
                        player.jump = True

            if event.key == K_SPACE and player.alive:
                if cant_play == False:
                    if player.action != 5 and player.action != 4:
                        if player.in_air == False:
                            dash = True

            if event.key == K_r and player.alive:
                if cant_play == False:
                    if player.action != 2:
                        attack = True

            if event.key == K_v and player.alive:
                if cant_play == False:
                    if player.action != 2:
                        save_robot = True


            if event.key == K_q and player.alive:
                if player.action != 2:
                    shoot_front = True

            if event.key == K_e and player.alive:
                if cant_play == False:
                    if player.action != 2:
                        shoot_up = True
                        player.lock_top = True

            if event.key == K_ESCAPE:
                run = False

            if event.key == K_p and player.alive:
                if cant_play == False:
                    if pause_game == False:
                        pause_game = True
                    else:
                        pause_game = False


        # keyboard button released
        if event.type == pygame.KEYUP:


            if event.key == K_UP and player.alive:
                if cant_play == False:
                    player.jump = False

            if event.key == K_LEFT:
                if cant_play == False:
                    moving_left = False

            if event.key == K_RIGHT:
                if cant_play == False:
                    moving_right = False

            if event.key == pygame.K_p:
                cant_play = False


    pygame.display.update()