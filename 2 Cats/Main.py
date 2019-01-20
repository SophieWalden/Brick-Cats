#Importing all the modules
try:
    import time, random, sys, os
except ImportError:
    print("Make sure to have the time module")
    sys.exit()
try:
    import pygame
except ImportError:
    print("Make sure you have python 3 and pygame.")
    sys.exit()
from pygame import freetype


#game_font = pygame.freetype.Font("Font.ttf", 75)
#text_surface, rect = game_font.render(("Programmer: 8BitToaster"), (0, 0, 0))
#gameDisplay.blit(text_surface, (150, 300))

# Initialize the game engine
pygame.init()


DisplayWidth,DisplayHeight = 1000, 800
clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((DisplayWidth,DisplayHeight))
pygame.display.set_caption("Name")

Cats = pygame.sprite.Group()
Platforms = pygame.sprite.Group()

#The bigger slower cat
class BigCat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, Cats)
        self.x = 100
        self.y = 750
        self.x_change = 0
        self.y_change = 0
        self.gravity = 0
        self.size = [75,50]
        self.image = pygame.Surface(self.size)
        self.image.fill((100,50,50))
        self.rect = self.image.get_rect()
        self.chose = False
        self.JumpAllowed = True
    def draw(self):
        pygame.draw.rect(gameDisplay,(100,50,50),(self.x,self.y,75,50),0)
    def KeyPress(self):
        if self.chose == True:
            key = pygame.key.get_pressed()
            if key[ord('w')] and self.JumpAllowed == True:
                self.gravity = -8
                self.JumpAllowed = False
            if key[ord('d')]:
                self.x_change = 5
            if key[ord('a')]:
                self.x_change = -5
            if self.x_change == 5 and key[ord('d')]  == 0:
                self.x_change = 0
            if self.x_change == -5 and key[ord('a')]  == 0:
                self.x_change = 0
        self.x += self.x_change
    def Gravity(self):
        self.y += self.gravity
        if self.gravity == 0:
            self.gravity = 1
        else:
            self.gravity += .35
            
        if self.y >= DisplayHeight - 50:
            self.gravity = 0
            self.y = DisplayHeight - 50
            self.JumpAllowed = True
    def Collision(self, Small):
        for platform in Platforms:
            if pygame.sprite.collide_rect(self, platform) == True:
                if self.y < platform.y and self.gravity > 0:
                    self.gravity = 0
                    self.y = platform.y - 50
                    self.JumpAllowed = True
                if self.x_change > 0 and self.y > platform.y and self.y < platform.y + platform.height - 5:
                    self.x = platform.x - 75
                    self.x_change = 0
                elif self.x_change < 0 and self.y > platform.y and self.y < platform.y + platform.height - 5:
                    self.x = platform.x + 75
                    self.x_change = 0
                if self.y > platform.y and self.gravity < 0:
                    self.gravity = 0
                
    def update(self, Small):
        self.Collision(Small)
        self.KeyPress()
        self.draw()
        self.Gravity()
        self.rect.left = self.x
        self.rect.right = self.x+75
        self.rect.top = self.y
        self.rect.bottom = self.y + 50




#The Smaller more agile cat
class SmallCat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, Cats)
        self.x = 125
        self.y = 750
        self.x_change = 0
        self.y_change = 0
        self.gravity = 0
        self.size = [37,25]
        self.image = pygame.Surface(self.size)
        self.image.fill((100,50,50))
        self.rect = self.image.get_rect()
        self.chose = True
        self.JumpAllowed = True
    def draw(self):
        pygame.draw.rect(gameDisplay,(150,50,50),(self.x,self.y,37,25),0)
    def KeyPress(self):
        if self.chose == True:
            key = pygame.key.get_pressed()
            if key[ord('w')] and self.JumpAllowed == True:
                self.gravity = -10
                self.JumpAllowed = False
            if key[ord('d')]:
                self.x_change = 8
            if key[ord('a')]:
                self.x_change = -8
            if self.x_change == 8 and key[ord('d')]  == 0:
                self.x_change = 0
            if self.x_change == -8 and key[ord('a')]  == 0:
                self.x_change = 0
        self.x += self.x_change
    def Gravity(self):
        self.y += self.gravity
        if self.gravity == 0:
            self.gravity = 1
        else:
            self.gravity += .35
            
        if self.y >= DisplayHeight - 25:
            self.gravity = 0
            self.y = DisplayHeight - 25
            self.JumpAllowed = True

    def Collision(self, Big):
        if pygame.sprite.collide_rect(self, Big) == True:
            if self.y < Big.y - (Big.size[1] - self.size[1]) + 10 and self.gravity > 0:
                self.JumpAllowed = True
                self.gravity = 0
                self.y = Big.y - 25
        for platform in Platforms:
            if pygame.sprite.collide_rect(self, platform) == True:
                if self.y < platform.y and self.gravity > 0:
                    self.JumpAllowed = True
                    self.gravity = 0
                    self.y = platform.y - 25
                if self.x_change > 0 and self.y > platform.y and self.y < platform.y + platform.height - 5:
                    self.x = platform.x - 37
                    self.x_change = 0
                elif self.x_change < 0 and self.y > platform.y and self.y < platform.y + platform.height - 5:
                    self.x = platform.x + 37
                    self.x_change = 0
                if self.y > platform.y and self.gravity < 0:
                    self.gravity = 0
        
    def update(self, Big):
        self.Collision(Big)
        self.KeyPress()
        self.draw()
        self.Gravity()
        self.rect.left = self.x
        self.rect.right = self.x+37
        self.rect.top = self.y
        self.rect.bottom = self.y + 25
        
        
class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self, Platforms)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill((100,50,50))
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.right = self.x + self.width
        self.rect.top = self.y
        self.rect.bottom = self.y + height

    def draw(self):
        pygame.draw.rect(gameDisplay,(0,150,100),(self.x,self.y,self.width,self.height),0)
        pygame.draw.rect(gameDisplay,(0,150,0),(self.x,self.y,self.width,self.height/5),0)

def Levels(Level):
    if Level == 1:
        Platforms = [Platform(500,700,200,50),
                     Platform(200,600,200,50),
                     Platform(300,400,200,50),
                     Platform(600,300,400,100)]
    if Level == 2:
        Platforms = [Platform(400,620,100,150),
                     Platform(650,600,200,50),
                     Platform(900,700,75,25),
                     Platform(500,500,200,50),
                     Platform(50,710,200,25),
                     Platform(0,400,150,50)]
    return Platforms

def LevelCheck(Level, Small, Big, PlatformList):
    if Level == 1:
        if Small.y < 300 and Small.x > 600:
            PlatformList.append(Platform(100,500,100,50))
        if Small.y < 300 and Big.y < 300 and Small.x > 800 and Big.x > 800:
            Level += 1
            PlatformList = Levels(Level)
            Small.x = 125
            Big.x = 100
            Big.y = 700
            Small.y = 750
    if Level == 2:
        if Small.y < 400 and Small.x < 150:
            PlatformList.append(Platform(250,450,100,50))
            
    return PlatformList, Level
        

def game_loop():
    game_run = True
    Small = SmallCat()
    Big = BigCat()
    Cats.add(Small)
    Cats.add(Big)
    PlatformList = Levels(1)
    for platform in PlatformList:
        Platforms.add(platform)
    Level = 1

    while game_run == True:

        gameDisplay.fill((200,200,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if Big.chose == True:
                        Big.chose = False
                        Small.chose = True
                        Big.x_change = 0
                    else:
                        Small.chose = False
                        Big.chose = True
                        Small.x_change = 0


        Big.update(Small)
        Small.update(Big)

        for platform in PlatformList:
            platform.draw()

        PlatformList, Level = LevelCheck(Level, Small, Big, PlatformList)
    

        pygame.display.flip()
        clock.tick(60)



game_loop()
