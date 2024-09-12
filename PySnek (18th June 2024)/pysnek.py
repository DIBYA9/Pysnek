required_modules = {'pygame':'pygame'}

import subprocess, sys, os, time
import pygame, time
#import termcolor as concolor
from random import randrange


LOCK_FILE = 'game.lock'
WINDOW = 400
TILE_SIZE = 18
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE) # (start, stop, step) for random position generation
timer = 10

get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)] #Lambda function to generate a random position

highscore = 0
score = 0
keys = {pygame.K_UP: 0, pygame.K_DOWN: 0, pygame.K_LEFT: 0, pygame.K_RIGHT: 0}
last_key_press_time = 0
current_time = time.time()
key_press_delay = 0.05

snake = pygame.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2]) # Snake's head
snake.center = get_random_position() # Initial position of the snake
length = 1 # Length of the snake
segments = [snake.copy()]  # List of segments of the snake
snake_dir = (0, 0)  # Direction of the snake (x, y)

bg_org = pygame.image.load('home-gameover_bg.png')
bg = pygame.transform.scale(bg_org,(400,400))

startop_bg_org = pygame.image.load('startop_bg.png')
startop_bg = pygame.transform.scale(startop_bg_org,(400,400))



credits_bg = pygame.image.load('credits.png')

food1 = pygame.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
food2 = pygame.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
food3 = pygame.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
food4 = pygame.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
food5 = pygame.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
food6 = pygame.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
'''org_apple = pygame.image.load('food.png')
apple = pygame.transform.scale(org_apple,(50,50))
apple_rect = apple.get_rect()'''
food1.center = get_random_position()
food2.center = get_random_position()
food3.center = get_random_position()
food4.center = get_random_position()
food5.center = get_random_position()
food6.center = get_random_position()
#apple_rect.center = get_random_position()


def button_hover(button_rect): #Function to check if the mouse is hovering over a button
    mouse_pos = pygame.mouse.get_pos() #Get the mouse position
    return button_rect.collidepoint(mouse_pos) #Return True if the mouse is hovering over the button

def button_click(button_rect): #Function to check if the button is clicked
    mouse_pos = pygame.mouse.get_pos() #Get the mouse position
    mouse_click = pygame.mouse.get_pressed() #Get the mouse click
    return button_rect.collidepoint(mouse_pos) and mouse_click[0] #Return True if the button is clicked



'''def raise_error(msg): #Function to raise an error
    print(concolor.colored(str(msg),'red')) #Print the message in red color'''

def display_score():
    score_text = font.render(f'{score}', True, (255, 255, 255))
    screen.blit(score_text, (60, 10))

def display_highscore():
    score_text = font.render(f'{highscore}', True, (255, 255, 255))
    screen.blit(score_text, (240, 10))

def play_sound(filename, loop=0): #Function to play a sound file
    pygame.mixer.init() #Initialize the mixer
    pygame.mixer.music.load(filename) #Load the sound file
    pygame.mixer.music.play(loop) #Play the sound file for the specified number of loops

def play_sfx(filename, loop=0): #Function to play a sound effect
    pygame.mixer.Sound(filename).play(loop) #Play the sound effect

def create_lock_file(): #Function to create a lock file
    LOCK_FILE = open('game.lock','w') #Create a file named game.lock
    LOCK_FILE.write('') #Write an empty string to the file

def is_game_running(): #Function to check if the game is already running
    return os.path.exists(LOCK_FILE) #Return True if the path to the game.lock file exists

def delete_lock_file(): #Function to delete the lock file
    if  os.path.exists(LOCK_FILE): #If the game is running
        os.remove(LOCK_FILE) #Remove the game.lock file

def pysnek_init():
    global WINDOW, TILE_SIZE, RANGE, get_random_position, highscore, score, key_press_delay, keys, last_key_press_time, current_time, length, segments, snake_dir

    WINDOW = 400
    TILE_SIZE = 18
    RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE) # (start, stop, step) for random position generation

    get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)] #Lambda function to generate a random position

    score = 0
    keys = {pygame.K_UP: 0, pygame.K_DOWN: 0, pygame.K_LEFT: 0, pygame.K_RIGHT: 0}
    last_key_press_time = 0
    current_time = time.time()
    key_press_delay = 0.05
    snake.center = get_random_position() # Initial position of the snake
    length = 1 # Length of the snake
    del segments[:]
    segments = [snake.copy()]  # List of segments of the snake
    snake_dir = (0, 0)  # Direction of the snake (x, y)

    food1 = pygame.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
    '''org_apple = pygame.image.load('food.png')
    apple = pygame.transform.scale(org_apple,(50,50))
    apple_rect = apple.get_rect()'''
    food1.center = get_random_position()
    #apple_rect.center = get_random_position()

if is_game_running():
    raise_error("One instance of the game can only be run.")
    exit()
else:
    create_lock_file()

'''main_dir = os.path.split(os.path.abspath(__file__))[0] 
print(f"{main_dir}")'''



try:
    cfgfile = open('config.ini','r')
except FileNotFoundError:
    cfgfile = open('config.ini', 'w+')
try:  
    try:
        highscore = int(cfgfile.readline())
        ##WINDOW = int(cfgfile.readline())
    except ValueError:
        highscore = 0
        #WINDOW = 400
except EOFError:
    pass
cfgfile.close()
cfgfile = open('config.ini','w+')


pygame.init()

menu = 'intro1'
last_menu = ''

intro = 1

font = pygame.font.Font('pixels.woff', 30) #Font object
font2 = pygame.font.Font('pixels.woff', 20) #Font object
font2_mini = pygame.font.Font('pixels.woff', 13) #Font object
font3 = pygame.font.Font('pixels.woff', 40) #Font object
font4 = pygame.font.Font('pixels.woff', 40) #Font object

icon = pygame.image.load('icon.png') #Load the icon image
org_logo = pygame.image.load('logo.png') #Load the logo image
logo = pygame.transform.scale(org_logo,(220,80)) #Scale the logo image to 200x200 pixels
org_made_with = pygame.image.load('made_with_pygame.png') #Load the made with pygame image
made_with = pygame.transform.scale(org_made_with,(200,30)) #Scale the made with pygame image to 200x30 pixels
org_trophy = pygame.image.load('trophy.png') #Load the trophy image
trophy = pygame.transform.scale(org_trophy,(30,30)) #Scale the trophy image to 30x30 pixels
org_apple = pygame.image.load('food.png')
apple = pygame.transform.scale(org_apple, (50, 50))
org_sad_pysnek = pygame.image.load('gameover_sadpysnek.png')
sad_pysnek = pygame.transform.scale(org_sad_pysnek, (80, 80))



org_play_button = pygame.image.load('home_startbutton.png') #Load the play button image
play_button = pygame.transform.scale(org_play_button,(110,60)) #Scale the play button image to 90x60 pixels
play_button_rect = pygame.Surface.get_rect(play_button) #Get the rectangle object of the play button
play_button_rect.center = (204, 230) #Set the center of the play button to (204, 230)

org_credits_button = pygame.image.load('creditsbutton.png') #Load the play button image
credits_button = pygame.transform.scale(org_credits_button,(110,60)) #Scale the play button image to 90x60 pixels
credits_button_rect = pygame.Surface.get_rect(credits_button) #Get the rectangle object of the play button
credits_button_rect.center = (204, 295) #Set the center of the play button to (204, 230)

org_play_frominst_button = pygame.image.load('gameover_replaybutton.png') #Load the play button image
play_frominst_button = pygame.transform.scale(org_play_frominst_button,(110,60)) #Scale the play button image to 90x60 pixels
play_frominst_button_rect = pygame.Surface.get_rect(play_frominst_button) #Get the rectangle object of the play button
play_frominst_button_rect.center = (0, 0) #Set the center of the play button to (70, 100)

org_play_easy_button = pygame.image.load('easy_button.png') #Load the play button image
play_easy_button = pygame.transform.scale(org_play_easy_button,(110,60)) #Scale the play button image to 90x60 pixels
play_easy_button_rect = pygame.Surface.get_rect(play_easy_button) #Get the rectangle object of the play button
play_easy_button_rect.center = (70, 100) #Set the center of the play button to (70, 100)

org_play_hard_button = pygame.image.load('hard_button.png') #Load the play button image
play_hard_button = pygame.transform.scale(org_play_hard_button,(110,60)) #Scale the play button image to 90x60 pixels
play_hard_button_rect = pygame.Surface.get_rect(play_hard_button) #Get the rectangle object of the play button
play_hard_button_rect.center = (70, 220) #Set the center of the play button to (70, 100)

org_quit_button = pygame.image.load('quit_norm.png')
quit_button = pygame.transform.scale(org_quit_button,(60,60))
quit_button_rect = pygame.Surface.get_rect(quit_button)
quit_button_rect.center = (368, 30)

org_restart_button = pygame.image.load('gameover_replaybutton.png') #Load the restart button image
restart_button = pygame.transform.scale(org_restart_button,(110,60)) #Scale the restart button image to 90x60 pixels
restart_button_rect = pygame.Surface.get_rect(restart_button) #Get the rectangle object of the restart button
restart_button_rect.center = (194, 300) #Set the center of the restart button to (396, 452)

org_back_button = pygame.image.load('backbutton.png') #Load the restart button image
back_button = pygame.transform.scale(org_back_button,(110,60)) #Scale the restart button image to 90x60 pixels
back_button_rect = pygame.Surface.get_rect(back_button) #Get the rectangle object of the restart button
back_button_rect.center = (194, 370) #Set the center of the restart button to (396, 452)


screen = pygame.display.set_mode([WINDOW] * 2) #Creates a window of WINDOW x WINDOW pixels
pygame.display.set_caption('PySnek') #Sets the title of the window
pygame.display.set_icon(icon) #Sets the icon of the window
clock = pygame.time.Clock() #Creates a clock object to control the frame rate
intro1 = pygame.image.load('intro1.png').convert_alpha()
intro2 = pygame.image.load('intro2.png')

play_music = 0
cfgfile.seek(0) #Move the file pointer to the beginning of the file

intro_tick = 0
mode = ''
intro1_y = -120
intro1_alpha = 0

play_sfx('start_intro.mp3')
while intro == 1:
    if menu == 'intro1':
            for event in pygame.event.get(): #Iterate over the events in the event queue of pygame
                    if event.type == pygame.QUIT: #If the user closes the window using the close button
                        cfgfile.close() #Close the config.ini file
                        cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                        cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                        pygame.quit() #Quit the pygame
                        cfgfile.close() #Close the config.ini file
                        delete_lock_file() #Delete the lock file
                        exit() #Exit the program


            if intro1_y < 0 :
                intro1_y += 1
                screen.blit(intro1, (0,intro1_y))

            '''faded_intro1 = intro1.copy()
            faded_into1.set_alpha(alpha_value)'''

            
                      
            screen.blit(intro1, (0,intro1_y))
            intro_tick += 1
  
            
            pygame.display.update() #Update the display
            clock.tick(60) #Control the frame rate of the game
            
            if intro_tick > 300:
                menu = 'intro2'
                intro_tick = 0
                
    if menu == 'intro2':
            for event in pygame.event.get(): #Iterate over the events in the event queue of pygame
                    if event.type == pygame.QUIT: #If the user closes the window using the close button
                        cfgfile.close() #Close the config.ini file
                        cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                        cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                        pygame.quit() #Quit the pygame
                        cfgfile.close() #Close the config.ini file
                        delete_lock_file() #Delete the lock file
                        exit() #Exit the program
                        
            screen.blit(intro2, (0,0))
            intro_tick += 1

            
            pygame.display.update() #Update the display
            clock.tick(60) #Control the frame rate of the game
            
            if intro_tick > 200:
                menu = 'main'
                intro = 0
                intro_tick = 0
            

            
while True:
    try:
        #print(pygame.mouse.get_pos())
        if menu == 'game':
            if mode == 'easy':   
                if score > highscore: #If the current score is greater than the highscore
                    highscore = score #Set the highscore to the current score
        
                for event in pygame.event.get(): #Iterate over the events in the event queue of pygame
                    if event.type == pygame.QUIT: #If the user closes the window using the close button
                        menu = 'over'
                        play_sound('over.mp3')
                        cfgfile.close() #Close the config.ini file
                        cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                        cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                        cfgfile.close() #Close the config.ini file
                        delete_lock_file() #Delete the lock file
                        pygame.display.update()
                        exit()
                
                    if event.type == pygame.KEYDOWN: #If a key is pressed  
                        if event.key == pygame.K_UP and snake_dir != (0, TILE_SIZE): #If the key is UP arrow key and the snake is not moving down
                            snake_dir = (0, -TILE_SIZE) #Change the direction of the snake to up
                            keys = {key: (event.key == key) for key in keys}
                        if event.key == pygame.K_DOWN and snake_dir != (0, -TILE_SIZE): #If the key is DOWN arrow key and the snake is not moving up
                            snake_dir = (0, TILE_SIZE) #Change the direction of the snake to down
                            keys = {key: (event.key == key) for key in keys}
                        if event.key == pygame.K_LEFT and snake_dir != (TILE_SIZE, 0): #If the key is LEFT arrow key and the snake is not moving right
                            snake_dir = (-TILE_SIZE, 0) #Change the direction of the snake to left
                            keys = {key: (event.key == key) for key in keys}
                        if event.key == pygame.K_RIGHT and snake_dir != (-TILE_SIZE, 0): #If the key is RIGHT arrow key and the snake is not moving left
                            snake_dir = (TILE_SIZE, 0) #Change the direction of the snake to right
                            keys = {key: (event.key == key) for key in keys}

                        '''current_time = time.time() #Get the current time
                        print(f'{current_time-last_key_press_time}>={key_press_delay}')
                        if current_time-last_key_press_time >= key_press_delay:
                            if not any(keys.values()):
                                if event.key == pygame.K_UP and snake_dir != (0, TILE_SIZE): #If the key is UP arrow key and the snake is not moving down
                                    snake_dir = (0, -TILE_SIZE) #Change the direction of the snake to up
                                    keys = {key: (event.key == key) for key in keys}
                                if event.key == pygame.K_DOWN and snake_dir != (0, -TILE_SIZE): #If the key is DOWN arrow key and the snake is not moving up
                                    snake_dir = (0, TILE_SIZE) #Change the direction of the snake to down
                                    keys = {key: (event.key == key) for key in keys}
                                if event.key == pygame.K_LEFT and snake_dir != (TILE_SIZE, 0): #If the key is LEFT arrow key and the snake is not moving right
                                    snake_dir = (-TILE_SIZE, 0) #Change the direction of the snake to left
                                    keys = {key: (event.key == key) for key in keys}
                                if event.key == pygame.K_RIGHT and snake_dir != (-TILE_SIZE, 0): #If the key is RIGHT arrow key and the snake is not moving left
                                    snake_dir = (TILE_SIZE, 0) #Change the direction of the snake to right
                                    keys = {key: (event.key == key) for key in keys}
                                last_key_press_time = current_time'''

            

                snake.move_ip(snake_dir) #Move the snake in the direction of snake_dir by one step (TILE_SIZE)

     
                if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW: #If the snake hits the wall of the window 
                    menu = 'over'
                    play_sound('over.mp3')
                    time.sleep(1)
                    cfgfile.close() #Close the config.ini file
                    cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                    cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                    cfgfile.close() #Close the config.ini file
                    delete_lock_file() #Delete the lock file
                    pygame.display.update()
                

                segments.append(snake.copy()) #Append the head of the snake to the segments list to create a new segment of the snake
                segments = segments[-length:] #Keep only the last 'length' segments of the snake to maintain the length of the snake

                if snake.colliderect(food1): #If the snake eats the food 
                    play_sfx('eat.mp3') #Play the eat sound
                    food1.center = get_random_position() #Generate a new random position for the food
                    food3.center = get_random_position() #Generate a new random position for the food
                    food4.center = get_random_position() #Generate a new random position for the food
                    food5.center = get_random_position() #Generate a new random position for the food
                    food6.center = get_random_position() #Generate a new random position for the food
                    length += 1 #Increase the length of the snake
                    score += 1 #Increase the score by 1
                if snake.colliderect(food2): #If the snake eats the food 
                    play_sfx('eat.mp3') #Play the eat sound
                    food2.center = get_random_position() #Generate a new random position for the food
                    food3.center = get_random_position() #Generate a new random position for the food
                    food4.center = get_random_position() #Generate a new random position for the food
                    food5.center = get_random_position() #Generate a new random position for the food
                    food6.center = get_random_position() #Generate a new random position for the food
                    length += 1 #Increase the length of the snake
                    score += 2 #Increase the score by 1
                if snake.colliderect(food3): #If the snake eats the food 
                    menu = 'over'
                    play_sound('over.mp3')
                    time.sleep(1)
                    cfgfile.close() #Close the config.ini file
                    cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                    cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                    cfgfile.close() #Close the config.ini file
                    delete_lock_file() #Delete the lock file
                    pygame.display.update()
                if snake.colliderect(food4): #If the snake eats the food 
                    menu = 'over'
                    play_sound('over.mp3')
                    time.sleep(1)
                    cfgfile.close() #Close the config.ini file
                    cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                    cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                    cfgfile.close() #Close the config.ini file
                    delete_lock_file() #Delete the lock file
                    pygame.display.update()
                if snake.colliderect(food5): #If the snake eats the food 
                    menu = 'over'
                    play_sound('over.mp3')
                    time.sleep(1)
                    cfgfile.close() #Close the config.ini file
                    cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                    cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                    cfgfile.close() #Close the config.ini file
                    delete_lock_file() #Delete the lock file
                    pygame.display.update()
                if snake.colliderect(food6): #If the snake eats the food 
                    menu = 'over'
                    play_sound('over.mp3')
                    time.sleep(1)
                    cfgfile.close() #Close the config.ini file
                    cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                    cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                    cfgfile.close() #Close the config.ini file
                    delete_lock_file() #Delete the lock file
                    pygame.display.update()  
                
                

                if len(segments) != len(set((seg.left, seg.top) for seg in segments)): #If the snake collides with itself 
                    play_sound('over.mp3') #Play the game over sound
                    time.sleep(1) #Wait for 1 second
                    menu = 'over'
                    cfgfile.close() #Close the config.ini file
                    cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                    cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                    cfgfile.close() #Close the config.ini file
                    delete_lock_file() #Delete the lock file
                    pygame.display.update()
                

                screen.fill('black') #Fill the screen with black color

                #screen.blit(apple, apple_rect.center)
               

                pygame.draw.rect(screen, 'red', food1) #Draw the food on the screen with red color using the food1 rectangle
                pygame.draw.rect(screen, 'yellow', food2) #Draw the food on the screen with red color using the food1 rectangle
                pygame.draw.rect(screen, 'white', food3) #Draw the food on the screen with red color using the food1 rectangle
                pygame.draw.rect(screen, 'white', food4) #Draw the food on the screen with red color using the food1 rectangle
                pygame.draw.rect(screen, 'white', food5) #Draw the food on the screen with red color using the food1 rectangle
                pygame.draw.rect(screen, 'white', food6) #Draw the food on the screen with red color using the food1 rectangle
        
                 # Draw the snake segments
                for i, segment in enumerate(segments): #Iterate over the segments of the snake
                    if i == length-1:  #The head of the snake 
                        pygame.draw.rect(screen, (0, 64, 0), segment)  # Dark green color
                    elif i == 0: #he tail of the snake
                        pygame.draw.rect(screen, (60, 94, 32), segment)  # Sap green color
                    else:  #The body of the snake
                        pygame.draw.rect(screen, (0, 128, 0), segment)  # Green color

                display_score() 
                display_highscore()
            
                screen.blit(trophy, (200,10)) #Display the trophy image at (200, 10) position
                screen.blit(apple, (5, 0))
                pygame.display.update() #Update the display

                if score < 10:
                    speed = 10 
                elif score < 30:
                    speed = 15
                elif score < 150:
                    speed = 20
                else:
                    speed = 25 

                clock.tick(speed) #Control the frame rate of the game
                
  
            if mode == 'hard':

                speed=20
                
                if score > highscore: #If the current score is greater than the highscore
                    highscore = score #Set the highscore to the current score
        
                for event in pygame.event.get(): #Iterate over the events in the event queue of pygame
                    if event.type == pygame.QUIT: #If the user closes the window using the close button
                        menu = 'over'
                        play_sound('over.mp3')
                        cfgfile.close() #Close the config.ini file
                        cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                        cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                        cfgfile.close() #Close the config.ini file
                        delete_lock_file() #Delete the lock file
                        pygame.display.update()
                        exit()
                
                    if event.type == pygame.KEYDOWN: #If a key is pressed  
                        if event.key == pygame.K_UP and snake_dir != (0, TILE_SIZE): #If the key is UP arrow key and the snake is not moving down
                            snake_dir = (0, -TILE_SIZE) #Change the direction of the snake to up
                            keys = {key: (event.key == key) for key in keys}
                        if event.key == pygame.K_DOWN and snake_dir != (0, -TILE_SIZE): #If the key is DOWN arrow key and the snake is not moving up
                            snake_dir = (0, TILE_SIZE) #Change the direction of the snake to down
                            keys = {key: (event.key == key) for key in keys}
                        if event.key == pygame.K_LEFT and snake_dir != (TILE_SIZE, 0): #If the key is LEFT arrow key and the snake is not moving right
                            snake_dir = (-TILE_SIZE, 0) #Change the direction of the snake to left
                            keys = {key: (event.key == key) for key in keys}
                        if event.key == pygame.K_RIGHT and snake_dir != (-TILE_SIZE, 0): #If the key is RIGHT arrow key and the snake is not moving left
                            snake_dir = (TILE_SIZE, 0) #Change the direction of the snake to right
                            keys = {key: (event.key == key) for key in keys}

                        '''current_time = time.time() #Get the current time
                        print(f'{current_time-last_key_press_time}>={key_press_delay}')
                        if current_time-last_key_press_time >= key_press_delay:
                            if not any(keys.values()):
                                if event.key == pygame.K_UP and snake_dir != (0, TILE_SIZE): #If the key is UP arrow key and the snake is not moving down
                                    snake_dir = (0, -TILE_SIZE) #Change the direction of the snake to up
                                    keys = {key: (event.key == key) for key in keys}
                                if event.key == pygame.K_DOWN and snake_dir != (0, -TILE_SIZE): #If the key is DOWN arrow key and the snake is not moving up
                                    snake_dir = (0, TILE_SIZE) #Change the direction of the snake to down
                                    keys = {key: (event.key == key) for key in keys}
                                if event.key == pygame.K_LEFT and snake_dir != (TILE_SIZE, 0): #If the key is LEFT arrow key and the snake is not moving right
                                    snake_dir = (-TILE_SIZE, 0) #Change the direction of the snake to left
                                    keys = {key: (event.key == key) for key in keys}
                                if event.key == pygame.K_RIGHT and snake_dir != (-TILE_SIZE, 0): #If the key is RIGHT arrow key and the snake is not moving left
                                    snake_dir = (TILE_SIZE, 0) #Change the direction of the snake to right
                                    keys = {key: (event.key == key) for key in keys}
                                last_key_press_time = current_time'''

            

                snake.move_ip(snake_dir) #Move the snake in the direction of snake_dir by one step (TILE_SIZE)

     
                if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW: #If the snake hits the wall of the window 
                    menu = 'over'
                    play_sound('over.mp3')
                    time.sleep(1)
                    cfgfile.close() #Close the config.ini file
                    cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                    cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                    cfgfile.close() #Close the config.ini file
                    delete_lock_file() #Delete the lock file
                    pygame.display.update()
                

                segments.append(snake.copy()) #Append the head of the snake to the segments list to create a new segment of the snake
                segments = segments[-length:] #Keep only the last 'length' segments of the snake to maintain the length of the snake

                if snake.colliderect(food1): #If the snake eats the food 
                    play_sfx('eat.mp3') #Play the eat sound
                    food1.center = get_random_position() #Generate a new random position for the food
                    food3.center = get_random_position() #Generate a new random position for the food
                    food4.center = get_random_position() #Generate a new random position for the food
                    food5.center = get_random_position() #Generate a new random position for the food
                    food6.center = get_random_position() #Generate a new random position for the food
                    length += 1 #Increase the length of the snake
                    score += 1 #Increase the score by 1
                if snake.colliderect(food2): #If the snake eats the food 
                    play_sfx('eat.mp3') #Play the eat sound
                    food2.center = get_random_position() #Generate a new random position for the food
                    food3.center = get_random_position() #Generate a new random position for the food
                    food4.center = get_random_position() #Generate a new random position for the food
                    food5.center = get_random_position() #Generate a new random position for the food
                    food6.center = get_random_position() #Generate a new random position for the food
                    length += 1 #Increase the length of the snake
                    score += 2 #Increase the score by 1
                if snake.colliderect(food3): #If the snake eats the food 
                    menu = 'over'
                    play_sound('over.mp3')
                    time.sleep(1)
                    cfgfile.close() #Close the config.ini file
                    cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                    cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                    cfgfile.close() #Close the config.ini file
                    delete_lock_file() #Delete the lock file
                    pygame.display.update()
                if snake.colliderect(food4): #If the snake eats the food 
                    menu = 'over'
                    play_sound('over.mp3')
                    time.sleep(1)
                    cfgfile.close() #Close the config.ini file
                    cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                    cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                    cfgfile.close() #Close the config.ini file
                    delete_lock_file() #Delete the lock file
                    pygame.display.update()
                if snake.colliderect(food5): #If the snake eats the food 
                    menu = 'over'
                    play_sound('over.mp3')
                    time.sleep(1)
                    cfgfile.close() #Close the config.ini file
                    cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                    cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                    cfgfile.close() #Close the config.ini file
                    delete_lock_file() #Delete the lock file
                    pygame.display.update()
                if snake.colliderect(food6): #If the snake eats the food 
                    menu = 'over'
                    play_sound('over.mp3')
                    time.sleep(1)
                    cfgfile.close() #Close the config.ini file
                    cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                    cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                    cfgfile.close() #Close the config.ini file
                    delete_lock_file() #Delete the lock file
                    pygame.display.update()  

                if len(segments) != len(set((seg.left, seg.top) for seg in segments)): #If the snake collides with itself 
                    play_sound('over.mp3') #Play the game over sound
                    time.sleep(1) #Wait for 1 second
                    menu = 'over'
                    cfgfile.close() #Close the config.ini file
                    cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                    cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                    cfgfile.close() #Close the config.ini file
                    delete_lock_file() #Delete the lock file
                    pygame.display.update()
                

                screen.fill('black') #Fill the screen with black color

                #screen.blit(apple, apple_rect.center)
               

                pygame.draw.rect(screen, 'red', food1) #Draw the food on the screen with red color using the food1 rectangle
                pygame.draw.rect(screen, 'yellow', food2) #Draw the food on the screen with red color using the food1 rectangle
                pygame.draw.rect(screen, 'white', food3) #Draw the food on the screen with red color using the food1 rectangle
                pygame.draw.rect(screen, 'white', food4) #Draw the food on the screen with red color using the food1 rectangle
                pygame.draw.rect(screen, 'white', food5) #Draw the food on the screen with red color using the food1 rectangle
                pygame.draw.rect(screen, 'white', food6) #Draw the food on the screen with red color using the food1 rectangle
        
                 # Draw the snake segments
                for i, segment in enumerate(segments): #Iterate over the segments of the snake
                    if i == length-1:  #The head of the snake 
                        pygame.draw.rect(screen, (0, 64, 0), segment)  # Dark green color
                    elif i == 0: #he tail of the snake
                        pygame.draw.rect(screen, (60, 94, 32), segment)  # Sap green color
                    else:  #The body of the snake
                        pygame.draw.rect(screen, (0, 128, 0), segment)  # Green color

                display_score() 
                display_highscore()
            
                screen.blit(trophy, (200,10)) #Display the trophy image at (200, 10) position
                screen.blit(apple, (5, 0))
                pygame.display.update() #Update the display

                speed = 20

                clock.tick(speed) #Control the frame rate of the game
                

        elif menu == 'main':
                    
                    if play_music == 0:
                        play_sound('music.mp3', -1) #Play the background music with infinite loop (-1)
                        play_music = 1
                    
                    for event in pygame.event.get(): #Iterate over the events in the event queue of pygame
                        if event.type == pygame.QUIT: #If the user closes the window using the close button
                            cfgfile.close() #Close the config.ini file
                            cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                            cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                            pygame.quit() #Quit the pygame
                            cfgfile.close() #Close the config.ini file
                            delete_lock_file() #Delete the lock file
                            exit() #Exit the program

                    
                    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 400, 800)) #Fill the screen with black color (RGB: 0, 0, 0) at (0, 0) position with width 400 and height 800
                    screen.blit(bg,(0,0))
                    
                    screen.blit(play_button, play_button_rect) #Display the play button on the screen at the center of the screen
                    if button_hover(play_button_rect): #If the mouse is hovering over the play button 
                        play_button.set_alpha(200) #Fade the play button to 200 alpha
                        if button_click(play_button_rect): #If the play button is clicked
                            #play_sfx('click.mp3')
                            menu = 'start_ops' #Change the menu to start_ops
                    else:
                        play_button.set_alpha(255) #Make the button opaque (alpha 255)

                    screen.blit(credits_button, credits_button_rect) #Display the play button on the screen at the center of the screen
                    if button_hover(credits_button_rect): #If the mouse is hovering over the play button 
                        credits_button.set_alpha(200) #Fade the play button to 200 alpha
                        if button_click(credits_button_rect): #If the play button is clicked
                            #play_sfx('click.mp3')
                            menu = 'credits' #Change the menu to start_ops
                    else:
                        credits_button.set_alpha(255) #Make the button opaque (alpha 255)

                    screen.blit(quit_button, quit_button_rect) #Display the quit button on the screen at the center of the screen
                    if button_hover(quit_button_rect): #If the mouse is hovering over the quit button
                        quit_button.set_alpha(200) #Fade the quit button to 200 alpha
                        if button_click(quit_button_rect): #If the quit button is clicked
                            #play_sfx('click.mp3')
                            cfgfile.close() #Close the config.ini file
                            cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                            cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                            pygame.quit() #Quit the pygame
                            cfgfile.close() #Close the config.ini file
                            delete_lock_file() #Delete the lock file
                            time.sleep(1) #Wait for 1 second
                            exit() #Exit the program
                    else:
                        quit_button.set_alpha(255) #Make the button opaque (alpha 255)

                    copyright_text = font2.render('The first collaboration project of Collab_1 Division of CodingUHub group', True, (255, 255, 255)) #Render the text with white color and antialiasing enabled (True)
                    copyright_text_2 = font2.render('under UBSR', True, (255, 255, 255)) #Render the text with white color and antialiasing enabled (True)
                    copyright_text_3 = font2.render('Shouneel Ghosh, Pratyush Chanda and Dibyadip Mitra', True, (255, 255, 255)) #Render the text with white color and antialiasing enabled (True)
                    screen.blit(copyright_text, (6, 747)) #Display the text on the screen at (6, 787)
                    screen.blit(copyright_text_2, (6, 767)) #Display the text on the screen at (6, 797)
                    screen.blit(copyright_text_3, (6, 787)) #Display the text on the screen at (6, 797)

                    highscore_home = font2.render(f'Best score: {highscore}', True, (255, 255, 255))
                    screen.blit(highscore_home, (130, 335))
                    screen.blit(logo, (90, 84))
                    screen.blit(made_with, (110, 360))

        elif menu == 'start_ops':
                    
                    
                    for event in pygame.event.get(): #Iterate over the events in the event queue of pygame
                        if event.type == pygame.QUIT: #If the user closes the window using the close button
                            cfgfile.close() #Close the config.ini file
                            cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                            cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                            pygame.quit() #Quit the pygame
                            cfgfile.close() #Close the config.ini file
                            delete_lock_file() #Delete the lock file
                            exit() #Exit the program

                    
                    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 400, 800)) #Fill the screen with black color (RGB: 0, 0, 0) at (0, 0) position with width 400 and height 800
                    screen.blit(startop_bg,(0,0))
                    
                    screen.blit(play_easy_button, play_easy_button_rect) #Display the play button on the screen at the center of the screen
                    if button_hover(play_easy_button_rect): #If the mouse is hovering over the play button 
                        play_easy_button.set_alpha(200) #Fade the play button to 200 alpha
                        if button_click(play_easy_button_rect): #If the play button is clicked
                            #play_sfx('click.mp3')
                            menu = 'game' #Change the menu to start_ops
                            mode = 'easy'
                    else:
                        play_easy_button.set_alpha(255) #Make the button opaque (alpha 255)
                        
                    screen.blit(play_hard_button, play_hard_button_rect) #Display the play button on the screen at the center of the screen
                    if button_hover(play_hard_button_rect): #If the mouse is hovering over the play button 
                        play_hard_button.set_alpha(200) #Fade the play button to 200 alpha
                        if button_click(play_hard_button_rect): #If the play button is clicked
                            #play_sfx('click.mp3')
                            menu = 'game' #Change the menu to start_ops
                            mode = 'hard'
                    else:
                        play_hard_button.set_alpha(255) #Make the button opaque (alpha 255)


                    screen.blit(quit_button, quit_button_rect) #Display the quit button on the screen at the center of the screen
                    if button_hover(quit_button_rect): #If the mouse is hovering over the quit button
                        quit_button.set_alpha(200) #Fade the quit button to 200 alpha
                        if button_click(quit_button_rect): #If the quit button is clicked
                            #play_sfx('click.mp3')
                            cfgfile.close() #Close the config.ini file
                            cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                            cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                            pygame.quit() #Quit the pygame
                            cfgfile.close() #Close the config.ini file
                            delete_lock_file() #Delete the lock file
                            time.sleep(1) #Wait for 1 second
                            exit() #Exit the program
                    else:
                        quit_button.set_alpha(255) #Make the button opaque (alpha 255)

                    inst_easy_text = font2_mini.render('You play the game!', True, (255, 255, 255)) #Render the text with white color and antialiasing enabled (True)
                    inst_easy_text_2 = font2_mini.render('Use the arrow keys to move the snake', True, (255, 255, 255)) #Render the text with white color and antialiasing enabled (True)
                    inst_easy_text_3 = font2_mini.render('Eat the apples to increase your score,', True, (255, 255, 255)) #Render the text with white color and antialiasing enabled (True)
                    inst_easy_text_4 = font2_mini.render('But dont collide with the obstacles!', True, (255, 255, 255)) #Render the text with white color and antialiasing enabled (True)

                    screen.blit(inst_easy_text, (135, 87)) #Display the text on the screen at (6, 787)
                    screen.blit(inst_easy_text_2, (135, 100)) #Display the text on the screen at (6, 797)
                    screen.blit(inst_easy_text_3, (135, 113)) #Display the text on the screen at (6, 797)
                    screen.blit(inst_easy_text_4, (135, 126)) #Display the text on the screen at (6, 797)
                    
                    inst_easy_text_5 = font2_mini.render('You anyway play the game', True, (255, 255, 255)) #Render the text with white color and antialiasing enabled (True)
                    inst_easy_text_6 = font2_mini.render('Use the arrow keys to move the snake', True, (255, 255, 255)) #Render the text with white color and antialiasing enabled (True)
                    inst_easy_text_7 = font2_mini.render('Eat the apples to increase your score,', True, (255, 255, 255)) #Render the text with white color and antialiasing enabled (True)
                    inst_easy_text_8 = font2_mini.render('But instead your speed is fast! Forever!', True, (255, 255, 255)) #Render the text with white color and antialiasing enabled (True)

                    screen.blit(inst_easy_text_5, (135, 205)) #Display the text on the screen at (6, 787)
                    screen.blit(inst_easy_text_6, (135, 218)) #Display the text on the screen at (6, 797)
                    screen.blit(inst_easy_text_7, (135, 231)) #Display the text on the screen at (6, 797)
                    screen.blit(inst_easy_text_8, (135, 244)) #Display the text on the screen at (6, 797)

        elif menu == 'credits':
                    
                    
                    for event in pygame.event.get(): #Iterate over the events in the event queue of pygame
                        if event.type == pygame.QUIT: #If the user closes the window using the close button
                            cfgfile.close() #Close the config.ini file
                            cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                            cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                            pygame.quit() #Quit the pygame
                            cfgfile.close() #Close the config.ini file
                            delete_lock_file() #Delete the lock file
                            exit() #Exit the program

                    
                    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 400, 800)) #Fill the screen with black color (RGB: 0, 0, 0) at (0, 0) position with width 400 and height 800
                    screen.blit(credits_bg,(0,0))
                    
                   


                    screen.blit(quit_button, quit_button_rect) #Display the quit button on the screen at the center of the screen
                    if button_hover(quit_button_rect): #If the mouse is hovering over the quit button
                        quit_button.set_alpha(200) #Fade the quit button to 200 alpha
                        if button_click(quit_button_rect): #If the quit button is clicked
                            #play_sfx('click.mp3')
                            cfgfile.close() #Close the config.ini file
                            cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                            cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                            pygame.quit() #Quit the pygame
                            cfgfile.close() #Close the config.ini file
                            delete_lock_file() #Delete the lock file
                            time.sleep(1) #Wait for 1 second
                            exit() #Exit the program
                    else:
                        quit_button.set_alpha(255) #Make the button opaque (alpha 255)

                    

        elif menu == 'over':       
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        cfgfile.close()
                        cfgfile = open('config.ini','w')
                        cfgfile.write(str(highscore))
                        pygame.quit()
                        cfgfile.close()
                        delete_lock_file()
                        exit()

                pygame.draw.rect(screen, (0, 0, 0), (0, 0, 400, 800))

                screen.blit(restart_button, restart_button_rect)
                if button_hover(restart_button_rect): #If the mouse is hovering over the play button 
                        restart_button.set_alpha(200) #Fade the play button to 200 alpha
                        if button_click(restart_button_rect): #If the play button is clicked
                            #play_sfx('click.mp3')
                            pysnek_init()
                            play_sound('music.mp3', -1)
                            menu = 'game' #Change the menu to game
                        else:
                            restart_button.set_alpha(255)
                            
                screen.blit(back_button, back_button_rect)
                if button_hover(back_button_rect): #If the mouse is hovering over the play button 
                        back_button.set_alpha(200) #Fade the play button to 200 alpha
                        if button_click(back_button_rect): #If the play button is clicked
                            #play_sfx('click.mp3')
                            pysnek_init()
                            play_sound('music.mp3', -1)
                            menu = 'main' #Change the menu to game
                        else:
                            back_button.set_alpha(255)
                
                screen.blit(quit_button, quit_button_rect) #Display the quit button on the screen at the center of the screen
                if button_hover(quit_button_rect): #If the mouse is hovering over the quit button
                    quit_button.set_alpha(200) #Fade the quit button to 200 alpha
                    if button_click(quit_button_rect): #If the quit button is clicked
                        #play_sfx('click.mp3')
                        cfgfile.close() #Close the config.ini file
                        cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                        cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                        pygame.quit() #Quit the pygame
                        cfgfile.close() #Close the config.ini file
                        delete_lock_file() #Delete the lock file
                        time.sleep(1) #Wait for 1 second
                        exit() #Exit the program
                    else:
                        quit_button.set_alpha(255) #Make the button opaque (alpha 255)
                
                over_txt = font3.render('Game over!', True, (255, 255, 255))
                screen.blit(over_txt, (80, 140))
                highscore_over = font2.render(f'Best score: {highscore}', True, (255, 255, 255))
                screen.blit(highscore_over, (127, 216))
                score_over = font2.render(f'Score: {score}', True, (255, 255, 255))
                screen.blit(score_over, (154, 236))
                screen.blit(sad_pysnek, (160, 70))
                
                

        elif menu == 'key_quit':
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        cfgfile.close()
                        cfgfile = open('config.ini','w')
                        cfgfile.write(str(highscore))
                        pygame.quit()
                        cfgfile.close()
                        delete_lock_file()
                        exit()

                pygame.draw.rect(screen, (0, 0, 0), (0, 0, 400, 800))
                key_invoked_txt = font.render('You invoked Ctrl+C', True, (255, 255, 255))
                screen.blit(key_invoked_txt, (50, 140))
                quit_msg = font2.render(f'Click on the red button to quit', True, (255, 255, 255))
                screen.blit(quit_msg, (40, 216))
                resume_msg = font2.render(f'Resuming in {int(timer)}', True, (255, 255, 255))
                screen.blit(resume_msg, (140, 236))
                timer -= 0.021
                if timer <= 0:
                    menu = last_menu
                
                screen.blit(quit_button, quit_button_rect) #Display the quit button on the screen at the center of the screen
                if button_hover(quit_button_rect): #If the mouse is hovering over the quit button
                    quit_button.set_alpha(200) #Fade the quit button to 200 alpha
                    if button_click(quit_button_rect): #If the quit button is clicked
                        #play_sfx('click.mp3')
                        cfgfile.close() #Close the config.ini file
                        cfgfile = open('config.ini','w') #Open the config.ini file in write mode
                        cfgfile.write(str(highscore)) #Write the highscore to the file in string format
                        pygame.quit() #Quit the pygame
                        cfgfile.close() #Close the config.ini file
                        delete_lock_file() #Delete the lock file
                        time.sleep(1) #Wait for 1 second
                        exit() #Exit the program
                    else:
                        quit_button.set_alpha(255) #Make the button opaque (alpha 255)
                

        pygame.display.update() #Update the display
        clock.tick(60) #Control the frame rate of the game

    except FileNotFoundError:
        cfgfile.close()
        cfgfile = open('config.ini','w')
        cfgfile.write(str(highscore))
        pygame.quit()
        cfgfile.close()
        delete_lock_file()
        exit()
    except KeyboardInterrupt:
        last_menu = menu
        timer = 10
        menu = 'key_quit'
    except:
        cfgfile.close()
        cfgfile = open('config.ini','w')
        cfgfile.write(str(highscore))
        pygame.quit()
        cfgfile.close()
        delete_lock_file()
        exit()
            
            
            
