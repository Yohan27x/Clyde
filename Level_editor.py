import pygame, csv
from button import *



pygame.init()

clock = pygame.time.Clock()
FPS = 60

# game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 850
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN),pygame.SCALED | pygame.DOUBLEBUF, vsync=1 )
pygame.display.set_caption('Level Editor')

# define game variables
ROWS = 60
MAX_COLS = 300
TILE_SIZE = SCREEN_HEIGHT // ROWS

TILE_TYPES = 46
level = 4
current_tile = 0
scroll_left = False
scroll_right = False
scroll_hor = 0
scroll_speed = 1

# load images
# store tiles in a list

img_list = []

for x in range(TILE_TYPES):
    img = pygame.image.load(f'Images/tile/{x}.png').convert_alpha()
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


save_img = pygame.image.load('Images/Level_editor_buttons/save_btn.png').convert_alpha()
load_img = pygame.image.load('Images/Level_editor_buttons/load_btn.png').convert_alpha()

# define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# define font
font = pygame.font.SysFont('Futura', 30)

# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

# create ground
#for tile in range(0, MAX_COLS):
    #world_data[ROWS - 1][tile] = 0


# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# create function for drawing background
def draw_bg():
    screen.fill(GREEN)

# draw grid
def draw_grid():
    # vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll_hor, 0), (c * TILE_SIZE - scroll_hor, SCREEN_HEIGHT))
    # horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


# function for drawing the world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll_hor, y * TILE_SIZE))


# create buttons
save_button = Button_level(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = Button_level(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
# make a button list
button_list = []
button_col = 0
button_row = 0

for i in range(len(img_list)):
    tile_button = Button_level(SCREEN_WIDTH + (60 * button_col) + 40, 50 * button_row + 40, img_list[i], 2) #TODO ICIII
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

run = True
while run:

    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

    # save and load data
    if save_button.draw(screen):
        # save level data
        with open(f'Game_levels/level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in world_data:
                writer.writerow(row)

    if load_button.draw(screen):
        # load in level data
        # reset scroll back to the start of the level
        scroll_hor = 0
        with open(f'Game_levels/level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

    # draw tile panel and tiles
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # choose a tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    # highlight the selected tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # scroll the map
    if scroll_left == True and scroll_hor > 0:
        scroll_hor -= 2 * scroll_speed
    if scroll_right == True and scroll_hor < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll_hor += 2 * scroll_speed

    # add new tiles to the screen
    # get mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll_hor) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    # check that the coordinates are within the tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1

            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 4

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()