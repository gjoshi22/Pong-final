#Gunjan Joshi
#Pong in pygame
import pygame, sys
from pygame.locals import *
import random

pygame.init()         
display = pygame.display.set_mode([600,400])
pygame.display.set_caption('Pong')
pygame.init()
fps = pygame.time.Clock()

#define global variables
widthdisplay = 600
heightdisplay = 400       
radiusofball = 15
widthofpad = 8
heightofpad = 80
posofball = [widthdisplay / 2, heightdisplay / 2]
velofball = [1,1]
posofpaddle1 = 160
posofpaddle2 = 160
velofpaddle1 = [0,0]
velofpaddle2 = [0,0]
score1 = 0
score2 = 0
done = False


def spawn_ball(direction):
    # spawn the ball with random velocity
    global posofball, velofball 
    posofball = [widthdisplay / 2, heightdisplay / 2]
    if direction == "right":
        velofball = [random.randrange(3, 5), -random.randrange(3, 5)]
    if direction == "left":
        velofball = [-random.randrange(3, 5), -random.randrange(3, 5)]

def new_game():
    # reset the paddles and the ball to their default positions
    # reset the scores and spawn the ball with random direction and velocity   
    global posofpaddle1, posofpaddle2, velofpaddle1, velofpaddle2 
    global score1, score2  
    number = random.randrange(1,3)
    if number == 1:
        spawn_ball("right")
    if number == 2:
        spawn_ball("left")
        
    posofpaddle1 = 160
    posofpaddle2 = 160
    score1 = 0
    score2 = 0
    posofball = [widthdisplay / 2, heightdisplay / 2]
    
def draw(canvas):    
    global score1, score2, posofpaddle1, posofpaddle2, posofball, velofball, velofpaddle1, velofpaddle2      
    
    # draw the table
    display.fill((0,0,0))
    pygame.draw.line(display,(255,255,255),[widthdisplay / 2, 0],[widthdisplay / 2, heightdisplay],1)
    pygame.draw.line(display,(255,255,255),[widthofpad, 0],[widthofpad, heightdisplay], 1)
    pygame.draw.line(display,(255,255,255),[widthdisplay - widthofpad, 0],[widthdisplay - widthofpad, heightdisplay], 1)
        
    # update the ball's position adding the velocity in both axis
    posofball[0] += velofball[0]
    posofball[1] += velofball[1]
    
    # identify collision 
    # if the ball hits the ceiling or the floor the velocity in the y axis changes sign
    
    if int(posofball[1]) >= (heightdisplay - radiusofball):
        velofball[1] = -velofball[1] 
    if int(posofball[1]) <= radiusofball:
        velofball[1] = -velofball[1]
    
    # if the ball hits the paddle the velocity in the x axis increments and changes sign
    # if the ball hits the wall it calls the spawn function and updates the score
    
    if int(posofball[0]) >= (widthdisplay - widthofpad - radiusofball):
        if posofpaddle2 + 80 >= posofball[1] >= posofpaddle2:
            velofball[0] = -1.1 * velofball[0]
        else: 
            spawn_ball("left")
            score1 += 1
    if int(posofball[0]) <= (widthofpad + radiusofball):
        if posofpaddle1 + 80 >= posofball[1] >= posofpaddle1:
            velofball[0] = -1.1 * velofball[0]
        else:
            spawn_ball("right")
            score2 += 1
 
    # draw ball
    pygame.draw.circle(display,(255,255,255),(int(posofball[0]),int(posofball[1])),radiusofball) 
    # draw paddles
    pygame.draw.line(display,(255,255,255),[widthofpad / 2, posofpaddle1], [widthofpad / 2, posofpaddle1 + heightofpad], widthofpad)
    pygame.draw.line(display,(255,255,255),[widthdisplay - widthofpad / 2, posofpaddle2], [widthdisplay - widthofpad / 2, posofpaddle2 + heightofpad], widthofpad)
  
   # update the paddles' position adding the velocity 
   # if a paddle reaches the floor or the ceiling, it stops
                
    posofpaddle1 += velofpaddle1[1]
    if posofpaddle1 <= 0:        
        velofpaddle1[1] = 0
    if posofpaddle1 >= 320:
        velofpaddle1[1] = 0
        
    posofpaddle2 += velofpaddle2[1]
    if posofpaddle2 <= 0:
        velofpaddle2[1] = 0
    if posofpaddle2 >= 320:
        velofpaddle2[1] = 0
    
    # draw each players' score in the display
    s1 = pygame.font.SysFont("Comic Sans MS", 25)
    player1 = s1.render("Score: "+ str(score1), 1, (0,255,0))
    display.blit(player1, (50,20))

    s2 = pygame.font.SysFont("Comic Sans MS", 25)
    player2 = s2.render("Score: "+ str(score2), 1, (0,255,0))
    display.blit(player2, (470, 20))  
    

     
       
def keydown(event):
    global velofpaddle1, velofpaddle2
    # set the velocity of the paddles when the buttons are pressed
    
    if event.key == K_w:
        velofpaddle1[1] = -5
    elif event.key == K_s:
        velofpaddle1[1] = 5
   
def keyup(event):
    # paddle's velocity returns to 0 when the button is released
    global velofpaddle1, velofpaddle2
    if event.key in (K_w, K_s):
        velofpaddle1[1] = 0
    

new_game()
def automaticpaddle2():
        
    if posofpaddle2 < posofball[1] + 40 and posofpaddle2 <= 320 and posofball[0] > 150:
        velofpaddle2[1] = 3
    if posofpaddle2 > posofball[1] - 40 and posofpaddle2 >= 0 and posofball[0] > 150:
        velofpaddle2[1] = -3
    if posofball[0] < 100 and velofpaddle2[1] == 3:
        velofpaddle2[1] += -3
    if posofball[0] < 100 and velofpaddle2[1] == -3:
        velofpaddle2[1] += 3  

# game loop        
while done == False:      
    draw(display)
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
    automaticpaddle2()        
    pygame.display.update()
    fps.tick(60)

# learned pygame methods from: https://www.pygame.org/docs/tut/PygameIntro.html