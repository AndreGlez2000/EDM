import pygame
# Colores (RGB)
from model.constants import *
import pygame
from model.constants import *

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text, base_color, hovering_color, font, image):
        self.image = image
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
        
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

        self.base_color, self.hovering_color = base_color, hovering_color
        self.font = font
        self.textd = self.font.render(self.text, True, self.base_color)
       
        if self.image is None:
            self.image = self.textd
            
        self.radius = 15
        self.is_hovered = False
        
        self.textd_rect = self.textd.get_rect(center=self.rect.center)

    def draw(self, screen: pygame.Surface):
        color = BLUE_C if self.is_hovered else ORANGE

        pygame.draw.rect(screen, color, self.rect, border_radius=self.radius)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def update_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def checkForInput(self, screen):
        action = False
        self.rect = self.image.get_rect(center=self.rect.center)
        position = pygame.mouse.get_pos()

        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.textd = self.font.render(self.text, True, self.hovering_color)
        else:
            self.textd = self.font.render(self.text, True, self.base_color)
    
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.textd, self.textd_rect)
        return action

    def update_position(self, x: int, y: int, width: int, height: int):
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.textd_rect = self.textd.get_rect(center=self.rect.center)

    def update(self, screen: pygame.Surface):
        """Actualiza el estado del botón y lo dibuja en la pantalla"""
        self.update_hover(pygame.mouse.get_pos())
        self.draw(screen)