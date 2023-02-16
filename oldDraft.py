import pygame 

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()
  
        self.image = pygame.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)
  
        pygame.draw.rect(self.image,color,pygame.Rect(0, 0, width, height))
  
        self.rect = self.image.get_rect()
        self.traveled = 0

    # Movement methods: 
    def moveRight(self, pixels):
        self.rect.x += pixels 
    def moveLeft(self, pixels):
        self.rect.x -= pixels
    def moveForward(self, speed):
        self.rect.y += speed 
    def moveBack(self, speed):
        self.rect.y -= speed

    def keepInScreen(self, width, height):
        
        # If you hit the right side, of screen
        if self.rect.right > width: 
            self.rect.right = width
            return True
        elif self.rect.left < 0:
            self.rect.left = 0
            return True 

        else:
            return False
            
    def checkCollision(self, spritesList):
        for i in spritesList:
            return self.colliderect(i)

if __name__ == "__main__":
    pygame.init() 
    SURFACE_COLOR = (167, 255, 100)
    COLOR = (255, 100, 98)
    white = (255, 255, 255)
    red = (255, 0, 0)  
    HEIGHT = 600
    WIDTH = 1000

    # Create a screen object
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # Set the caption at the top of screen
    pygame.display.set_caption('Traffic Game')

    # Declare all sprites list
    all_sprites_list = pygame.sprite.Group() 
    # Create player object 
    player = Sprite(red, 10, 10)    
    # Position on screen
    player.rect.x = WIDTH / 2 # start at the top of the screen, in the middle
    player.rect.y = 0
    all_sprites_list.add(player)

    # Create traffic objects 
    car1 = Sprite((0, 0, 255), 10, 10)
    car1.rect.x = 0 
    car1.rect.y = 150
    all_sprites_list.add(car1)
    
    car2 = Sprite((0, 0, 255), 10, 10)
    car2.rect.x = 0 
    car2.rect.y = 300
    all_sprites_list.add(car2)

    car3 = Sprite((0, 0, 255), 10, 10)
    car3.rect.x = 0 
    car3.rect.y = 450
    all_sprites_list.add(car3)

    car4 = Sprite((0, 0, 255), 10, 10)
    car4.rect.x = 0 
    car4.rect.y = 600 
    all_sprites_list.add(car4)

    # Create finish line object
    finishLine = Sprite(white, 20, WIDTH) 
    finishLineImage = pygame.image.load('finishLine.jpg').convert()

    running = True 
    clock = pygame.time.Clock()
    speedOfCar1 = 15 
    speedOfCar2 = 10
    speedOfCar3 = 5

    # GAME LOOP 
    while running:
        # Check for exit in eventss
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    running = False

        # Draw finish line 
        screen.blit(finishLineImage, (WIDTH, HEIGHT))
        # Constant movement of cars 
        if car1.traveled % 2 == 0: # DEFUALT TO 0 
            car1.moveRight(speedOfCar1)
        else:
            car1.moveLeft(speedOfCar1) 

        if car2.traveled % 2 == 0:
            car2.moveRight(speedOfCar2)
        else:
            car2.moveLeft(speedOfCar2)

        if car3.traveled % 2 == 0:
            car3.moveRight(speedOfCar2)
        else:
            car3.moveLeft(speedOfCar3)
        
        # Check if hit the end of screen
        if car1.keepInScreen(WIDTH, HEIGHT): 
            car1.traveled += 1  
        if car2.keepInScreen(WIDTH, HEIGHT):
            car2.traveled += 1
        if car3.keepInScreen(WIDTH, HEIGHT):
            car3.traveled += 1
        player.keepInScreen(WIDTH, HEIGHT) 
        
        # Check for movement events 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.moveLeft(5)
        if keys[pygame.K_RIGHT]:
            player.moveRight(5)
        if keys[pygame.K_DOWN]:
            player.moveForward(5)
        if keys[pygame.K_UP]:
            player.moveBack(5)

        all_sprites_list.update()
        screen.fill(SURFACE_COLOR) 
        all_sprites_list.draw(screen) # draw all sprites on the screen
        pygame.display.flip() # update screen
        clock.tick(60) # 60 fps

    pygame.display.quit()