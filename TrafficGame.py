import pygame 
import sys 

SURFACE_COLOR = (167, 255, 100)
COLOR = (255, 100, 98)
WIDTH, HEIGHT = 800, 600 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)  

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)
        self.rect = pygame.draw.rect(self.image, color, pygame.Rect(0, 0, height, width))
        self.travelled = 0

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

def draw_start_menu(screen):
    font = pygame.font.SysFont('arial', 40) 
    title = font.render(("Zombie Crossy Road"), True, (255, 255, 255)) 
    start_button = font.render('Start', True, (255, 255, 255)) 
    screen.fill((0, 0, 0))
    screen.blit(title, (WIDTH / 2 - title.get_width() / 2, 0))
    screen.blit(start_button, (WIDTH / 2 - start_button.get_width() / 2, HEIGHT / 2 - start_button.get_height() / 2))
    # print(f"Start Button Width: {start_button.get_width()} and Height: {start_button.get_height()}")
    pygame.display.flip()

def draw_post_game(screen):
    smallfont = pygame.font.SysFont('arial', 35)
    quit_text = smallfont.render('Quit Game', True, BLACK) 
    play_again_text = smallfont.render('Play Again', True, BLACK)  
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)
    mouse = pygame.mouse.get_pos()

    screen.fill(SURFACE_COLOR)
    # If mouse is hovering change the color of the button
    # QUIT: 
    if (WIDTH/2 - 75) <= mouse[0] <= (WIDTH/2 + 75) and (HEIGHT/2 - 20) <= mouse[1] <= (HEIGHT/2 + 40):
        pygame.draw.rect(screen, color_light, [(WIDTH / 2) - 75, (HEIGHT / 2) - 20, 140, 40])
    else:
        pygame.draw.rect(screen, color_dark, [(WIDTH / 2) - 75, (HEIGHT / 2) - 20, 140, 40])
    
    # PLAY AGAIN: 
    if (WIDTH/2 - 75) <= mouse[0] <=  (WIDTH/2 + 75) and (HEIGHT/2 - 80) <= mouse[1] <= (HEIGHT/2 - 80 + 40):
        pygame.draw.rect(screen, color_light, [(WIDTH / 2) - 75, (HEIGHT / 2) - 80, 140, 40])
    else:
        pygame.draw.rect(screen, color_dark, [(WIDTH / 2) - 75, (HEIGHT / 2) - 80, 140, 40])
    
    screen.blit(play_again_text, (WIDTH / 2 - 75, HEIGHT / 2 - 80))
    screen.blit(quit_text, (WIDTH / 2 - 75, HEIGHT / 2 - 20))
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
    pygame.init() # Initialize pygame 
    # Draw the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
    screen.fill(SURFACE_COLOR)
    pygame.display.set_caption("Traffic Game") 
    # Create Sprites and add them to the list of sprites 
    all_sprites_list = pygame.sprite.Group()
    player = Sprite(RED, 10, 10) 
    #player.rect.x = WIDTH / 2
    #player.rect.y = 0 
    all_sprites_list.add(player)
    for i in range(1, 4):
        car = Sprite(BLUE, 20, 20) 
        #car.rect.x = 0
        #car.rect.y = 150 * i
        all_sprites_list.add(car)

    # GAME LOOP 
    running = True 
    clock = pygame.time.Clock() 
    all_sprites_array = list(all_sprites_list)  
    set_start_pos(all_sprites_array)
    collide_list = [] 
    game_state = "start_menu"  
    while running: 
        # MAIN GAME BRANCH  
        if game_state == "game":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_x:
                        running = False
            player.handle_keys(5)
            for i in range(1, 4): # iterate thru the cars to move them 
                all_sprites_array[i].move_car(5 + (i*5)) 
            if player.is_colliding(collide_list):
                print("Collision!") 
                set_start_pos(all_sprites_array)
                game_state = "post_game"
            # UPDATE AND DRAW SPRITES ONTO SCREEN 
            for i in range(1, 4): 
                collide_list.append(all_sprites_array[i].rect)
            all_sprites_list.update() 
            screen.fill(SURFACE_COLOR) 
            all_sprites_list.draw(screen) 
            clock.tick(60)  
            pygame.display.flip() 

        # START MENU BRANCH 
        elif game_state == "start_menu": 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos() 
                # screen.blit(start_button, (WIDTH / 2 - start_button.get_width() / 2, HEIGHT / 2 - start_button.get_height() / 2))
                # if button is clicked on the "Start" button: 
                    if WIDTH/2 - 69 / 2 <= mouse[0] <= WIDTH/2 + 69 / 2 and HEIGHT/2 - 46 / 2<= mouse[1] <= HEIGHT/2 + 46 / 2:
                        game_state = "game" 
                elif event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_x:
                        running = False
            draw_start_menu(screen)
        # POST GAME BRANCH
        elif game_state == "post_game":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos() 
                    if WIDTH/2 - 75 <= mouse[0] <= WIDTH/2 + 75 and HEIGHT/2 - 20 <= mouse[1] <= HEIGHT/2 + 20: # if "Quit" is clicked
                        running = False
                    elif (WIDTH/2 - 75) <= mouse[0] <=  (WIDTH/2 + 75) and (HEIGHT/2 - 80) <= mouse[1] <= (HEIGHT/2 - 80 + 40):
                        game_state = "game"
                elif event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_x:
                        running = False
            draw_post_game(screen)

pygame.display.quit()