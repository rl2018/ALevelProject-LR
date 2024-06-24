import pygame, sys

#Setting up an environment to initialize pygame
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('DriveRightUK')
screenwidth=720
screenheight=405
screen = pygame.display.set_mode((screenwidth, screenheight),0,32)

#setting font settings
font = pygame.font.SysFont(None, 30)


#A function that can be used to write text on our screen and buttons
def draw_text(text, font, color, surface, x, y, centered=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if centered:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    
    surface.blit(text_surface, text_rect)

# A variable to check for the status later
click = False

# Main container function that holds the buttons and game functions
def main_menu():
    while True:

        screen.fill((0,190,255))
        draw_text("DriveRightUK", font, (0,0,0), screen, (screenwidth//2), 50, centered=True)

        mx, my = pygame.mouse.get_pos()

        #creating buttons
        button_1 = pygame.Rect(10, 350, 200, 40)
        button_2 = pygame.Rect(10, 300, 200, 40)
        button_3 = pygame.Rect(670, 80, 40, 40)

        #defining functions when a certain button is pressed
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        if button_3.collidepoint((mx, my)):
            if click:
                settings()
        pygame.draw.rect(screen, (255, 0, 0), button_1, 0, 3)
        pygame.draw.rect(screen, (255, 0, 0), button_2, 0, 3)
        pygame.draw.rect(screen, (128, 128, 128), button_3, 0, 100)

        #writing text on top of button
        draw_text('PLAY', font, (255,255,255), screen, 20, 360)
        draw_text('OPTIONS', font, (255,255,255), screen, 20, 310)


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

#This function is called when the "PLAY" button is clicked.
def game():
    running = True
    while running:
        screen.fill((0,0,0))

        draw_text('GAME SCREEN', font, (255, 255, 255), screen, 20, 20)
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
        screen.fill((0,0,0))

        draw_text('OPTIONS SCREEN', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)

# This function is called when the "SETTINGS" button is clicked.
def settings():
    running = True
    while running:
        screen.fill((0,190,255))

        draw_text("SETTINGS SCREEN", font, (255, 255, 255), screen, (screenwidth//2), 50, centered=True)
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
