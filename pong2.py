#Author: Minh Nguyen
#Date: 11/15/2023
#Purpose: Pong game (updated version)

# I have enjoyed and had so much fun updating this game, it would be so fun to play,
# and I hope this worth some extra credit points :)

# I personally like how colorful and fun the game looks

# updated pong game that I made have 2 modes (easy and hard). you can only pick the mode when the game just launched,
# once you picked the mode, you cannot change even after you restart the game after one of the players scored the
# max of 10 points and won. you can only change the mode if you quit the game and relaunch it.
# easy mode has one ball and hard mode has two balls
# instructions will also appear on the graphics for you so no worries
# I really feel like I played a real game downloaded from appstore haha
# you can of course alter the velocities of the balls to how hard or easy you want them to be

from cs1lib import *
from random import uniform

#Variables
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
PADDLE_HEIGHT = 150
PADDLE_WIDTH = 30

# player 1 box positions
PLAYER1_X = 100
PLAYER1_Y = 0

# player 2 box positions
PLAYER2_X = 500
PLAYER2_Y = 0

# player 1 text positions
NAME1_X = 103
NAME1_Y = 35

# player 2 text positions
NAME2_X = 503
NAME2_Y = 35

# players initial scores
count1 = 0
count2 = 0

BALL_SIZE = 15 #radius of ball
#ball1's center coordinates
xb1 = 400
yb1 = 400
#ball1's velocity
vx1 = 5
vy1 = 10

#ball2's center coordinates
xb2 = 400
yb2 = 400
#ball2's velocity
vx2 = 10
vy2 = 5

START_GAME = " "
easy_ = "1"
hard_ = "2"
END_GAME = "q"

LEFT_UP = "a"
LEFT_DOWN = "z"
RIGHT_UP = "k"
RIGHT_DOWN = "m"

#initial position of left paddle (upper-left corner of 400x400 window)
left_x = 0
left_y = 0
#initial position of right paddle (lower-right corner of 400x400 window)
right_x = WINDOW_WIDTH - PADDLE_WIDTH
right_y = WINDOW_HEIGHT - PADDLE_HEIGHT

#The amount that a paddle moves when it moves.
MOVE = 15

left_up_press = False
left_down_press = False
right_up_press = False
right_down_press = False
start_game = False
easy = False
hard = False

def draw_player(x, y): # draw players boxes
    disable_stroke()
    set_fill_color(0.6, 0.2, 0.4)
    draw_rectangle(x, y, 200, 50)

def draw_name(name, x, y): # draw players names and scores
    enable_stroke()
    set_font_bold()
    set_font_size(30)
    set_stroke_color(0.2, 0.5, 0.8)
    draw_text(name, x, y)

def draw_ball(x, y): #function draws ball
    enable_stroke()
    set_stroke_width(1)
    set_fill_color(1, 1, 1)
    draw_circle(x, y, BALL_SIZE)

def draw_paddle(x, y, w, h): #function draws paddles
    disable_stroke()
    set_fill_color(1, 0.4, 0.4)
    draw_rectangle(x, y, w, h)

def main_draw(): #main draw function
    global left_x, left_y, right_x, right_y, xb1, yb1, xb2, yb2, count1, count2, easy, hard, start_game
    #set background
    set_clear_color(0.8, 0.9, 0.2)
    clear()

    # instructions to start the game or quit the game before pressing start
    if start_game == False:
        enable_stroke()
        set_font_bold()
        set_font_size(20)
        set_stroke_color(1, 1, 1)
        draw_text("press space to start", 303, 430)
        set_stroke_color(0, 0, 0)
        draw_text("press q to exit", 334, 460)
        if count1 == 0 and count2 == 0:
            set_stroke_color(0.5, 0.5, 0.9)
            draw_text("press 1 for easy mode", 293, 350)
            set_stroke_color(1, 0.1, 0.3)
            draw_text("press 2 for hard mode", 293, 380)

    # displays the players and their scores of maximum 10 on top of the graphics
    draw_player(PLAYER1_X, PLAYER1_Y)
    draw_player(PLAYER2_X, PLAYER2_Y)

    draw_name("PLAYER 1: " + str(count1), NAME1_X, NAME1_Y)
    draw_name("PLAYER 2: " + str(count2), NAME2_X, NAME2_Y)

    # draw ball

    if easy == True:
        draw_ball(xb1, yb1)

    if hard == True:
        draw_ball(xb1, yb1)
        draw_ball(xb2, yb2)


    #draw left paddle
    draw_paddle(left_x, left_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    #draw right paddle
    draw_paddle(right_x, right_y, PADDLE_WIDTH, PADDLE_HEIGHT)

    #move paddles
    move_paddle()

    #move ball
    move_ball()
    paddle_collide()
    horizontal_collide()
    vertical_collide()

    end_game()

def kpress(value):
    global left_up_press, left_down_press, right_up_press, right_down_press, start_game,\
        easy_, hard_, easy, hard
    if value == LEFT_UP:
        left_up_press = True
    if value == LEFT_DOWN:
        left_down_press = True
    if value == RIGHT_UP:
        right_up_press = True
    if value == RIGHT_DOWN:
        right_down_press = True
    if value == START_GAME:
        start_game = True
    if value == END_GAME:
        cs1_quit()
    # once choose easy or hard, you cannot change the mode of the game except when you quit and relaunch to change mode
    if value == easy_:
        easy = True
        hard_ = None
    if value == hard_:
        hard = True
        easy_ = None

#no paddle may move outside the window.
# When the left paddle hits the top window boundary, pressing a has no effect,
# and when it hits the bottom window boundary, pressing z has no effect.
# Likewise, when the right paddle hits the top window boundary, pressing k has no effect,
# and when it hits the bottom window boundary, pressing m has no effect.
# Remember that paddles move only vertically.
def move_paddle():
    global left_y, right_y, left_up_press, left_down_press, right_up_press, right_down_press
    if start_game == True: #paddles can be moved when the game starts
        if left_y >= 0:
            if left_up_press == True:
                left_y = left_y - MOVE
        if left_y <= (WINDOW_HEIGHT - PADDLE_HEIGHT):
            if left_down_press == True:
                left_y = left_y + MOVE

        if right_y >= 0:
            if right_up_press == True:
                right_y = right_y - MOVE
        if right_y <= (WINDOW_HEIGHT - PADDLE_HEIGHT):
            if right_down_press == True:
                right_y = right_y + MOVE

def move_ball(): #function updates balls position
    global xb1, yb1, vx1, vy1, xb2, yb2, vx2, vy2, start_game, easy, hard
    if easy == True:
        if start_game == True:
            xb1 = xb1 + vx1
            yb1 = yb1 + vy1
    if hard == True:
        if start_game == True:
            xb1 = xb1 + vx1
            yb1 = yb1 + vy1
            xb2 = xb2 + vx2
            yb2 = yb2 + vy2

def paddle_collide(): #function checks if the balls have collided with the inner face
    # of either paddle and updates the ball velocities
    global xb1, yb1, vx1, xb2, yb2, vx2, left_x, left_y, right_x, right_y
    if left_y <= yb1 <= left_y + PADDLE_HEIGHT and xb1 - BALL_SIZE <= left_x + PADDLE_WIDTH:
        vx1 = -vx1
        xb1 = PADDLE_WIDTH + BALL_SIZE + 1
    if right_y <= yb1 <= right_y + PADDLE_HEIGHT and xb1 + BALL_SIZE >= right_x:
        vx1 = -vx1
        xb1 = right_x - BALL_SIZE - 1
    if left_y <= yb2 <= left_y + PADDLE_HEIGHT and xb2 - BALL_SIZE <= left_x + PADDLE_WIDTH:
        vx2 = -vx2
        xb2 = PADDLE_WIDTH + BALL_SIZE + 1
    if right_y <= yb2 <= right_y + PADDLE_HEIGHT and xb2 + BALL_SIZE >= right_x:
        vx2 = -vx2
        xb2 = right_x - BALL_SIZE - 1

def horizontal_collide(): #function that checks if the balls have collided with horizontal bounds
    #and updates the balls velocities
    global yb1, vy1, yb2, vy2
    if yb1 - BALL_SIZE <= 0: #checks if the ball collided with the ceiling
        vy1 = -vy1
    if yb1 + BALL_SIZE >= 800: #checks if the ball collided with the floor
        vy1 = -vy1

    if yb2 - BALL_SIZE <= 0: #checks if the ball collided with the ceiling
        vy2 = -vy2
    if yb2 + BALL_SIZE >= 800: #checks if the ball collided with the floor
        vy2 = -vy2

def vertical_collide(): #function that checks if the balls have collided
    # with the vertical walls and resets the game if collision occurs
    global xb1, xb2, count1, count2
    if xb1 - BALL_SIZE <= 0 or xb2 - BALL_SIZE <= 0: #left vertical wall
        reset()
        count2 = count2 + 1 # updates player's score
    if xb1 + BALL_SIZE >= 800 or xb2 + BALL_SIZE >= 800: #right vertical wall
        reset()
        count1 = count1 + 1 # updates player's score

def reset(): #reset the state to the starting state
    global xb1, yb1, xb2, yb2, left_x, left_y, right_x, right_y, start_game
    xb1 = 400
    yb1 = 400
    xb2 = 400
    yb2 = 400
    left_x = 0
    left_y = 0
    right_x = WINDOW_WIDTH - PADDLE_WIDTH
    right_y = WINDOW_HEIGHT - PADDLE_HEIGHT
    start_game = False

def krelease(value): #paddles not moving when keys released.
    global left_up_press, left_down_press, right_up_press, right_down_press
    if value == LEFT_UP:
        left_up_press = False
    if value == LEFT_DOWN:
        left_down_press = False
    if value == RIGHT_UP:
        right_up_press = False
    if value == RIGHT_DOWN:
        right_down_press = False

def win(text): # display whoever wins
    enable_stroke()
    set_font_bold()
    set_font_size(50)
    set_stroke_color(uniform(0, 1), uniform(0, 1), uniform(0, 1))
    draw_text(text, 220, 380)

def restart_game(): # instructions on whether to restart or end the game when it ends
    enable_stroke()
    set_font_bold()
    set_font_size(20)
    set_stroke_color(1, 1, 1)
    draw_text("press space to restart", 300, 430)
    set_stroke_color(0, 0, 0)
    draw_text("press q to exit", 335, 460)

def end_game(): # the game ends if one of the players scores 10 points
    global count1, count2, start_game
    # whoever hits 10 points first wins and the game ends, players can choose to restart or quit game
    if count1 == 10:
        image()
        win("PLAYER 1 WIN!")
        restart_game()

        if start_game == True: # automatically start a new game
            count1 = 0
            count2 = 0

    if count2 == 10:
        image()
        win("PLAYER 2 WIN!")
        restart_game()

        if start_game == True: # # automatically start a new game
            count1 = 0
            count2 = 0

# image positions
xm = 115
ym = 115
# image velocities
vxm = 1
vym = 2
# image size in pixels
IMAGE_SIZE = 570

def image(): # cute animation to congratulate the winner
    global xm, ym, vxm, vym
    img = load_image("win.avif")
    draw_image(img, xm, ym)
    xm = xm + vxm
    ym = ym + vym
    if xm <= 0 or xm >= WINDOW_WIDTH - IMAGE_SIZE:
        vxm = -vxm
    if ym <= 0 or ym >= WINDOW_HEIGHT - IMAGE_SIZE:
        vym = -vym

start_graphics(main_draw, key_press=kpress, key_release=krelease, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)