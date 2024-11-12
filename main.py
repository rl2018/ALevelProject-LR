import pygame
import sys
import os # for checking if save file exists
import time

# Setting up an environment to initialise pygame
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('DriveRightUK') # set the window name
screenwidth = 720 # width of the screen
screenheight = 405 # height of the screen
screen = pygame.display.set_mode((screenwidth, screenheight), 0, 32)
current_directory = os.path.dirname(os.path.abspath(__file__)) # gets the directory of the game

# Load background image
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, (screenwidth, screenheight))

# Load logo image
logo_image = pygame.image.load('simlogo.png')
logo_image = pygame.transform.scale(logo_image, (400, 80))

# Load cog image
cog_image = pygame.image.load('cog.png')
cog_image = pygame.transform.scale(cog_image, (30,30))

# Setting font settings
font = pygame.font.SysFont(None, 30) # default font
font_50 = pygame.font.SysFont(None, 50)
font_40 = pygame.font.SysFont(None, 40)
font_30 = pygame.font.SysFont(None, 30)
font_25 = pygame.font.SysFont(None, 25)
font_20 = pygame.font.SysFont(None, 20)
font_10 = pygame.font.SysFont(None, 10)

# Class used to write text on screen
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


# Class used to generate buttons
class Button:
    def __init__(self, x, y, width, height, color, hover_color, border_color, border_width, text, font, text_color, surface, image=None):
        if x == "center":  # If the value of the x parameter is "center"
            x = (screenwidth // 2) - (width // 2)  # Center the element horizontally
        self.width = width
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = Text(text, font, text_color, surface)
        self.surface = surface
        self.image = image
        self.border_color = border_color
        self.border_width = border_width

    def draw(self):
        mx, my = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint((mx, my)) else self.color
        
        # Draw the button rectangle with the border
        if self.border_color and self.border_width > 0:
            pygame.draw.rect(self.surface, self.border_color, self.rect, border_radius=3)  # Border
            inner_rect = self.rect.inflate(-self.border_width * 2, -self.border_width * 2)  # Adjust the inner rect size
            pygame.draw.rect(self.surface, current_color, inner_rect, border_radius=3)
        else:
            pygame.draw.rect(self.surface, current_color, self.rect, border_radius=3)

        # Draw the text in the center of the button
        self.text.draw(self.rect.centerx, self.rect.centery, centered=True)

        # Draw the image (if set) in the center of the button
        if self.image:
            image_rect = self.image.get_rect(center=self.rect.center)
            self.surface.blit(self.image, image_rect)

    def is_clicked(self):
        mx, my = pygame.mouse.get_pos()
        if self.rect.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                return True
        return False

# Class used to create "underlays" behind the main content
class Background:
    def __init__(self, x, y, width, height, fill_color, border_color, border_radius, opacity, surface):
        if(x=="center"): # If the value of the x parameter is "center"
            x=(screenwidth/2) - (width/2) # This takes away half of the intended width of the element from half the screenwidth, thus centring it
        else:
            x=x
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = fill_color
        self.border_color = border_color
        self.border_radius = border_radius
        self.opacity = opacity
        self.surface = surface
        self.background_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.background_surface.set_alpha(self.opacity)

    def draw(self):
        # Fill the background surface with the fill color
        self.background_surface.fill((0, 0, 0, 0))  # Clear the surface
        pygame.draw.rect(self.background_surface, self.fill_color, self.background_surface.get_rect(), border_radius=self.border_radius)

        # Draw the border if the border color
        if self.border_color is not None:
            pygame.draw.rect(self.background_surface, self.border_color, self.background_surface.get_rect(), width=2, border_radius=self.border_radius)

        # Blit the background surface onto the main surface
        self.surface.blit(self.background_surface, self.rect.topleft)

class Car(pygame.sprite.Sprite):
    def __init__(self):  # constructor method for the vehicle
        super().__init__()  # initializes sprite class
        self.original_image = pygame.image.load('car.png')  # gets the image for the vehicle
        self.image = pygame.transform.rotozoom(self.original_image, 0, 0.1)  # scale the image down initially
        self.rect = self.image.get_rect(center=(390, 370))  # where the vehicle will appear initially
        self.angle = 0  # angle at which the vehicle is rotated initially
        self.rotation_speed = 1.8  # the speed at which the vehicle will rotate
        self.direction = 0  # initial direction force of the vehicle
        self.forward = pygame.math.Vector2(0, -1)
        self.active_forward = False  # controls if the car is accelerating forward
        self.active_reverse = False  # controls if the car is reversing
        self.reverse_speed = -1.5  # speed for reverse
        self.forward_speed = 3  # speed for forward movement

    def set_rotation(self):
        if self.active_forward or self.active_reverse:  # Only rotate if car is moving
            if self.direction == 1:  # if direction is turning right
                self.angle -= self.rotation_speed  # decrease the angle by the rotation speed
            if self.direction == -1:  # if direction is turning left
                self.angle += self.rotation_speed  # increase the angle by the rotation speed

            # Rotate the image and scale it down
            self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.1)
            self.rect = self.image.get_rect(center=self.rect.center)  # update the rect

    def get_rotation(self):
        if self.active_forward or self.active_reverse:  # Only adjust forward vector if car is moving
            if self.direction == 1:
                self.forward.rotate_ip(self.rotation_speed)
            if self.direction == -1:
                self.forward.rotate_ip(-self.rotation_speed)

    def accelerate(self):
        if self.active_forward:  # Forward movement
            self.rect.center += self.forward * self.forward_speed
        elif self.active_reverse:  # Reverse movement
            self.rect.center += self.forward * self.reverse_speed

    def update(self):
        self.set_rotation()  # call set_rotation to change the rotation of the vehicle
        self.get_rotation()
        self.accelerate()  # apply the movement depending on the state

# A variable to check for the status later
click = False

# called when level is selected through level selector
def game(level):
    running = True
    car = pygame.sprite.GroupSingle(Car()) # creates the group for the cars, with the sprite in the group
    map_filename = (str(level)+".png")
    if level==0:
        levelname = "Tutorial" # level 0 is the tutorial
    else:
        levelname = "Level",level
    levelmap = pygame.image.load('levels/'+map_filename) # import the map image

    settings_button = Button(670, 10, 40, 40, (128, 128, 128), (100, 100, 100), (100, 100, 100), 2, "", font, (255, 255, 255), screen, cog_image) # settings button displayed in the top right
    level_display = Button(0, 30, 110, 30,  (128, 128, 128), (128, 128, 128), (100, 100, 100), 2, levelname, font, (255, 255, 255), screen) # shows the level in the top left

    start_time = time.time()

    while running:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:  # when key is pressed
                if event.key == pygame.K_RIGHT:  # right button
                    car.sprite.direction += 1  # increment direction
                if event.key == pygame.K_LEFT:  # left button
                    car.sprite.direction -= 1  # decrement direction
                if event.key == pygame.K_UP:  # accelerate forward
                    car.sprite.active_forward = True
                if event.key == pygame.K_DOWN:  # reverse
                    car.sprite.active_reverse = True

            if event.type == KEYUP:  # when key is released
                if event.key == pygame.K_RIGHT:  # right button
                    car.sprite.direction -= 1  # decrement direction
                if event.key == pygame.K_LEFT:  # left button
                    car.sprite.direction += 1  # increment direction
                if event.key == pygame.K_UP:  # stop accelerating forwardd
                    car.sprite.active_forward = False
                if event.key == pygame.K_DOWN:  # stop reversing
                    car.sprite.active_reverse = False

        # Calculate the elapsed time
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)  # get the minutes
        seconds = int(elapsed_time % 60)  # get the seconds
        timer_display = f"{minutes}:{seconds:02d}"  # format the time as "0:00"

        screen.blit(levelmap, (0,0)) # copy the image onto the screen
        settings_button.draw()
        level_display.draw()
        
        timer_button = Button(0, 0, 110, 30, (128, 128, 128), (128, 128, 128), (100, 100, 100), 2, timer_display, font, (255, 255, 255), screen)
        timer_button.draw()
        
        car.draw(screen)
        car.update()

        # Check if the car is on the road
        car_position = car.sprite.rect.center  # get the car's position
        pixel_color = levelmap.get_at(car_position)[:3]  # Get the RGB value at the car's position

        if pixel_color in [(0,255,0)]:
            levelPass() # passed the level, placeholder
        else:
            if not isOnAllowedColor(pixel_color): # check if pixel colour underneath is not accepted road colour
                levelFail(level)  # show level fail screen

        if settings_button.is_clicked():
            settings(ingame=True)

        pygame.display.update()
        mainClock.tick(60)

def isOnAllowedColor(color):
    # tolerance range for colors
    road_color = (118, 114, 107)
    white_line_color = (254, 254, 254)
    tolerance = 10

    # check if colour is within the tolerance range for colours expected on road
    road_check = all(abs(color[i] - road_color[i]) <= tolerance for i in range(3))
    white_line_check = all(abs(color[i] - white_line_color[i]) <= tolerance for i in range(3))
    return road_check or white_line_check

def levelFail(current_level):
    # freeze the current game screen by taking a snapshot of the screen
    background = screen.copy()

    # underlay
    underlay = Background("center", 90, 330, 230, (255, 255, 255, 150), (0, 0, 0), 10, 180, screen)

    # define text
    fail_text = Text("Level failed!", font_40, (0, 0, 0), screen)
    
    # define buttons for retry and exit
    retry_button = Button("center", 180, 200, 50, (200, 0, 0), (255, 0, 0), (150, 0, 0), 2, "Retry", font, (255, 255, 255), screen)
    exit_button = Button("center", 240, 200, 50, (200, 0, 0), (255, 0, 0), (150, 0, 0), 2, "Exit", font, (255, 255, 255), screen)

    while True:
        # draw the background, buttons, text
        screen.blit(background, (0, 0)) # display background
        underlay.draw()
        fail_text.draw(screenwidth // 2, 130, centered=True)
        retry_button.draw()
        exit_button.draw()

        if retry_button.is_clicked():
            game(current_level)  # restart the game at the current level
        elif exit_button.is_clicked():
            main_menu()  # return to main menu

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        pygame.display.update()
        mainClock.tick(60)

# Main container function that holds the buttons and game functions
def main_menu():
    global click
    newsave_button = Button(10, 350, 200, 40,  (128, 128, 128), (100, 100, 100), (100, 100, 100), 2, "New Save", font, (255, 255, 255), screen)
    loadsave_button = Button(10, 300, 200, 40,  (128, 128, 128), (100, 100, 100), (100, 100, 100), 2, "Load Save", font, (255, 255, 255), screen)
    settings_button = Button(670, 80, 40, 40, (128, 128, 128), (100, 100, 100), (100, 100, 100), 2, "", font, (255, 255, 255), screen, cog_image)

    while True:
        screen.blit(background_image, (0,0))

        screen.blit(logo_image, ((screenwidth/2 - 200), 20))

        newsave_button.draw()
        loadsave_button.draw()
        settings_button.draw()

        if newsave_button.is_clicked():
            newSave()
        if loadsave_button.is_clicked():
            loadSave()
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

# called when the "Load Save" button is clicked
def loadSave():
    running = True
    filename="savefile.txt"
    file_path=os.path.join(current_directory, filename) # set the full path to the file
    
    # check if the file exists
    if os.path.exists(file_path): # if "savefile.txt" exists
        loadsave_success = True # set success as true (used for check in button direction)
        loadsave_message = Text("Save file successfully retrieved!", font_30, (0, 0, 0), screen) # creates success message
    else:
        loadsave_success = False
        loadsave_message = Text("Save file could not be retrieved!", font_30, (0, 0, 0), screen) # creates fail message

    while running:
        screen.blit(background_image, (0,0)) # background

        underlay = Background("center", 13, 330, 380, (255, 255, 255, 150), (0, 0, 0), 10, 180, screen) # gui background

        newsave_text = Text("Load Save", font_50, (0, 0, 0), screen) # gui title

        underlay.draw()
        newsave_text.draw(screenwidth // 2, 50, centered=True)
        loadsave_message.draw(screenwidth // 2, 180, centered=True)

        if loadsave_success is True: # if the file was successfully found
            nextbutton = Button("center", 220, 270, 45, (128, 128, 128), (100, 100, 100), (100, 100, 100), 2, "Level selection", font, (255, 255, 255), screen) # makes a button titled "level selection"
        else: # if the file was not found (needs to be made through newSave)

            nextbutton = Button("center", 220, 270, 45, (128, 128, 128), (100, 100, 100), (100, 100, 100), 2, "Create new save", font, (255, 255, 255), screen) # sets the nextbutton as "create new save"
        nextbutton.draw()

        if nextbutton.is_clicked(): # when the nextbutton is clicked on
            if(loadsave_success is True): # if the file exists
                selectionMenu() # takes the user to the selection menu
            else:
                newSave() # takes the user to the new save menu (save file will be generated through here)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


# called when the "New Save" button is clicked
def newSave():
    running = True
    while running:
        savefile = open ("savefile.txt", "w") # creates the file 'savefile.txt' in write mode
        savefile.write("1") # first level
        savefile.close()

        screen.blit(background_image, (0,0))

        underlay = Background("center", 13, 300, 380, (255, 255, 255, 150), (0, 0, 0), 10, 180, screen)

        newsave_text = Text("New Save", font_50, (0, 0, 0), screen)

        newsave_success1 = Text("New save file has been", font_30, (0, 0, 0), screen)
        newsave_success2 = Text("successfully created", font_30, (0, 0, 0), screen)

        levelselection = Button("center", 220, 270, 45, (128, 128, 128), (100, 100, 100), (100, 100, 100), 2, "Level selection", font, (255, 255, 255), screen)

        underlay.draw()
        newsave_text.draw(screenwidth // 2, 50, centered=True)
        newsave_success1.draw(screenwidth // 2, 170, centered=True)
        newsave_success2.draw(screenwidth // 2, 190, centered=True)
        levelselection.draw()
        
        if levelselection.is_clicked():
            selectionMenu()

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
def settings(ingame=False):
    running = True
    while running:
        screen.blit(background_image, (0,0)) # sets the background image

        # Settings menu title text
        settings_text = Text("Settings", font_50, (0, 0, 0), screen)

        # Create underlay design
        underlay = Background("center", 13, 300, 380, (255, 255, 255, 150), (0, 0, 0), 10, 180, screen)
    
        # Create button design
        howtoplay_button = Button("center", 100, 250, 45, (128, 128, 128), (100, 100, 100), (100, 100, 100), 2, "How to Play", font, (255, 255, 255), screen)
        mute_button = Button("center", 160, 250, 45, (128, 128, 128), (100, 100, 100), (100, 100, 100), 2, "Mute Sound", font, (255, 255, 255), screen)
        credits_button = Button("center", 220, 250, 45, (128, 128, 128), (100, 100, 100), (100, 100, 100), 2, "Credits", font, (255, 255, 255), screen)
        if ingame: # checks if the user has clicked the settings button from ingame
            quit_button = Button("center", 280, 250, 45, (128, 128, 128), (100, 100, 100), (100, 100, 100), 2, "Quit Level", font, (255, 255, 255), screen)
        else:
            quit_button = Button("center", 280, 250, 45, (100, 100, 100), (100, 100, 100), (100, 100, 100), 2, "Quit Level", font, (255, 255, 255), screen)

        # Show buttons, underlay on screen
        underlay.draw()
        settings_text.draw(screenwidth // 2, 50, centered=True)
        howtoplay_button.draw()
        mute_button.draw()
        credits_button.draw()
        quit_button.draw()

        if howtoplay_button.is_clicked():
            howToPlay()
        if mute_button.is_clicked():
            muteSound()
        if credits_button.is_clicked():
            credits()
        if ingame:
            if quit_button.is_clicked():
                quitLevel()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)

# This function is called when the "Credits" button on the settings page is clicked
def credits():
    running = True
    while running:
        screen.blit(background_image, (0,0)) # sets the background image

        # Credits menu title text
        page_title = Text("Credits", font_50, (0, 0, 0), screen)
        
        # Main content text
        line1 = Text("Created by", font_25, (0, 0, 0), screen)
        line2 = Text("Loran", font_40, (0, 0, 0), screen)
        line3 = Text("With thanks to", font_25, (0,0,0), screen)
        line4 = Text("Ms Lassami", font_40, (0,0,0), screen)
        line5 = Text("for teaching me", font_20, (0,0,0), screen)
        line6 = Text("And an honourable mention to", font_25, (0,0,0), screen)
        line7 = Text("Mr Lau", font_40, (0,0,0), screen)
        line8 = Text("the legend of computer science", font_20, (0,0,0), screen)

        # Create underlay design
        underlay = Background("center", 13, 300, 380, (255, 255, 255, 150), (0, 0, 0), 10, 180, screen)

        textline_xpos = screenwidth / 2 - 140

        underlay.draw()
        page_title.draw(screenwidth//2, 50, True)
        line1.draw(textline_xpos, 90)
        line2.draw(textline_xpos, 110)
        line3.draw(textline_xpos, 170)
        line4.draw(textline_xpos, 190)
        line5.draw(textline_xpos, 220)
        line6.draw(textline_xpos, 270)
        line7.draw(textline_xpos, 290)
        line8.draw(textline_xpos, 320)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


def howToPlay():
    running = True
    while running:
        screen.blit(background_image, (0,0)) # sets the background image

        # How to play menu title text
        page_title = Text("How to Play", font_50, (0, 0, 0), screen)

        # Create underlay design
        underlay = Background("center", 13, 300, 380, (255, 255, 255, 150), (0, 0, 0), 10, 180, screen)

        key_w = Button(220, 100, 50, 50, (128, 128, 128), (128, 128, 128), (100, 100, 100), 2, "W", font, (255, 255, 255), screen)
        text_w = Text("Accelerate the vehicle", font_30, (0, 0, 0), screen)

        key_s = Button(220, 160, 50, 50, (128, 128, 128), (128, 128, 128), (100, 100, 100), 2, "S", font, (255, 255, 255), screen)
        text_s = Text("Decelerate the vehicle", font_30, (0, 0, 0), screen)

        key_a = Button(220, 220, 50, 50, (128, 128, 128), (128, 128, 128), (100, 100, 100), 2, "A", font, (255, 255, 255), screen)
        text_a = Text("Steer the vehicle left", font_30, (0, 0, 0), screen)

        key_d = Button(220, 280, 50, 50, (128, 128, 128), (128, 128, 128), (100, 100, 100), 2, "D", font, (255, 255, 255), screen)
        text_d = Text("Steer the vehicle right", font_30, (0, 0, 0), screen)

        key_spacebar = Button(220, 340, 100, 50, (128, 128, 128), (128, 128, 128), (100, 100, 100), 2, "Spacebar", font, (255, 255, 255), screen)
        text_spacebar = Text("Handbrake", font_30, (0, 0, 0), screen)



        underlay.draw()
        
        key_w.draw()
        text_w.draw(280, 112.5)
        key_s.draw()
        text_s.draw(280, 172.5)
        key_a.draw()
        text_a.draw(280, 232.5)
        key_d.draw()
        text_d.draw(280, 292.5)
        key_spacebar.draw()
        text_spacebar.draw(340, 352.5)

        page_title.draw(screenwidth//2, 50, True)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        pygame.display.update()
        mainClock.tick(60)

def muteSound():
    running = True

def quitLevel():
    main_menu()


def selectionMenu():
    running = True
    while running:
        screen.blit(background_image, (0,0))

        placeholderimg = pygame.image.load('levelplaceholder.png')

        underlay = Background("center", 13, 700, 380, (255, 255, 255, 150), (0, 0, 0), 10, 180, screen)

        levelselection_text = Text("Level Selection", font_30, (0, 0, 0), screen)

        level0_img = Button(35, 60, 140, 80, (255, 255, 255), (255, 255, 255), (100, 100, 100), 2, "", font, (255, 255, 255), screen, placeholderimg)
        level0_text = Text("Tutorial level", font_20, (0, 0, 0), screen)

        level1_img = Button(205, 60, 140, 80, (255, 255, 255), (255, 255, 255), (100, 100, 100), 2, "", font, (255, 255, 255), screen, placeholderimg)
        level1_text = Text("Level 1", font_20, (0, 0, 0), screen)

        level2_img = Button(375, 60, 140, 80, (255, 255, 255), (255, 255, 255), (100, 100, 100), 2, "", font, (255, 255, 255), screen, placeholderimg)
        level2_text = Text("Level 2", font_20, (0, 0, 0), screen)
            
        level3_img = Button(545, 60, 140, 80, (255, 255, 255), (255, 255, 255), (100, 100, 100), 2, "", font, (255, 255, 255), screen, placeholderimg)
        level3_text = Text("Level 3", font_20, (0, 0, 0), screen)

        level4_img = Button(35, 170, 140, 80, (255, 255, 255), (255, 255, 255), (100, 100, 100), 2, "", font, (255, 255, 255), screen, placeholderimg)
        level4_text = Text("Level 4", font_20, (0, 0, 0), screen)

        level5_img = Button(205, 170, 140, 80, (255, 255, 255), (255, 255, 255), (100, 100, 100), 2, "", font, (255, 255, 255), screen, placeholderimg)
        level5_text = Text("Level 5", font_20, (0, 0, 0), screen)

        level6_img = Button(375, 170, 140, 80, (255, 255, 255), (255, 255, 255), (100, 100, 100), 2, "", font, (255, 255, 255), screen, placeholderimg)
        level6_text = Text("Level 6", font_20, (0, 0, 0), screen)
            
        level7_img = Button(545, 170, 140, 80, (255, 255, 255), (255, 255, 255), (100, 100, 100), 2, "", font, (255, 255, 255), screen, placeholderimg)
        level7_text = Text("Level 7", font_20, (0, 0, 0), screen)

        level8_img = Button(35, 280, 140, 80, (255, 255, 255), (255, 255, 255), (100, 100, 100), 2, "", font, (255, 255, 255), screen, placeholderimg)
        level8_text = Text("Level 8", font_20, (0, 0, 0), screen)

        level9_img = Button(205, 280, 140, 80, (255, 255, 255), (255, 255, 255), (100, 100, 100), 2, "", font, (255, 255, 255), screen, placeholderimg)
        level9_text = Text("Level 9", font_20, (0, 0, 0), screen)

        level10_img = Button(375, 280, 140, 80, (255, 255, 255), (255, 255, 255), (100, 100, 100), 2, "", font, (255, 255, 255), screen, placeholderimg)
        level10_text = Text("Level 10", font_20, (0, 0, 0), screen)
            
        level11_img = Button(545, 280, 140, 80, (255, 255, 255), (255, 255, 255), (100, 100, 100), 2, "", font, (255, 255, 255), screen, placeholderimg)
        level11_text = Text("Level 11", font_20, (0, 0, 0), screen)

        underlay.draw()
        levelselection_text.draw(110, 40, centered=True)

        level0_img.draw()
        level0_text.draw(35, 145)

        level1_img.draw()
        level1_text.draw(205, 145)

        level2_img.draw()
        level2_text.draw(375, 145)

        level3_img.draw()
        level3_text.draw(545, 145)

        level4_img.draw()
        level4_text.draw(35, 255)

        level5_img.draw()
        level5_text.draw(205, 255)

        level6_img.draw()
        level6_text.draw(375, 255)

        level7_img.draw()
        level7_text.draw(545, 255)

        level8_img.draw()
        level8_text.draw(35, 365)

        level9_img.draw()
        level9_text.draw(205, 365)

        level10_img.draw()
        level10_text.draw(375, 365)

        level11_img.draw()
        level11_text.draw(545, 365)

        if level0_img.is_clicked():
            game(0)
        
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
