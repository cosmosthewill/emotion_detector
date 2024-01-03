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

def good():
    subprocess.Popen(["python", "realtimedetection.py"])
    time.sleep(5)
    #os.kill(os.getpid(), signal.SIGTERM)
    
def bad():
    subprocess.Popen(["python", "optimized_ver.py"])
    time.sleep(5)
    #os.kill(os.getpid(), signal.SIGTERM)

def back():
    import menu  # Import the module to avoid circular dependencies
    menu.mainmenu()

def mainmenu():
    while True:
        SCREEN.blit(BG, (0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        MENU_TEXT = get_font(80).render("PERFORMANCE", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        
        GOODPERFORMANCE = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 250), 
                            text_input="PERFORMANCE", font=get_font(60), base_color="#d7fcd4", hovering_color="Green")
        BADPERFORMANCE = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 400), 
                            text_input="BALANCED", font=get_font(60), base_color="#d7fcd4", hovering_color="Green")
        BACK_BUTTON = Button(image=None, pos=(640, 650), 
                            text_input="BACK", font=get_font(50), base_color="#d7fcd4", hovering_color="Green")
        
        INFO_TEXT_1 = get_font(40).render("PERFORMANCE: FOR HIGH-END PC WITH ADDIDION FEATURES", True, "#b68f40")
        INFO_RECT_1 = INFO_TEXT_1.get_rect(center=(640, 500))
        INFO_TEXT_2 = get_font(40).render("BALANCED: FOR LOW-END PC WITH LIMITED FEATURES", True, "#b68f40")
        INFO_RECT_2 = INFO_TEXT_2.get_rect(center=(640, 570))
        
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(INFO_TEXT_1, INFO_RECT_1)
        SCREEN.blit(INFO_TEXT_2, INFO_RECT_2)
        for button in [GOODPERFORMANCE, BADPERFORMANCE, BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    back()
                if GOODPERFORMANCE.checkForInput(MENU_MOUSE_POS):
                    good()
                if BADPERFORMANCE.checkForInput(MENU_MOUSE_POS):
                    bad()

        pygame.display.update()
        
mainmenu()