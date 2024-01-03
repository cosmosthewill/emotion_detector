import pygame
import sys
import subprocess
import os
import signal
import time
import ctypes
from button import Button
from sound_manager import play_background_music
import signal

# Initialize Pygame
pygame.init()
pygame.mixer.init()
# Set up display
width, height = 1280, 720
SCREEN = pygame.display.set_mode((width, height))
pygame.display.set_caption("MODE")
BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/times.ttf", size)

# VAR
white = (255, 255, 255)
black = (0, 0, 0)
with open("sound.txt", "r") as file:
    sound_on = file.read()
if sound_on.lower() == "true":
    sound_on = True
else:
    sound_on = False
dnd_on = False

def back():
    import options  # Import the module to avoid circular dependencies
    options.mainmenu()

def enable_dnd_windows():
    try:
        process = subprocess.Popen(['powershell', '-Command', 'Start-Process powershell -ArgumentList "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\System -Name FocusAssist -Value 2" -Verb RunAs'])
        print("enabled")
        process.communicate()  # Wait
        input("Press any key to continue...")
    except Exception as e:
        print(f"Error enabling Focus Assist on Windows: {e}")

def disable_dnd_windows():
    try:
        process = subprocess.Popen(['powershell', '-Command', 'Start-Process powershell -ArgumentList "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\System -Name FocusAssist -Value 0" -Verb RunAs'])
        print("disabled")
        process.communicate()  # Wait
        input("Press any key to continue...")
    except Exception as e:
        print(f"Error disabling Focus Assist on Windows: {e}")
     
def update_sound():
    with open("sound.txt", "w") as file:
        file.write(str(sound_on))
         
def mainmenu():
    global sound_on, dnd_on
    #play_background_music()
    while True:
        SETTINGS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0,0))
        # SCREEN.fill(white)
        # OPTIONS_TEXT = get_font(45).render("STH HERE IDK", True, "Black")
        # OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        
        #SOUND
        SOUND_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(550, 200), 
                            text_input="SOUND", font=get_font(60), base_color="#d7fcd4", hovering_color="Green")
        SOUND_STATE = Button(image=pygame.image.load("assets/off.png"), pos=(1000, 300), 
                            text_input="", font=get_font(10), base_color="#d7fcd4", hovering_color="Green")
        if sound_on:
            SOUND_STATE.updateImage(img=pygame.image.load("assets/on.png"), scale=(90, 60))
        else:
            SOUND_STATE.updateImage(img=pygame.image.load("assets/off.png"), scale=(90, 60))
            
        #DND
        DND_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(550, 350), 
                            text_input="FOCUS", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")
        DND_STATE = Button(image=pygame.image.load("assets/off.png"), pos=(1000, 470), 
                            text_input="", font=get_font(10), base_color="#d7fcd4", hovering_color="Green")
        if dnd_on:
            DND_STATE.updateImage(img=pygame.image.load("assets/on.png"), scale=(90, 60))
        else:
            DND_STATE.updateImage(img=pygame.image.load("assets/off.png"), scale=(90, 60))
        
        
        # SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        SETTINGS_BACK = Button(image=None, pos=(640, 650), 
                            text_input="BACK", font=get_font(50), base_color="#d7fcd4", hovering_color="Green")

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SETTINGS_BACK.checkForInput(SETTINGS_MOUSE_POS):
                    back()
                if SOUND_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                    sound_on = not sound_on
                    update_sound()
                    if sound_on:
                        pygame.mixer.music.unpause()
                        SOUND_STATE.updateImage(img=pygame.image.load("assets/on.png"), scale=(90, 60))
                    else:
                        pygame.mixer.music.pause()
                        SOUND_STATE.updateImage(img=pygame.image.load("assets/off.png"), scale=(90, 60))
                if DND_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                    dnd_on = not dnd_on
                    if dnd_on:
                        DND_STATE.updateImage(img=pygame.image.load("assets/on.png"), scale=(90, 60))
                        enable_dnd_windows()
                    else:
                        DND_STATE.updateImage(img=pygame.image.load("assets/off.png"), scale=(90, 60))
                        disable_dnd_windows()
                    
        for button in [SOUND_BUTTON, DND_BUTTON, SOUND_STATE, DND_STATE]:
            button.changeColor(SETTINGS_MOUSE_POS)
            # button.updateText()
            button.update(SCREEN)
            
        
        SETTINGS_BACK.changeColor(SETTINGS_MOUSE_POS)
        SETTINGS_BACK.update(SCREEN)
            
        pygame.display.update()
        
mainmenu()