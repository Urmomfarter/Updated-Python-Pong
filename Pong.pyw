import pygame, sys, time, math, os
import random
from random import randint as rand
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
pygame.font.init()

#800x600 looks good
fullscreen = 1
if not fullscreen:
    display_width = 800
    display_height = 600
else:
    display_width = 1600
    display_height = 900
####
Difficulty = 0 #Starts at zero
botMult = 1 + Difficulty * .05
os.environ['SDL_VIDEO_CENTERED'] = '1'
DISPLAY = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Python Pong")
clock = pygame.time.Clock()

startTime = time.time()

BlipSound = pygame.mixer.Sound(r"C:\Users\urmom\Music\Pong Blip.wav")
MissSound = pygame.mixer.Sound(r"C:\Users\urmom\Music\Pong Miss Hum.wav")

if fullscreen:
    DISPLAYSURF = pygame.display.set_mode((1600, 900), pygame.FULLSCREEN)

#####
p_score = 0
b_score = 0
#####
def chooseFont(a,b):
    return pygame.font.SysFont(str(a), int(b))
class userRectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

paddleH = int(display_height / 20 + 40.5) * 1
def game_loop(a):
    global p_score,b_score,paddleH,display_width,display_height,startTime
    fps = 300
    startTime = time.time()

    
    upBool,downBool = 0,0
    DISPLAY.fill((0,0,0))
    
    movementPx = int((display_height / 60 + .5) * 1.5)
    paddleW = int(display_width / 200 + 5.5)
    ball_w = 10
    
    player = userRectangle(20,display_height/2 - paddleH/2,paddleW,paddleH)
    bot = userRectangle(display_width-20-paddleW,display_height/2-paddleH/2,paddleW,paddleH)
    ball = userRectangle(display_width/2 - ball_w/2,display_height/2-ball_w/2-3,ball_w,ball_w)

    ballSlope = ()
    ballSpeed = 6 * (100)/fps / (500 / display_width)
    ballDeltaX = random.uniform(-ballSpeed,-ballSpeed / 2)/2
    ballDeltaY = (ballSpeed - abs(ballDeltaX*2))*.5
    if rand(0,1):
        ballDeltaX *= -1

    totalDistance = display_height/2

    altkey = 0
    f4key = 0
    
    if rand(0,1) == 1:
        ballDeltaY *= -1
    roundOver = 0
    while 1:
        if roundOver:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                
                if event.key==pygame.K_RALT or event.key==pygame.K_LALT:
                    altkey=1
                elif event.key==pygame.K_F4:
                    f4key=1
                elif event.key == pygame.K_DOWN:
                    downBool = 1
                elif event.key == pygame.K_UP:
                    upBool = 1
                if f4key and altkey:
                    pygame.quit()
            if event.type == pygame.KEYUP:
                downBool,upBool,altkey,f4key = 0,0,0,0
        #Any of the code that runs during the program goes here
        if not player.y + player.height + 1 < display_height:
            downBool = 0
            player.y = display_height - player.height - 1
        if not player.y > 1:
            upBool = 0
            player.y = 1
        if upBool:
            player.y -= movementPx * (60 / fps)
        elif downBool:
            player.y += movementPx* (60 / fps)
        if time.time() - startTime > 1: #move ball, bot
            if ball.x > 1 and ball.x + ball.width < display_width: #On the stage
                if ball.y > 1 and ball.y + ball.height < display_height - 1: #Within stage vertically
                    if player.x  <= ball.x <= player.x + player.width: #If ball_x is within player x
                        bC_Y = ball.y + ball.height/2 #Ball center Y
                        if player.y <= bC_Y <= player.y + player.height: #If bLC_Y within player y
                            BlipSound.play()
                            ballSlope = ((player.y + player.height / 2) - bC_Y) / ((player.x + player.width - player.height/2) - ball.x)
                            z = ballSpeed
                            s = ballSlope
                            ballDeltaY = math.sqrt(abs(z**2*(-4/s**2-4)))/(2*((1/s**2)+1))
                            ballDeltaX = math.sqrt(abs(ballSpeed ** 2 - ballDeltaY ** 2))
                            ball.x += player.width
                            if bC_Y < player.y + player.height/2:
                                ballDeltaY *= -1
                            ballSpeed *= 1.05
                            ###############
                            #Bot AI
                            ###############
                    elif bot.x  <= ball.x + ball.width <= bot.x + bot.width: #If ball_x is within bot x:
                        bC_Y = ball.y + ball.height/2 #Ball center Y
                        if bot.x  <= ball.x + ball.width <= bot.x + bot.width: #If ball_x is within bot x
                            if bot.y <= bC_Y <= bot.y + bot.height: #If bLC_Y within bot y
                                BlipSound.play()
                                ballSlope = ((bot.y + bot.height / 2) - bC_Y) / ((bot.x + bot.height / 2) - (ball.x + ball.width))
                                z = ballSpeed
                                s = ballSlope
                                ballDeltaY = math.sqrt(abs(z**2*(-4/s**2-4)))/(2*((1/s**2)+1))
                                ballDeltaX = math.sqrt(ballSpeed ** 2 - ballDeltaY ** 2)
                                ball.x -= bot.width
                                if bC_Y < bot.y + bot.height/2:
                                    ballDeltaY *= -1
                                ballDeltaX *= -1
                                ballSpeed *= 1.05
                        
                else:
                    ballDeltaY *= -1
            else:
                if ball.x < display_width/2:
                    b_score += 1
                else:
                    p_score += 1
                return 0
            ball.y += ballDeltaY
            ball.x += ballDeltaX
        #Bot movement
        if ballDeltaX > 0:
            totalDistance = ball.y + ball.height/2
            distToPrediction = abs(bot.y + bot.height/2 - totalDistance)
            isAbleToMove = 1
            botSlowDown = 1
            if distToPrediction <= 1:
                isAbleToMove = 0
            elif distToPrediction <= movementPx * (60 / fps):
                botSlowdown = 2
            if isAbleToMove:
                if bot.y + bot.height/2 < totalDistance:
                    if bot.y + bot.height < display_height - 1:
                        bot.y += movementPx * (60 / fps) / botSlowDown * botMult
                else:
                    if bot.y > 1:
                        bot.y -= movementPx * (60 / fps) / botSlowDown * botMult
        TextToRender = ""
        if p_score < 10:
            TextToRender += "0"
        TextToRender += (str(p_score) + " - ")
        if b_score < 10:
            TextToRender += '0'
        TextToRender += str(b_score)
        
        DISPLAY.fill((0,0,0))

        netw=10
        neth = 30
        net = pygame.Surface((netw,neth))
        net.set_alpha(128)
        net.fill((255,255,255))
        for i in range(int(display_height / (neth))):
            DISPLAY.blit(net, (display_width/2 - netw/2,2 * neth * i))
            
        pygame.draw.rect(DISPLAY, (255,255,255), (player.x,player.y,player.width,player.height), 0)
        pygame.draw.rect(DISPLAY, (255,255,255), (bot.x,bot.y,bot.width,bot.height), 0)
        pygame.draw.rect(DISPLAY, (255,255,255), (ball.x,ball.y,ball.width,ball.height), 0)
        textsurface = (chooseFont("monospace",50)).render(TextToRender,1,(255,255,255))
        DISPLAY.blit(textsurface,(display_width/2 - 2 * 50 - 5,20))
        pygame.display.update()
        clock.tick(fps)

def wait(Time):
    global startTime
    while time.time() - startTime < Time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        clock.tick(15)

#wait(1) #Before game starts

while 1:
    game_loop(1)
    MissSound.play()
    startTime = time.time()
    wait(2.5)
#pygame.quit()
