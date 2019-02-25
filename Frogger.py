#Samuel
#22/1/2019
#Frogger



#Imports
import pygame
import random


#Variables
#Main game vars
gameWindow = None
WIDTH = 640
HEIGHT = 480
SCALE = 40
running = True

#Tick speed
tickSpeed = 60

#Score vars
score = 0
scoreFont = None

#Class vars
player = None
lanes = []

#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 100, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


#Classes
class Player:
    def __init__(self, x, y, w, h, moveSpd):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.moveSpd = moveSpd
        self.dir = 0

        self.logMoveSpd = 0
        
        self.lives = 3
        self.dead = False

        #Current animation frame
        self.animationFrame = 1
        #Animation timer
        self.animationTime = 0
        #Images
        self.images1 = []
        self.images2 = []
        self.images3 = []
        #File names for frame 1
        fileNames = ("Data/frogUp0.png", "Data/frogRight0.png", "Data/frogDown0.png", "Data/frogLeft0.png")
        #Load and scale images
        for i in range(4):
            self.images1.append(pygame.image.load(fileNames[i]))
            self.images1[i] = pygame.transform.scale(self.images1[i], (self.w, self.h))

        #File names for frame 2
        fileNames = ("Data/frogUp1.png", "Data/frogRight1.png", "Data/frogDown1.png", "Data/frogLeft1.png")
        #Load and scale images
        for i in range(4):
            self.images2.append(pygame.image.load(fileNames[i]))
            self.images2[i] = pygame.transform.scale(self.images2[i], (self.w, self.h))

        #File names for frame 3
        fileNames = ("Data/frogUp2.png", "Data/frogRight2.png", "Data/frogDown2.png", "Data/frogLeft2.png")
        #Load and scale images
        for i in range(4):
            self.images3.append(pygame.image.load(fileNames[i]))
            self.images3[i] = pygame.transform.scale(self.images3[i], (self.w, self.h))

    def show(self, gameWindow):
        #pygame.draw.rect(gameWindow, BLACK, (self.x, self.y, self.w, self.h))
        #print(self.dir)
        #Displays frame 1
        if(self.animationFrame == 1):
            gameWindow.blit(self.images1[self.dir], (self.x, self.y))

        #Displays frame 2
        elif(self.animationFrame == 2):
            gameWindow.blit(self.images2[self.dir], (self.x, self.y))

        #Displays frame 3
        elif(self.animationFrame == 3):
            gameWindow.blit(self.images3[self.dir], (self.x, self.y))

        #Displays lives
        for i in range(self.lives):
            gameWindow.blit(self.images1[0], (SCALE * i + 10, HEIGHT - self.h))

    def moveLeft(self):
        #Sets direction ot left
        self.dir = 3
        if(self.x > 0):
            self.x -= self.moveSpd

        self.cycleAnimation()

    def moveRight(self):
        #Sets direction to right
        self.dir = 1
        if(self.x < WIDTH - self.w):
            self.x += self.moveSpd

        self.cycleAnimation()
    
    def moveUp(self):
        #Sets direction to up
        self.dir = 0
        if(self.y > 0):
            self.y -= self.moveSpd

        self.cycleAnimation()

    def moveDown(self):
        #Sets direction to down
        self.dir = 2
        if(self.y < HEIGHT - self.h * 2):
            self.y += self.moveSpd

        self.cycleAnimation()

    def cycleAnimation(self):
        #Adds to the animation timer
        self.animationTime += 1
        if(self.animationTime % 4 == 0):
            if(self.animationFrame < 3):
                #Moves to the next animation
                self.animationFrame += 1

            else:
                #Makes it stay within the 3 animation frames
                self.animationFrame = 1

    def moveOnLog(self):
        if(self.x < WIDTH - self.w):
            self.x += self.logMoveSpd

    def takeHit(self):
        #Resets pos
        self.x = WIDTH // 2 - self.w // 2
        self.y = HEIGHT - self.h * 2 + 5
        #Plays a sound
        pygame.mixer.Sound("Data/getHitSound.wav").play()

        #Removes a live
        if(self.lives > 0):
            self.lives -= 1

        else:
            #Makes the player dead
            self.dead = True
            print("dead")

    def col(self, lanes, exitLane, gameWindow, score):
        #Stores if the player is on a log
        onVehicle = False
        
        for lane in lanes:
            for vehicle in lane.vehicles:
                #Collides the player with the vehicles
                if(pygame.Rect(self.x, self.y, self.w, self.h).colliderect((vehicle.x, vehicle.y, vehicle.w, vehicle.h))):
                    #Checks if it is a ground lane
                    if(lane.t == 'g'):
                        self.takeHit()

                    #Checks if it is a water lane
                    elif(lane.t == 'w'):
                        onVehicle = True
                        #print(onVehicle)
                        if(self.x < WIDTH - self.w):
                            self.logMoveSpd = vehicle.moveSpd

            #Collides the player with the lanes
            if(pygame.Rect(self.x, self.y, self.w, self.h).colliderect((lane.x, lane.y + 5, lane.w, lane.h - 15)) and not onVehicle):
                #Checks if it is a water lane
                if(lane.t == 'w'):
                    #print(onVehicle)
                    self.takeHit()

            for collectable in lane.collectables:
                if(not collectable.isCollected):
                    #Collides the player with the collectable
                    if(pygame.Rect(self.x, self.y, self.w, self.h).colliderect((collectable.x, collectable.y, collectable.w, collectable.h))):
                        #Checks if it is a key
                        if(collectable.t == 'k'):
                            #Plays a sound
                            pygame.mixer.Sound("Data/collectKeySound.wav").play()
                            #Sets the collectable as collected
                            collectable.isCollected = True
                            print('c')
                            exitLane.currentCollectable += 1

        #Collides the player with the exitlane
        if(pygame.Rect(self.x, self.y, self.w, self.h).colliderect((exitLane.x, exitLane.y, exitLane.w, exitLane.h))):
            #Checks if it is a exit lane and the player collected all of the keys
            if(exitLane.t == 'e' and exitLane.currentCollectable == exitLane.maxCollectable):
                #Plays a sound
                pygame.mixer.Sound("Data/beatLevelSound.wav").play()
                #Generates a new level
                generateLevel(lanes)
                #Resets players pos
                self.x = WIDTH // 2 - self.w // 2
                self.y = HEIGHT - self.h * 2 + 5
                #Adds some score
                score += 100

        #Checks if the player was on a log
        if(not onVehicle):
            self.logMoveSpd = 0

        return score

class Vehicle:
    def __init__(self, x, y, w, h, moveSpd, t, imageName):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.moveSpd = moveSpd

        #Load and scale the image
        self.image = pygame.image.load(imageName)
        self.image = pygame.transform.scale(self.image, (self.w, self.h))

        #Gives a type
        self.t = t

    def show(self, gameWindow):
        #pygame.draw.rect(gameWindow, BLACK, (self.x, self.y, self.w, self.h))
        gameWindow.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.moveSpd

    def wrap(self):
        if(self.x > WIDTH + self.w):
            self.x = -self.w

class Collectable:
    def __init__(self, x, y, w, h, t, imageName):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        #Load and scale the image
        self.image = pygame.image.load(imageName)
        self.image = pygame.transform.scale(self.image, (self.w, self.h))

        #Gives a type
        self.t = t
        self.isCollected = False

    def show(self, gameWindow):
        if(not self.isCollected):
            #pygame.draw.rect(gameWindow, YELLOW, (self.x, self.y, self.w, self.h))
            gameWindow.blit(self.image, (self.x, self.y))

class Lane:
    def __init__(self, y, h, t):
        self.x = 0
        self.y = y
        self.w = WIDTH
        self.h = h
        self.t = t

        #Stores all of the collectables
        self.collectables = []

        #Gives only the exit lane the collectable vars
        if(self.t == 'e'):
            self.currentCollectable = 0
            self.maxCollectable = 1

        #Gives the lanes a colour
        self.clr = None
        if(self.t == 'g'):
            self.clr = GRAY

        elif(self.t == 'w'):
            self.clr = BLUE

        elif(self.t == 's'):
            self.clr = YELLOW

        elif(self.t == 'e'):
            self.clr = GREEN

        #Stores all of the vehicles
        self.vehicles = []
        #Checks if it is a ground lane
        if(self.t == 'g'):
            #Generates random amount of cars
            randCarAmounts = [(1, 2)]
            randCarAmount = random.randint(randCarAmounts[0][0], randCarAmounts[0][1])
            #Gives a random speed
            vSpd = random.randint(3, 5)
            for i in range(randCarAmount):
                #Gives a random x pos
                vRandX = random.randint(0, SCALE * randCarAmounts[0][1]) * 3 + i * SCALE * randCarAmounts[0][1] * 5
                #Assigns a type
                vType = 'c'
                #Assigns a random image
                vImage = "Data/carRight" + str(random.randint(1, 4)) + ".png"
                #Creates the vehicle
                self.vehicles.append(Vehicle(vRandX, self.y, SCALE, SCALE, vSpd, vType, vImage))

        #Checks if it is a water lane
        elif(self.t == 'w'):
            #Generates random amount of cars
            randRaftAmounts = [(3, 4)]
            randRaftAmount = random.randint(randRaftAmounts[0][0], randRaftAmounts[0][1])
            #Gives a random speed
            vSpd = random.randint(3, 5)
            for i in range(randRaftAmount):
                #Gives a random x pos
                vRandX = random.randint(0, SCALE * randRaftAmounts[0][1]) * 3 + i * SCALE * randRaftAmounts[0][1] * 5
                #Assigns a type
                vType = 'l'
                #Assigns a image
                vImage = "Data/log.png"
                #Creates the vehicle
                self.vehicles.append(Vehicle(vRandX, self.y, SCALE * 2, SCALE, vSpd, vType, vImage))

    def show(self, gameWindow):
        #Displays the lane
        pygame.draw.rect(gameWindow, self.clr, (self.x, self.y, self.w, self.h))

        #Displays the collectables
        for collectable in self.collectables:
            collectable.show(gameWindow)

        #Displays the vehicles
        for vehicle in self.vehicles:
            vehicle.show(gameWindow)

    def update(self):
        for vehicle in self.vehicles:
            #Moves the vehicles
            vehicle.move()
            #Makes the vehicles loop back from on side to the other side of the screen
            vehicle.wrap()

    def addCollectable(self):
        #Creates a collectable
        self.collectables.append(Collectable(random.randint(0, WIDTH - SCALE), self.y, SCALE, SCALE, 'k', "Data/key.png"))

#Functions
def gameoverScreen(gameWindow, score):
    gameWindow.fill(BLACK)

    #Gameover text
    gameoverFont = pygame.font.SysFont("Arial Black", 100)
    gameWindow.blit(gameoverFont.render("Game Over", 1, WHITE), (WIDTH // 2 - gameoverFont.size("Game Over")[0] // 2, HEIGHT // 2 - 200)) 
    
    #Score text
    scoreFont = pygame.font.SysFont("Arial Black", 45)
    gameWindow.blit(scoreFont.render("SCORE " + str(score), 1, WHITE), (WIDTH // 2 - scoreFont.size("SCORE " + str(score))[0] // 2, HEIGHT // 2))
        
def generateLevel(lanes):
    #Selects a random lane to have the key
    randLane = random.randint(1, len(lanes) - 2)

    #Reloads the exit lane
    lanes[0] = Lane(0 * SCALE, SCALE, 'e')
    for i in range(1, len(lanes) - 1):
        #Randomizes the ground and water lanes
        randNum = random.randint(0, 1)
        if(randNum == 0):
            #Reloads the lane to ground
            lanes[i] = Lane(i * SCALE, SCALE, 'g')
            
        elif(randNum == 1):
            #Reloads the lane to water
            lanes[i] = Lane(i * SCALE, SCALE, 'w')

    #Reloads the start lane
    lanes[len(lanes) - 1] = Lane(HEIGHT - SCALE * 2, SCALE, 's')

    #Adds the collectable to the random lane
    lanes[randLane].addCollectable()
    
def keyInput(player):
    #Key input
    keys = pygame.key.get_pressed()

    #Left arrow or 'a' key
    if(keys[pygame.K_a] or keys[pygame.K_LEFT]):
        player.moveLeft()

    #Right arrow or 'd' key
    elif(keys[pygame.K_d] or keys[pygame.K_RIGHT]):
        player.moveRight()

    #Up arrow or 'w' key
    if(keys[pygame.K_w] or keys[pygame.K_UP]):
        player.moveUp()

    #Down arrow or 's' key
    elif(keys[pygame.K_s] or keys[pygame.K_DOWN]):
        player.moveDown()

    #'z' key
    if(keys[pygame.K_z]):
        generateLevel(lanes)
        player.x = WIDTH // 2 - player.w // 2
        player.y = HEIGHT - player.h * 2 + 5
        
def initClasses():
    #Creates the player
    player = Player(WIDTH // 2 - SCALE // 2, HEIGHT - SCALE * 2 + 5, SCALE - 5, SCALE - 5, 5)

    #Creates empty lanes
    lanes.append(0)
    for i in range(1, (HEIGHT // SCALE) - 2):
        lanes.append(0)

    lanes.append(0)
        
    return player, lanes
    
def start():
    pygame.init()
    gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
    gameWindow.fill(WHITE)
    pygame.display.set_caption("Frogger")
    #Inits classes
    player, lanes = initClasses()
    #Generates the level
    generateLevel(lanes)
    return gameWindow, player, lanes

def update(gameWindow, player, lanes, score):
    if(player.dead):
        #Shows the gameover screen
        gameoverScreen(gameWindow, score)
    else:
        gameWindow.fill(BLACK)
        for lane in lanes:
            #Displays the lanes and whats on them
            lane.show(gameWindow)
            #Updates the lanes and whats on them
            lane.update()
            #print(lane)

        #Displays the player
        player.show(gameWindow)
        #Gives the player collision
        score = player.col(lanes, lanes[0], gameWindow, score)
        #Moves the player if on a log
        player.moveOnLog()

        #Key input
        keyInput(player)

        #Score text
        scoreFont = pygame.font.SysFont("Arial Black", 20)
        gameWindow.blit(scoreFont.render("SCORE: " + str(score), 1, WHITE), (WIDTH // 2, HEIGHT - 30))

    return score

def main(running, score):
    gameWindow, player, lanes = start()

    while(running):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                running = False
                
        score = update(gameWindow, player, lanes, score)
        pygame.time.delay(tickSpeed)
        pygame.display.update()

    pygame.quit()


#Main
if(__name__ == "__main__"):
   main(running, score)   
