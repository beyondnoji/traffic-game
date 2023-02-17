import pygame
pygame.init() 

SURFACE_COLOR = (50, 50, 50)
# (167, 255, 100)
COLOR = (255, 100, 98)
WIDTH, HEIGHT = 800, 600 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (100, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 100)  
YELLOW = (255, 255, 0)
LIGHT_PURPLE = (60, 0, 90)
LEVEL = 1

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Game") 
buttons = pygame.sprite.Group() 
all_sprites_list = pygame.sprite.Group()
car_img = pygame.image.load('car.png') 
player_img = pygame.image.load('player2.png') 
finish_line_img = pygame.image.load('finish_line.png')


class Button(pygame.sprite.Sprite):
    def __init__(self, position, text, text_color, size, bg_unhovered, bg_hovered):
        super().__init__()
        self.text_color = text_color 
        self.bg_unhovered = bg_unhovered
        self.bg_hovered = bg_hovered
        self.font = pygame.font.SysFont("Arial", size)
        self.text_render = self.font.render(text, True, self.text_color)
        self.image = self.text_render 
        self.x, self.y, self.w, self.h = self.text_render.get_rect() 
        self.position = position
        self.x, self.y = position
        buttons.add(self) 
    
    def update(self, mouse):
        self.x, self.y, self.w, self.h = self.text_render.get_rect() 
        self.x, self.y = self.position
        if self.is_hovered(mouse):
            pygame.draw.rect(window, self.bg_hovered, [self.x - self.text_render.get_width() / 2, self.y - self.text_render.get_height() / 2 , self.w, self.h])
        else:
            pygame.draw.rect(window, self.bg_unhovered, [self.x - self.text_render.get_width() / 2, self.y - self.text_render.get_height() / 2, self.w, self.h])
        window.blit(self.text_render, (self.x - self.text_render.get_width() / 2, self.y - self.text_render.get_height() / 2))
    
    def is_hovered(self, mouse): 
        return (self.x - self.text_render.get_width() / 2) <= mouse[0] <=  (self.x + self.w / 2) and (self.y - self.text_render.get_height() / 2) <= mouse[1] <= (self.y + self.h / 2)
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
            super().__init__()  
            self.image = player_img.convert_alpha()
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            all_sprites_list.add(self)

    def handle_keys(self, speed):
        key = pygame.key.get_pressed() 
        dist = 1 * speed # distan
        if key[pygame.K_DOWN]: 
            self.rect.y += dist 
        elif key[pygame.K_UP]: 
            self.rect.y -= dist 
        elif key[pygame.K_RIGHT]:
            self.rect.x += dist 
        elif key[pygame.K_LEFT]:
            self.rect.x -= dist 
        self.keep_in_screen(WIDTH, HEIGHT)

    def keep_in_screen(self, width, height):
        # If you hit the right side, of screen
        if self.rect.right > width: 
            self.rect.right = width
            return True
        elif self.rect.left < 0:
            self.rect.left = 0
            return True 
        elif self.rect.top < 0:
            self.rect.top = 0
            return True
        elif self.rect.bottom > height:
            self.rect.bottom = height
            return True
        else:
            return False

    def is_colliding(self, collide_list):
        if self.rect.collidelist(collide_list) == -1:
            return False
        else:
            return True
    
    def just_won(self):
        return self.rect.bottom >= 500 

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = car_img.convert_alpha() 
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.travelled = 0
        all_sprites_list.add(self)

    def move_car(self, speed):
        dist = 1
        if self.travelled % 2 == 0: # DEFUALT TO 0 
            self.rect.x += dist * speed 
        else:
            self.rect.x -= dist * speed
        if self.keep_in_screen(WIDTH, HEIGHT): 
            self.travelled += 1
    
    def keep_in_screen(self, width, height):
        # If you hit the right side, of screen
        if self.rect.right > width: 
            self.rect.right = width
            return True
        elif self.rect.left < 0:
            self.rect.left = 0
            return True 
        elif self.rect.top < 0:
            self.rect.top = 0
            return True
        elif self.rect.bottom > height:
            self.rect.bottom = height
            return True
        else:
            return False

class FinishLine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = finish_line_img.convert_alpha() 
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = HEIGHT - 200
        self.rect.width = WIDTH
        self.rect.height = HEIGHT - 100 
        print(self.rect)
        all_sprites_list.add(self)

def set_start_pos():
    for i in range(len(sprites_array)): 
        if i == 0:
            sprites_array[i].rect.x = WIDTH / 2
            sprites_array[i].rect.y = 0
        else:
            sprites_array[i].rect.x = 0
            sprites_array[i].rect.y = 150 * i

def update_game_screen(): 
    for i in range(1, 5): 
        collide_list.append(sprites_array[i].rect)
    all_sprites_list.update() 
    window.fill(SURFACE_COLOR) 
    window.blit(level_render, (0, 0)) 
    window.blit(finish_line.image, (0, 500))
    all_sprites_list.draw(window) 
    clock.tick(60)  
    pygame.display.flip() 

def draw_start_menu():
    mouse = pygame.mouse.get_pos()
    window.fill((SURFACE_COLOR))
    window.blit(title, (WIDTH / 2 - title.get_width() / 2, 0)) 
    start_button.update(mouse)
    pygame.display.flip()

def draw_post_game(winning):
    if winning:
        win_or_lose_message = title_font.render("WINNER!", True, GREEN) 
        play_again_button.text_render = play_again_button.font.render(f"Play Level {LEVEL}", True, GREEN)

    else:
        play_again_button.text_render = play_again_button.font.render("Play Again", True, YELLOW)
        win_or_lose_message = title_font.render("LOSER!", True, RED) 

    mouse = pygame.mouse.get_pos()
    window.fill(SURFACE_COLOR) 
    quit_button.update(mouse) 
    play_again_button.update(mouse)
    window.blit(win_or_lose_message, (WIDTH / 2 - win_or_lose_message.get_width() / 2, 0))
    pygame.display.flip() 

def move_all_cars():
    for i in range(1, 4): # iterate thru the cars to move them 
        sprites_array[i].move_car(5 + (i*LEVEL)) 


''' DECLARE ALL VARIABLES AND OBJECTS '''
hovered_color = (170, 170, 170)
unhovered_color = (100, 100, 100)

quit_text = "Quit Game"
quit_button_x, quit_button_y = WIDTH / 2 + 100, HEIGHT/2 
quit_button = Button([quit_button_x, quit_button_y], quit_text, BLACK, 35, unhovered_color, hovered_color)

play_again_text = "Play Again"
play_again_button_x, play_again_button_y, = WIDTH / 2 - 100, HEIGHT /  2 
play_again_button = Button([play_again_button_x, play_again_button_y], play_again_text, BLACK, 35, unhovered_color, hovered_color) 

title_font = pygame.font.SysFont('Arial', 40) 
title = title_font.render(("Zombie Crossy Road"), True, RED)

level_font = pygame.font.SysFont('Arial', 25)
level_render = level_font.render((f"Level {LEVEL}"), True, RED)

start_button_x, start_button_y = WIDTH / 2, HEIGHT / 2
start_button = Button([start_button_x, start_button_y], "Start", WHITE, 35, unhovered_color, GREEN) 

player = Player() 
for i in range(1, 4):
    car = Car() 

finish_line = FinishLine()

buttons_array = list(buttons)
sprites_array = list(all_sprites_list)

if __name__ == "__main__":
    '''
    MAIN GAME LOOP BEGINS : 
    '''
    running = True 
    winning = True
    clock = pygame.time.Clock() 
    set_start_pos()
    collide_list = [] 
    GAME_STATE = "start_menu"  

    while running: 
        ''' MAIN GAME BRANCH '''
        if GAME_STATE == "game":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_x:
                        running = False
            player.handle_keys(5)
            move_all_cars()

            if player.is_colliding(collide_list):
                print("Collision!") 
                set_start_pos()
                winning = False
                LEVEL = 1
                level_render = level_font.render((f"Level {LEVEL}"), True, RED)
                GAME_STATE = "post_game"

            elif player.just_won(): 
                set_start_pos()
                winning = True
                LEVEL += 1
                level_render = level_font.render((f"Level {LEVEL}"), True, RED)
                GAME_STATE = "post_game" 
            update_game_screen()

            ''' START MENU BRANCH '''
        elif GAME_STATE == "start_menu": 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos() 
                    if start_button.is_hovered(mouse):
                        GAME_STATE = "game" 
                elif event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_x:
                        running = False
            draw_start_menu()

            ''' POST GAME BRANCH ''' 
        elif GAME_STATE == "post_game":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos() 
                    if quit_button.is_hovered(mouse):
                        running = False
                    elif play_again_button.is_hovered(mouse):
                        GAME_STATE = "game"
                elif event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_x:
                        running = False
            draw_post_game(winning)

pygame.display.quit()
    