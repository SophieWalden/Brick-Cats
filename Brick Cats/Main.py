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
pygame.display.set_caption("Brick Cats")

Cats = pygame.sprite.Group()
Platforms = pygame.sprite.Group()

def load_images(path_to_directory):
    images = {}
    for dirpath, dirnames, filenames in os.walk(path_to_directory):
        for name in filenames:
            if name.endswith('.png'):
                key = name[:-4]
                if key != "HouseBackground":
                    img = pygame.image.load(os.path.join(dirpath, name)).convert_alpha()
                else:
                    img = pygame.image.load(os.path.join(dirpath, name)).convert()
                images[key] = img
    return images

#The bigger slower cat
class BigCat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, Cats)
        self.x = 900
        self.y = 275
        self.x_change = 0
        self.gravity = 0
        self.size = [75,50]
        self.image = pygame.Surface(self.size)
        self.image.fill((100,50,50))
        self.rect = self.image.get_rect()
        self.chose = False
        self.JumpAllowed = True
        self.direction = "Right"
    def draw(self,Images):
        if self.x_change == 0:
            if self.direction == "Right":
                gameDisplay.blit(Images["BigCatSittingRight"],(self.x,self.y+4))
            else:
                gameDisplay.blit(Images["BigCatSittingLeft"],(self.x,self.y+4))
        else:
            if self.x_change > 0:
                gameDisplay.blit(Images["BigCatRight"],(self.x,self.y))
            else:
                gameDisplay.blit(Images["BigCatLeft"],(self.x,self.y))
    def KeyPress(self):
        if self.chose == True:
            key = pygame.key.get_pressed()
            if key[ord('w')] and self.JumpAllowed == True and self.gravity >= 0:
                self.gravity = -8
                self.JumpAllowed = False
            if key[ord('d')]:
                self.x_change = 5
                self.direction = "Right"
            if key[ord('a')]:
                self.x_change = -5
                self.direction = "Left"
            if self.x_change == 5 and key[ord('d')]  == 0:
                self.x_change = 0
            if self.x_change == -5 and key[ord('a')]  == 0:
                self.x_change = 0
        if self.x_change == 5 and self.x < DisplayWidth - 75:
            self.x += self.x_change
        if self.x_change == -5 and self.x - 5 > -5:
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
                if self.x_change > 0 and self.y > platform.y and self.y < platform.y + platform.height - 10:
                    self.x = platform.x - 75
                    self.x_change = 0
                elif self.x_change < 0 and self.y > platform.y and self.y < platform.y + platform.height - 10:
                    self.x = platform.x + platform.width
                    self.x_change = 0
                if self.y > platform.y and self.gravity < 0:
                    self.gravity = 0

    def reset(self,x,y):
        self.x = x
        self.y = y
        self.gravity = 0
                
    def update(self, Small,Images):
        self.Collision(Small)
        self.KeyPress()
        self.draw(Images)
        self.Gravity()
        self.rect.left = self.x
        self.rect.right = self.x+75
        self.rect.top = self.y
        self.rect.bottom = self.y + 50




#The Smaller more agile cat
class SmallCat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, Cats)
        self.x = 700
        self.y = 750
        self.x_change = 0
        self.gravity = 0
        self.size = [37,25]
        self.image = pygame.Surface(self.size)
        self.image.fill((100,50,50))
        self.rect = self.image.get_rect()
        self.chose = True
        self.JumpAllowed = True
        self.direction = "Right"
    def draw(self, Images):
        if self.x_change == 0:
            if self.direction == "Right":
                gameDisplay.blit(Images["SmallCatSittingRight"],(self.x,self.y+5))
            else:
                gameDisplay.blit(Images["SmallCatSittingLeft"],(self.x,self.y+5))

        else:
            if self.x_change > 0:
                gameDisplay.blit(Images["SmallCatRight"],(self.x,self.y))
            else:
                gameDisplay.blit(Images["SmallCatLeft"],(self.x,self.y))


    def KeyPress(self):
        if self.chose == True:
            key = pygame.key.get_pressed()
            if key[ord('w')] and self.JumpAllowed == True and self.gravity >= 0:
                self.gravity = -10
                self.JumpAllowed = False
            if key[ord('d')]:
                self.x_change = 8
                self.direction = "Right"
            if key[ord('a')]:
                self.x_change = -8
                self.direction = "Left"
            if self.x_change == 8 and key[ord('d')]  == 0:
                self.x_change = 0
            if self.x_change == -8 and key[ord('a')]  == 0:
                self.x_change = 0
        if self.x_change == 8 and self.x < DisplayWidth - 37:
            self.x += self.x_change
        if self.x_change == -8 and self.x - 8 > -8:
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
        if Big != 0:
            if Big.x < self.x and Big.x + 75 > self.x and Big.y - 15 < self.y  and Big.y > self.y and self.gravity > 0:
                self.y = Big.y - 30

            if pygame.sprite.collide_rect(self, Big) == True:
                if self.y < Big.y - (Big.size[1] - self.size[1]) + 10 and self.gravity > 0:
                    if Big.gravity < 0:
                        self.gravity = Big.gravity
                    self.JumpAllowed = True
                    self.gravity = 0
                    if Big.x_change != 0:
                        self.y = Big.y - 23
                    else:
                        self.y = Big.y - 17
        
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
                    self.x = platform.x + platform.width
                    self.x_change = 0
                if self.y > platform.y and self.gravity < 0:
                    self.gravity = 0

    def reset(self,x,y):
        self.x = x
        self.y = y
        self.gravity = 0
        self.x_change = 0
        self.JumpAllowed = True
        
    def update(self, Big, Images):
        self.Collision(Big)
        self.KeyPress()
        self.draw(Images)
        self.Gravity()
        self.rect.left = self.x
        self.rect.right = self.x+37
        self.rect.top = self.y
        self.rect.bottom = self.y + 25
        
        
class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height, Item):
        pygame.sprite.Sprite.__init__(self, Platforms)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.right = self.x + self.width
        self.rect.top = self.y
        self.rect.bottom = self.y + height
        self.Item = Item

    def draw(self, Images):
        gameDisplay.blit(pygame.transform.scale(Images[self.Item],(self.width,self.height)),(self.x,self.y))
            

def Levels(Level):
    #Drawing all the sprites on the level
    if Level == 1:
        Platforms = [Platform(0,700,500,100, "Bed"),
                     Platform(450,550,400,50,"Shelf"),
                     Platform(200,400,150,150,"Window"),
                     Platform(0,300,200,50,"Shelf"),
                     Platform(650,450,200,100,"Books"),
                     Platform(600,100,300,225,"MovingTutorial")]
    if Level == 2:
        Platforms = [Platform(700,300,300,50,"Shelf"),
                     Platform(100,400,200,400,"Door"),
                     Platform(700,400,200,400,"Door"),
                     Platform(450,700,100,100,"TableBottom"),
                     Platform(350,650,300,50,"TableTop"),
                     Platform(450,500,100,150,"Picture"),
                     Platform(0,300,200,50,"Shelf")]
    if Level == 3:
        Platforms = [Platform(700,300,300,50,"Shelf"),
                     Platform(500,700,500,100, "Bed"),
                     Platform(200,500,200,300,"Bookshelf"),
                     Platform(400,600,100,200,"SideTable"),
                     Platform(0,300,150,50,"Shelf"),
                     Platform(400,50,150,112,"SwitchingTutorial"),
                     Platform(0,200,100,100,"OpenWindow")]
    if Level == 4:
        pass
    return Platforms

def LevelCheck(Level, Small, Big, PlatformList):
    if Level == 1:
        if Small.x < 50 and Small.y < 300:
            Level += 1
            Small.reset(900,275)
            PlatformList = Levels(Level)
            for item in Platforms:
                Platforms.remove(item)
            for platform in PlatformList:
                Platforms.add(platform)
    if Level == 2:
        if Small.x < 50 and Small.y < 300:
            Level += 1
            Small.reset(900,275)
            PlatformList = Levels(Level)
            for item in Platforms:
                Platforms.remove(item)
            for platform in PlatformList:
                Platforms.add(platform)
    if Level == 3:
        if Small.x < 110 and Small.y < 300:
            Small.reset(900,275)
            Big.reset(900,275)
            PlatformList = Levels(Level)
            for item in Platforms:
                Platforms.remove(item)
            for platform in PlatformList:
                Platforms.add(platform)
            
            
    return PlatformList, Level
        

def game_loop():
    game_run = True
    Images = load_images("Images")
    Small = SmallCat()
    Cats.add(Small)
    PlatformList = Levels(1)
    for platform in PlatformList:
        Platforms.add(platform)
    Level = 1

    while game_run == True:

        #Displaying Backgrounds
        if Level <= 3:
            gameDisplay.blit(Images["HouseBackground"],(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #Switching Cats
                if event.key == pygame.K_q and Level >= 3:
                    if Big.chose == True:
                        Big.chose = False
                        Small.chose = True
                        Big.x_change = 0
                    else:
                        Small.chose = False
                        Big.chose = True
                        Small.x_change = 0
                #Restarting a level
                if event.key == pygame.K_r:
                    if Level == 1:
                        Small.reset(700,750)
                    if Level == 2:
                        Small.reset(900,275)
                    if Level == 3 or Level == 4:
                        Small.reset(900,275)
                        Big.reset(900,275)

        #Adding the Big cat after level 3
        if len(Cats) == 1 and Level >= 3:
           Big = BigCat()
           Cats.add(Big)

        #Updating everything
        if Level >= 3:
            Big.update(Small, Images)
            Small.update(Big, Images)
            PlatformList, Level = LevelCheck(Level, Small, Big, PlatformList)
        else:
            Small.update(0, Images)
            PlatformList, Level = LevelCheck(Level, Small, 0, PlatformList)
            
        #Drawing all the platforms
        for platform in PlatformList:
            platform.draw(Images)

        pygame.display.flip()
        clock.tick(120)



game_loop()
