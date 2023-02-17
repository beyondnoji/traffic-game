import pygame 
import sys 
pygame.init() 
SURFACE_COLOR = (0, 200, 150)
# (167, 255, 100)
COLOR = (255, 100, 98)
WIDTH, HEIGHT = 800, 600 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)  

buttons = pygame.sprite.Group() 
finish_line_img = pygame.image.load("finishLine.jpg")

class Button(pygame.sprite.Sprite):
    def __init__(self, screen, position, text, text_color, size, bg_default, bg_hovered):
        super().__init__()
        self.text_color = text_color 
        self.bg_default = bg_default
        self.bg_hovered = bg_hovered
        self.font = pygame.font.SysFont("Arial", size)
        self.text_render = self.font.render(text, True, self.text_color)
        self.image = self.text_render 
        self.x, self.y, self.w, self.h = self.text_render.get_rect() 
        self.x, self.y = position 
        buttons.add(self) 
    
    def update(self, mouse):
        if self.is_hovered(mouse):
            pygame.draw.rect(screen, self.bg_hovered, [self.x, self.y, self.w, self.h])
        else:
            pygame.draw.rect(screen, self.bg_default, [self.x, self.y, self.w, self.h])
        screen.blit(self.text_render, (self.x, self.y))
    
    def is_hovered(self, mouse): 
        return (self.x) <= mouse[0] <=  (self.x + self.w) and (self.y) <= mouse[1] <= (self.y + self.h)
        
class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width, image = None):
        super().__init__()
        if not image == None:
            self.image = finish_line_img
            self.rect = pygame.draw.rect(self.image, color, pygame.Rect(0, 0, height, width))
        else:
            self.image = pygame.Surface([width, height])
            self.image.set_colorkey(COLOR)
            self.rect = pygame.draw.rect(self.image, color, pygame.Rect(0, 0, height, width))
            self.travelled = 0

    def draw(self): 
        screen.blit(self.rect)
        
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
    
    def move_car(self, speed):
        dist = 1
        if self.travelled % 2 == 0: # DEFUALT TO 0 
            self.rect.x += dist * speed 
        else:
            self.rect.x -= dist * speed
        if self.keep_in_screen(WIDTH, HEIGHT): 
            self.travelled += 1

    def is_colliding(self, collide_list):
        if self.rect.collidelist(collide_list) == -1:
            return False
        else:
            return True

def update_game_screen(): 
    for i in range(1, 4): 
        collide_list.append(all_sprites_array[i].rect)
    all_sprites_list.update() 
    screen.fill(SURFACE_COLOR) 
    all_sprites_list.draw(screen) 
    screen.blit(finish_line.image, (finish_line.rect.x, finish_line.rect.y)) 
    clock.tick(60)  
    pygame.display.flip() 

def move_all_cars():
    for i in range(1, 4): # iterate thru the cars to move them 
        all_sprites_array[i].move_car(5 + (i*7)) 

def draw_start_menu(screen):
    mouse = pygame.mouse.get_pos()
    screen.fill((SURFACE_COLOR))
    screen.blit(title, (WIDTH / 2 - title.get_width() / 2, 0)) 
    start_button.update(mouse)
    pygame.display.flip()

def draw_post_game(screen):
    mouse = pygame.mouse.get_pos()
    screen.fill(SURFACE_COLOR) 
    quit_button.update(mouse) 
    play_again_button.update(mouse)
    pygame.display.flip() 

def set_start_pos( all_sprites_array):
    for i in range(len(all_sprites_array)): 
        if i == 0:
            all_sprites_array[i].rect.x = WIDTH / 2
            all_sprites_array[i].rect.y = 0
        else:
            all_sprites_array[i].rect.x = 0
            all_sprites_array[i].rect.y = 150 * i
        

if __name__ == "__main__": 
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
    pygame.display.set_caption("Traffic Game") 

    ''' CODE FOR GUI OBJECTS: '''
    quit_text = "Quit Game"
    play_again_text = "Play Again"
    quit_button_x, quit_button_y = WIDTH / 2 - 75, HEIGHT/2 - 20 
    play_again_button_x, play_again_button_y, = WIDTH / 2 - 75, HEIGHT /  2 - 80
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)
    quit_button = Button(screen, [quit_button_x, quit_button_y], quit_text, BLACK, 35, color_dark, color_light)
    play_again_button = Button(screen, [play_again_button_x, play_again_button_y], play_again_text, BLACK, 35, color_dark, color_light) 

    font = pygame.font.SysFont('arial', 40) 
    title = font.render(("Zombie Crossy Road"), True, BLACK) 
    start_button_x, start_button_y = WIDTH / 2, HEIGHT / 2
    start_button = Button(screen, [start_button_x, start_button_y], "Start", BLACK, 35, WHITE , GREEN) 

    ''' CODE FOR ALL SPRITE OBJECTS '''
    all_sprites_list = pygame.sprite.Group()
    player = Sprite(RED, 10, 10) 
    all_sprites_list.add(player)
    for i in range(1, 4):
        car = Sprite(BLUE, 25, 25) 
        all_sprites_list.add(car)
    buttons_list = list(buttons)

    finish_line = Sprite(WHITE, 100, 800, image = finish_line_img)
    all_sprites_list.add(finish_line)

    '''
    MAIN GAME LOOP BEGINS : 
    '''
    running = True 
    clock = pygame.time.Clock() 
    all_sprites_array = list(all_sprites_list)  
    set_start_pos(all_sprites_array)
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
                set_start_pos(all_sprites_array)
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
            draw_start_menu(screen)

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
            draw_post_game(screen)

pygame.display.quit()