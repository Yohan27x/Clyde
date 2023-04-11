import pygame

# Setup pygame/window ---------------------------------------- #
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

pygame.display.set_caption('game base non resiz')
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_HEIGHT), 0, 32)
surface = pygame.Surface((50, 50))

SHADE_WHITE = (212,212,212)
WHITE = (255, 255, 255)


# Funcs/Classes ---------------------------------------------- #

def palette_swap(surf, image, old_c, new_c):
    img_copy = pygame.Surface(image.get_size())  # prend la taille de l'image et crée une surface avec
    img_copy.fill(new_c)  # remplit la surface créé avec la nouvelle couleur
    surf.set_colorkey(old_c)  # faire en sorte que l'ancienne couleur n'apparaisse pas
    img_copy.blit(surf, (0, 0))  # blit la nouvelle " surface " sur une surface
    return img_copy

def clip(surf, x, y, x_size, y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()


class Font():
    def __init__(self, file):
        self.spacing = 1
        self.character_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                                'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                                'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                                'z', '.', '-', ',', ':', '+', '\'', '!', '?', '0', '1', '2', '3', '4', '5', '6', '7',
                                '8', '9', '(', ')', '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';']
        font_img = file
        font_img.set_colorkey((0, 0, 0))
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['A'].get_width()

    def render(self, surf, text, loc):
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing


class Newfont():
    def __init__(self, message, font, x, y, scale):
        #my_font = Font(little_font)
        self.font = font
        self.x = x
        self.y = y
        self.message = message
        my_big_font = Font(self.font)
        surfa = pygame.Surface((300, 200))
        surfa.fill((120, 120, 120))
        surfa.set_colorkey((120, 120, 120))
        my_big_font.render(surfa,self.message , (self.x, self.y))
        self.surfa = pygame.transform.scale(surfa, (int(surfa.get_width() * scale), int(surfa.get_height() * scale)))

    def draw(self):
        screen.blit(self.surfa, (0, 0))


# ------------------------------------------------------------------------ #


font_list = []
for i in range(60):
    large_font = pygame.image.load("Images/Font/large_font.png").convert()
    font_list.append(large_font)


for i in range(30):
    if i % 2 == 0:
        font_list[i] = palette_swap(font_list[i], font_list[i], (255, 0, 0), WHITE)
    else :
        font_list[i] = palette_swap(font_list[i], font_list[i], (255, 0, 0), SHADE_WHITE)




# thanks for playing
Fontt_high_thanks = Newfont('Thanks',font_list[0], 56, 26, 5)
Fontt_shade_thanks = Newfont('Thanks',font_list[1], 56, 27, 5)

Fontt_high_for = Newfont('For',font_list[2], 68, 45, 5)
Fontt_shade_for = Newfont('For',font_list[3], 68, 46, 5)

Fontt_high_playing = Newfont('Playing !',font_list[4],56, 65, 5)
Fontt_shade_playing = Newfont('Playing !',font_list[5], 56, 66, 5)


# bad end
Fontt_high_bad = Newfont('Bad',font_list[6], 65, 22, 5)
Fontt_shade_bad = Newfont('Bad',font_list[7], 65, 23, 5)

Fontt_high_end = Newfont('End',font_list[8], 69, 39, 5)
Fontt_shade_end = Newfont('End',font_list[9], 69, 40, 5)

Fontt_high_lessthan =  Newfont('You saved less than 12 robots ...',font_list[22], 30, 125, 3)
Fontt_shade_lessthan =  Newfont('You saved less than 12 robots ...',font_list[23], 30, 126, 3)




# good end
Fontt_high_good = Newfont('Good',font_list[10], 62, 22, 5)
Fontt_shade_good = Newfont('Good',font_list[11], 62, 23, 5)

Fontt_high_end2 = Newfont('End',font_list[12], 67, 39, 5)
Fontt_shade_end2 = Newfont('End',font_list[13], 67, 40, 5)

Fontt_high_morethan =  Newfont('You saved 12 or more robots !',font_list[24], 32, 125, 3)
Fontt_shade_morethan =  Newfont('You saved 12 or more robots !',font_list[25], 32, 126, 3)


#credits
Fontt_high_credits = Newfont('Credits :',font_list[14], 49, 17, 5)
Fontt_shade_credits = Newfont('Credits :',font_list[15], 49, 18, 5)


# -------------------

Fontt_high_adrien = Newfont('- Adrien : Characters Animation',font_list[18], 4, 80, 3)
Fontt_shade_adrien = Newfont('- Adrien : Characters Animation',font_list[19], 4, 81, 3)

Fontt_high_yohan = Newfont('- Yohan : Programmer ',font_list[16], 4, 100, 3)
Fontt_shade_yohan = Newfont('- Yohan : Programmer ',font_list[17], 4, 101, 3)

Fontt_high_others =  Newfont('-Buakaw, Lea, Thomas, Minh and others!',font_list[26], 4, 120, 3)
Fontt_shade_others =  Newfont('-Buakaw, Lea, Thomas, Minh and others!',font_list[27], 4, 121, 3)

#Fontt_high_ytb =  Newfont('-CodeWithRuss, DaFluffyPotato ',font_list[28], 30, 160, 3)
#Fontt_shade_ytb =  Newfont('-CodeWithRuss, DaFluffyPotato ',font_list[29], 30, 161, 3)





#----------------




num = 0
num_list = []

j = 0

# dx = 0 if pause_game == True else dx

for i in range(30,53):

    font_list[i] = palette_swap(font_list[i], font_list[i], (255, 0, 0), WHITE)

    # décaler le nombre de robot sauvés quand on passe au dessus de 10 pour l'affichage
    Fontt_num_robot_saved_ = Newfont(str(num), font_list[i], 28, 71, 1) if j < 10 else Newfont(str(num), font_list[i], 22, 71, 1)
    num += 1
    num_list.append(Fontt_num_robot_saved_)
    j += 1



font_list[53] = palette_swap(font_list[53], font_list[53], (255, 0, 0), WHITE) # 53 avant 45

Fontt_num_max_robot_saved = Newfont(' 18',font_list[53], 50, 71, 1) #53

font_list[54] = palette_swap(font_list[54], font_list[54], (255, 0, 0), WHITE) #54 avant 46


Fontt_pause_high = Newfont("Pause",font_list[54], 82,60, 4) #54

