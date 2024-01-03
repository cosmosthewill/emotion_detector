import pygame
import sys
import subprocess
from button import Button
from sound_manager import play_background_music


# Initialize Pygame
pygame.init()

# Set up display
width, height = 1280, 720
SCREEN = pygame.display.set_mode((width, height))
pygame.display.set_caption("SAFE DRIVER")
BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/times.ttf", size)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)


def start():
    import mode
    mode.mainmenu()

    
def options():
    import options
    options.mainmenu()


def mainmenu():
    with open("sound.txt", "r") as file:
        sound_on = file.read()
    if sound_on.lower() == "true":
        toggle_sound = True
    else:
        toggle_sound = False
    if toggle_sound:
        play_background_music()
    while True:
        SCREEN.blit(BG, (0,0))
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        MENU_TEXT = get_font(90).render("SAFE DRIVER", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        
        START_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="START", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")
        QUIT_BUTTON = Button(image=None, pos=(640, 650), 
                            text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="Green")
                                       
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        
        for button in [START_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_BUTTON.checkForInput(MENU_MOUSE_POS):
                    start()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

mainmenu()
        