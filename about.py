import pygame
import sys
import subprocess
import os
import signal
import time
from button import Button
# Initialize Pygame
pygame.init()

# Set up display
width, height = 1280, 720
SCREEN = pygame.display.set_mode((width, height))
pygame.display.set_caption("MODE")
BG = pygame.image.load("assets/About.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/times.ttf", size)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

def back():
    import options  # Import the module to avoid circular dependencies
    options.mainmenu()

def mainmenu():
    while True:
        SCREEN.blit(BG, (0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        BACK_BUTTON = Button(image=None, pos=(640, 650), 
                            text_input="BACK", font=get_font(50), base_color="#d7fcd4", hovering_color="Green")
        
        for button in [BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    back()

        pygame.display.update()
        
mainmenu()