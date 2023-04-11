import pygame


# load musics and sounds
pygame.mixer.music.load('audio/dont-forget-what-i-taught-you.mp3')  # pas de variable, elle se joue toute seul tout le tmps
pygame.mixer.music.set_volume(0.3)  # 30% du volume initial car la musique est forte de base
pygame.mixer.music.play(-1, 0.0,5000)  # -1 car joué a l'infini / 0.0 car pas de délai / 5000ms = 5s pour le fade au début


shoot_fx = pygame.mixer.Sound('audio/204321__juancamiloorjuela__punch.wav')
shoot_fx.set_volume(0.6)

attack_fx = pygame.mixer.Sound('audio/attack.wav')
attack_fx.set_volume(0.4)

hurt_clydefx = pygame.mixer.Sound('audio/hurt_clyde.wav')
hurt_clydefx.set_volume(0.6)

hurt_robot_ennemyfx = pygame.mixer.Sound('audio/hurt_robot_ennemy.wav')
hurt_robot_ennemyfx.set_volume(0.3)

hurt_top_ennemyfx = pygame.mixer.Sound('audio/hurt_top_ennemy.mp3')
hurt_top_ennemyfx.set_volume(0.4)

explosion_fx =  pygame.mixer.Sound('audio/die_explosion.wav')
explosion_fx.set_volume(0.5)

no_ammofx =  pygame.mixer.Sound('audio/no ammo.wav')
no_ammofx.set_volume(0.3)

jump_fx = pygame.mixer.Sound('audio/jump_fx1.wav')
jump_fx.set_volume(0.3)

grenade_fx = pygame.mixer.Sound('audio/grenade_fx.wav')
grenade_fx.set_volume(0.1)


dash_fx = pygame.mixer.Sound('audio/dash1.wav')
dash_fx.set_volume(0.8)

stun_fx = pygame.mixer.Sound('audio/stun.wav')
stun_fx.set_volume(0.2)

save_collide_fx = pygame.mixer.Sound('audio/save.wav')
save_collide_fx.set_volume(0.2)

collide_objects_fx = pygame.mixer.Sound('audio/object.wav')
collide_objects_fx.set_volume(0.8)

roof_die_fx = pygame.mixer.Sound('audio/Explosion15.wav')
roof_die_fx.set_volume(0.4)





