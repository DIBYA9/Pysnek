from random import choice

# Assuming the riddles dictionary is imported from another module
from riddles import riddles

# New Variables for Riddle Mechanism
current_riddle = None
user_answer = ""
input_box = pygame.Rect(300, 400, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False

def get_random_riddle():
    return choice(list(riddles.values()))

def draw_text_centered(text, font, color, surface, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(WINDOW//2, y))
    surface.blit(textobj, textrect)

def game_over_riddle():
    global menu, current_riddle, user_answer, active, color
    current_riddle = get_random_riddle()
    user_answer = ""
    active = False
    color = color_inactive
    menu = 'riddle'

# Riddle menu handling part in the game loop
elif menu == 'riddle':
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cfgfile.close()
            cfgfile = open('config.ini', 'w')
            cfgfile.write(str(highscore))
            pygame.quit()
            cfgfile.close()
            delete_lock_file()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if user_answer == current_riddle['answer']:
                    menu = 'game'
                else:
                    draw_text_centered("First practice school maths before trying this game,", font, (255, 0, 0), screen, 500)
                    draw_text_centered("it's not for beginners!", font, (255, 0, 0), screen, 540)
                    pygame.display.update()
                    time.sleep(10)
                    cfgfile.close()
                    cfgfile = open('config.ini', 'w')
                    cfgfile.write(str(highscore))
                    pygame.quit()
                    cfgfile.close()
                    delete_lock_file()
                    exit()
            elif event.key == pygame.K_BACKSPACE:
                user_answer = user_answer[:-1]
            else:
                user_answer += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive

    screen.fill((30, 30, 30))
    draw_text_centered(current_riddle['riddle'], font, (255, 255, 255), screen, 350)

    txt_surface = font.render(user_answer, True, color)
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)

    pygame.display.update()
    clock.tick(30)
