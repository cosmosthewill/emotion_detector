# sound_manager.py
import pygame
pygame.init()
pygame.mixer.init()

def play_background_music():
    pygame.mixer.music.load('assets/music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
