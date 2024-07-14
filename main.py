import pygame
import sys

# Setting up an environment to initialize pygame
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('DriveRightUK')
screenwidth = 720
screenheight = 405
screen = pygame.display.set_mode((screenwidth, screenheight), 0, 32)

# background image
background_image = pygame.image.load('background.jfif')
background_image = pygame.transform.scale(background_image, (screenwidth, screenheight))

#cog image
cog_image = pygame.image.load('cog.png')
cog_image = pygame.transform.scale(cog_image, (30,30))

# Setting font settings
font = pygame.font.SysFont(None, 30)

class Text:
    def __init__(self, text, font, color, surface):
        self.text = text
        self.font = font
        self.color = color
        self.surface = surface
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect()

    def draw(self, x, y, centered=False):
        if centered:
            self.text_rect.center = (x, y)
        else:
            self.text_rect.topleft = (x, y)
        self.surface.blit(self.text_surface, self.text_rect)

class Button:
    def __init__(self, x, y, width, height, color, hover_color, text, font, text_color, surface, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = Text(text, font, text_color, surface)
        self.surface = surface
        self.image = image

    def draw(self):
        mx, my = pygame.mouse.get_pos()
        if self.rect.collidepoint((mx, my)):
            pygame.draw.rect(self.surface, self.hover_color, self.rect, 0, 3)
        else:
            pygame.draw.rect(self.surface, self.color, self.rect, 0, 3)
        self.text.draw(self.rect.centerx, self.rect.centery, centered=True)

        if self.image:
            image_rect = self.image.get_rect(center=self.rect.center)
            self.surface.blit(self.image, image_rect)

    def is_clicked(self):
        mx, my = pygame.mouse.get_pos()
        if self.rect.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                return True
        return False

# A variable to check for the status later
click = False

# Main container function that holds the buttons and game functions
def main_menu():
    global click
    play_button = Button(10, 350, 200, 40, (255, 0, 0), (200, 0, 0), "PLAY", font, (255, 255, 255), screen)
    options_button = Button(10, 300, 200, 40, (255, 0, 0), (200, 0, 0), "OPTIONS", font, (255, 255, 255), screen)
    settings_button = Button(670, 80, 40, 40, (128, 128, 128), (100, 100, 100), "", font, (255, 255, 255), screen, cog_image)

    while True:
        screen.blit(background_image, (0,0))

        title_text = Text("DriveRightUK", font, (0, 0, 0), screen)
        title_text.draw(screenwidth // 2, 50, centered=True)

        play_button.draw()
        options_button.draw()
        settings_button.draw()

        if play_button.is_clicked():
            game()
        if options_button.is_clicked():
            options()
        if settings_button.is_clicked():
            settings()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

# This function is called when the "PLAY" button is clicked.
def game():
    running = True
    while running:
        screen.fill((0, 0, 0))

        game_text = Text('GAME SCREEN', font, (255, 255, 255), screen)
        game_text.draw(20, 20)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)

# This function is called when the "OPTIONS" button is clicked.
def options():
    running = True
    while running:
        screen.fill((0, 0, 0))

        options_text = Text('OPTIONS SCREEN', font, (255, 255, 255), screen)
        options_text.draw(20, 20)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)

# This function is called when the "SETTINGS" button is clicked
def settings():
    running = True
    while running:
        screen.fill((0, 190, 255))

        settings_text = Text("SETTINGS SCREEN", font, (255, 255, 255), screen)
        settings_text.draw(screenwidth // 2, 50, centered=True)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)

main_menu()