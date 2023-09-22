import pygame, os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ROWS = 60
COLS = 300
TILE_SIZE = SCREEN_HEIGHT // ROWS + 30 # +30 pour avoir la meme taille que dans le file level editor

TILE_TYPES = 46

# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'Clyde/Images/tile/{x}.png').convert_alpha()
    if x == 4 or x == 5 or x == 15 or x == 16 or x == 33:
        img = pygame.transform.scale(img, (TILE_SIZE * 2, TILE_SIZE))
    elif x == 11 or x == 12 or x == 22:
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE * 2))
    elif x == 34 or x == 35:
        img = pygame.transform.scale(img, (78, 28))
    elif x == 36 or x == 42 or x == 43:
        img = pygame.transform.scale(img, (89, 28))
    elif x == 30 or x == 31 or x == 32:
        img = pygame.transform.scale(img, (TILE_SIZE*3, TILE_SIZE *3))
    else:
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)


def animation(char_type, scale, animation_types):
    big_list = []
    for animation in animation_types:
        # reset temporary list of images
        temp_list = []
        # count number of files in the folder
        num_of_frames = len(os.listdir(f'Clyde/Images/{char_type}/{animation}'))
        for i in range(num_of_frames):
            img = pygame.image.load(f'Clyde/Images/{char_type}/{animation}/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        big_list.append(temp_list)

    return big_list


first_layer = pygame.image.load('Clyde/Images/background/first_layer.png').convert_alpha()
first_layer = pygame.transform.scale(first_layer, (800, 640))

second_layer = pygame.image.load('Clyde/Images/background/2d_layer.png').convert_alpha()
second_layer = pygame.transform.scale(second_layer, (800, 640))

last_layer = pygame.image.load('Clyde/Images/background/last_layer.png').convert_alpha()
last_layer = pygame.transform.scale(last_layer, (800, 640))

menu_bg = pygame.image.load('Clyde/Images/menu_background/background_menu.png').convert_alpha()
menu_bg = pygame.transform.scale(menu_bg, (800, 640))

missile_img = pygame.image.load('Clyde/Images/roof enemy/grenade.png').convert_alpha()

img_health_item = pygame.image.load('Clyde/Images/Icons/health_icon.png').convert()
img_health_item = pygame.transform.scale(img_health_item, (img_health_item.get_width() * 4 , img_health_item .get_height() * 4))

health_icon_images = []
for i in range(6):
    img = pygame.image.load(f'Clyde/Images/Icons/{i}.png').convert()
    img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
    health_icon_images.append(img)


img_robot_saved = pygame.image.load('Clyde/Images/Icons/green_head.png').convert()
img_robot_saved = pygame.transform.scale(img_robot_saved, (img_robot_saved.get_width() * 4 , img_robot_saved .get_height() * 4))

slash = pygame.image.load('Clyde/Images/Icons/slash.png').convert()
slash = pygame.transform.scale(slash, (slash.get_width() * 3 , slash .get_height() *3))

img_ammo_item = pygame.image.load("Clyde/Images/Icons/ammo_icon.png").convert_alpha()