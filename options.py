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
BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/times.ttf", size)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

def back():
    import menu  # Import the module to avoid circular dependencies
    menu.mainmenu()

def guides_scence():
    import guides
    guides.mainmenu()
    
def about_scence():
    import about
    about.mainmenu()
    
def settings_scence():
    import settings
    settings.mainmenu() 
    
def mainmenu():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0,0))
        # SCREEN.fill(white)
        # OPTIONS_TEXT = get_font(45).render("STH HERE IDK", True, "Black")
        # OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        
        GUIDES_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 200), 
                            text_input="GUIDES", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")
        ABOUT_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 350), 
                            text_input="CONTACT", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")
        SETTINGS = Button(image=pygame.image.load("assets/PLAY Rect.png"), pos=(640, 500), 
                            text_input="SETTINGS", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")
        
        
        
        # SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        OPTIONS_BACK = Button(image=None, pos=(640, 650), 
                            text_input="BACK", font=get_font(50), base_color="#d7fcd4", hovering_color="Green")

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    back()
                if GUIDES_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    guides_scence()
                if ABOUT_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    about_scence()
                if SETTINGS.checkForInput(OPTIONS_MOUSE_POS):
                    settings_scence()
                
        for button in [ABOUT_BUTTON, SETTINGS,GUIDES_BUTTON]:
            button.changeColor(OPTIONS_MOUSE_POS)
            # button.updateText()
            button.update(SCREEN)
            
        
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
            
        pygame.display.update()
        
mainmenu()