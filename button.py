import pygame

pygame.init()
pygame.mixer.init()  # Initialize the mixer module
pop_sound = pygame.mixer.Sound('assets/pop.ogg')

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.clicked = False

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            pop_sound.play()
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
    
    # def checkForInput1(self, position, screen):
    #     if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
    #         # Toggle the button state when clicked
    #         if self.clicked:
    #             self.clicked = False
    #             self.text = self.font.render(self.text_input, True, self.base_color)
    #         else:
    #             self.clicked = True
    #             self.text = self.font.render("TEST", True, self.base_color)
                
    #         screen.blit(self.text, self.text_rect)
    #         return True
    #     else:
    #         return False
        
    def updateText(self):
        if self.clicked:
            self.text = self.font.render("TEST", True, self.base_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
    
    
    def handleEvent(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.checkForInput(mouse_pos):
                self.clicked = not self.clicked
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pass
        
    def handleClick(self):
        self.clicked = not self.clicked
        
    def updateImage(self, img, scale):
        self.image = pygame.transform.scale(img, scale)