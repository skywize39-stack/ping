"""
Author: Konstantinos Angelopoulos
Date: 13/04/2020
All rights reserved.
Feel free to use and modify and if you like it give it a star.

=========================

Simple Ping Pong Game using turtle graphics

Up - Down for the right player
W/w - S/s for the left player
Enter - Space for pause
Q/q - Esc for quitting
M/m - for muting
R/r - for restart

=========================

No score Limit
Level increases every 5 points
Compatible with Python 2.7.X+ and Python 3.6.X+
Compatible with Linux and Windows
Enjoy!

"""
import os
import turtle
if os.name == 'nt':
    import winsound
import time
import sys
# Check for python2 and python3
try:
    from tkinter import *  # python3
except:
    from Tkinter import *  # python2


class PingPong:

    def __init__(self):
        # get names first
        self._root = None  # init for tkinter
        self._name1 = None  # init names for tkinter
        self._name2 = None  # init names for tkinter
        self._start = False  # flag for get name loop
        self._player_left_name = None  # left player name
        self._player_right_name = None  # right player name
        # get names
        while not self._start:
            self.get_names()  # get names
        # init for turtle
        self._screen = turtle.Screen()  # Initialize screen
        self._screen.title("Ping - Pong")  # Title screen
        self._screen.bgcolor("royal blue")  # background color
        self._screen.setup(width=960, height=540)  # screen dimensions
        self._screen.tracer(0)  # frame delay
        self.player_right = None  # store right player
        self.player_left = None  # store left player
        self.ball = None  # store ball
        self._move = 15  # move distance player
        self._score = None  # store score
        self.player_right_score = 0  # right player score
        self.player_left_score = 0  # left player score
        self._sound = 'bounce.wav'  # bounce sound
        self._sound_away = 'bounce_away.wav'  # lose sound
        self._done = True  # flag to terminate game
        self._pause = True  # flag to pause game
        self._level_up = False  # flag to level up
        self._level_limit = 5  # score limit to change level
        self._score_board = 1  # store score
        self._level_board = None  # store levels
        self._mute = False  # flag to mute sounds
        self.make_player_left()  # create left player
        self.make_player_right()  # create right player
        self.make_ball()  # create ball
        self.make_score()  # create score
        self.make_level()  # create levels
        self.listen()  # start listen key presses

    def get_names(self):
        # start main loop for player names
        while not self._start:
            self._root = Tk()  # tkinter window
            self._root.geometry("500x285")  # window size
            self._root.title("")  # Empty title
            self._name1 = StringVar()  # init names for tkinter
            self._name2 = StringVar()  # init names for tkintee
            # Label 1 title
            Label(self._root, text="Enter Players Name", font="Helvetica 18 bold").pack()
            Label(self._root).pack()  # spacer
            Label(self._root, text="Player 1", font="Helvetica 18 bold", fg='#49A').pack()
            Entry(self._root, textvariable=self._name1, width=30).pack(ipady=3)
            Label(self._root, text="Player 2", font="Helvetica 18 bold", fg='#49A').pack()
            Entry(self._root, textvariable=self._name2, width=30).pack(ipady=3)
            Label(self._root).pack()  # spacer
            Button(self._root, text="Submit", command=self.start_game, fg="red", bg='blue', font="Helvetica 18 bold").pack()
            self._root.mainloop()  # start mainloop

        # delete for python2 and python3 to ensure concurrency with turtle, which is a tkinter subsystem
        try:
            del sys.modules['tkinter']  # python3
        except:
            del sys.modules['Tkinter']  # python2

    def start_game(self):
        # check if names are not empty
        if self._name1.get() == "" or self._name2.get() == "":
            # delete label if exists
            t = self._root.pack_slaves()  # get all labels
            if t[-1].widgetName == "label":
                t[-1].destroy()
            # make new label to inform user
            Label(self._root, text="Names cannot be empty", font="Helvetica 18 bold", fg="red").pack()
        else:
            self._start = True  # flag for closing
            self._player_left_name = self._name1.get()  # left player name
            self._player_right_name = self._name2.get()  # right player name
            # close all and quit
            self._root.destroy()

    # make left player
    def make_player_left(self):
        self.player_right = turtle.Turtle()  # left player
        self.player_right.speed(0)  # no speed
        self.player_right.shape("square")  # shape
        self.player_right.shapesize(stretch_wid=6, stretch_len=1)  # shape size
        self.player_right.color("medium aquamarine")  # color
        self.player_right.penup()  # draw
        self.player_right.goto(450, 0)  # position
        self.player_left_score = 0  # score init

    def make_player_right(self):
        self.player_left = turtle.Turtle()  # left player
        self.player_left.speed(0)  # no speed
        self.player_left.shape("square")  # shape
        self.player_left.shapesize(stretch_wid=6, stretch_len=1)  # shape size
        self.player_left.color("medium aquamarine")  # color
        self.player_left.penup()  # draw
        self.player_left.goto(-450, 0)  # position
        self.player_right_score = 0  # score init

    def make_ball(self):
        self.ball = turtle.Turtle()  # ball
        self.ball.speed(0)  # no speed
        self.ball.shape("circle")  # shape
        self.ball.color("orange red")  # shape size
        self.ball.penup()  # draw
        self.ball.goto(0, 0)  # position
        self.ball.dx = .2  # velocity
        self.ball.dy = .2  # velocity

    def make_score(self):
        self._score = turtle.Turtle()  # score
        self._score.speed(0)  # speed
        self._score.color('black')  # color
        self._score.penup()  # draw
        self._score.hideturtle()  # don't show shape
        self._score.goto(0, 0)  # position
        # write score
        self._score.write("{}".format(self.player_left_score + self.player_right_score), align="center", font=("Arial", 24, "normal"))

    def make_level(self):
        self._level_board = turtle.Turtle()  # level
        self._level_board.speed(0)  # speed
        self._level_board.color('black')  # color
        self._level_board.penup()  # draw
        self._level_board.hideturtle()  # don't show shape
        self._level_board.goto(0, 230)  # shape
        # write level
        self._level_board.write("Level {}".format(self._score_board), align="center", font=("Arial", 24, "normal"))

    def player_left_move_up(self):
        # move left player up
        self._pause = False
        if self.player_left.ycor() <= 270 - 70:
            self.player_left.sety(self.player_left.ycor() + self._move)

    def player_left_move_down(self):
        # move left player down
        self._pause = False
        if self.player_left.ycor() >= -270 + 75:
            self.player_left.sety(self.player_left.ycor() - self._move)

    def player_right_move_up(self):
        # move right player up
        self._pause = False
        if self.player_right.ycor() <= 270 - 70:
            self.player_right.sety(self.player_right.ycor() + self._move)

    def player_right_move_down(self):
        # move right player down
        self._pause = False
        if self.player_right.ycor() >= -270 + 75:
            self.player_right.sety(self.player_right.ycor() - self._move)

    def pause(self):
        # check pause state
        if self._pause:
            self._pause = False
        else:
            self._pause = True

    def level_up(self):
        self.ball.dx += .1  # increase ball speed
        self.ball.dy += .1  # increase ball speed
        self._move += 5  # increase player speed
        self._score_board += 1  # increase score
        self._level_board.clear()  # increase level
        # increase level
        self._level_board.write("Level {}".format(self._score_board), align="center", font=("Arial", 24, "normal"))

    def restart(self):
        # restart game
        self.player_left_score = 0
        self.player_right_score = 0
        self.ball.goto(0, 0)
        self.ball.dx = .2
        self.ball.dy = .2
        self._move = 15
        self.player_left.goto(-450, 0)
        self.player_right.goto(450, 0)
        self._score.clear()
        self._score.write("{}".format(self.player_left_score + self.player_right_score), align="center", font=("Arial", 24, "normal"))

    def play_sound(self):
        # play sound bounce asynch
        # check linux or windows
        if os.name == 'nt':
            if not self._mute:
                winsound.PlaySound(self._sound, winsound.SND_ASYNC)
        else:
            os.system('aplay {}&'.format(self._sound))

    def play_sound_bounce_away(self):
        # play sound game over asynch
        # check linux or windows
        if os.name == 'nt':
            if not self._mute:
                winsound.PlaySound(self._sound_away, winsound.SND_ASYNC)
        else:
            os.system('aplay {}&'.format(self._sound_away))

    def mute_sound(self):
        # check pause state
        if self._mute:
            self._mute = False
        else:
            self._mute = True

    def quit(self):
        # exit application
        self._done = False
        self._screen.exitonclick()
        
    def listen(self):
        # listen key presses
        self._screen.listen()
        # for python 2 and python 3
        if sys.version_info[0] < 3:
            self._screen.onkey(self.player_left_move_up, 'w')
            self._screen.onkey(self.player_left_move_up, 'W')
            self._screen.onkey(self.player_left_move_down, 's')
            self._screen.onkey(self.player_left_move_down, 'S')
            self._screen.onkey(self.player_right_move_up, 'Up')
            self._screen.onkey(self.player_right_move_down, 'Down')
            self._screen.onkey(self.pause, 'space')
            self._screen.onkey(self.pause, 'Return')
            self._screen.onkey(self.quit, 'q')
            self._screen.onkey(self.quit, 'Q')
            self._screen.onkey(self.quit, 'Escape')
            self._screen.onkey(self.mute_sound, 'm')
            self._screen.onkey(self.mute_sound, 'M')
            self._screen.onkey(self.restart, 'r')
            self._screen.onkey(self.restart, 'R')
        else:
            self._screen.onkeypress(self.player_left_move_up, 'w')
            self._screen.onkeypress(self.player_left_move_up, 'W')
            self._screen.onkeypress(self.player_left_move_down, 's')
            self._screen.onkeypress(self.player_left_move_down, 'S')
            self._screen.onkeypress(self.player_right_move_up, 'Up')
            self._screen.onkeypress(self.player_right_move_down, 'Down')
            self._screen.onkeypress(self.pause, 'space')
            self._screen.onkeypress(self.pause, 'Return')
            self._screen.onkeypress(self.quit, 'q')
            self._screen.onkeypress(self.quit, 'Q')
            self._screen.onkeypress(self.quit, 'Escape')
            self._screen.onkeypress(self.mute_sound, 'm')
            self._screen.onkeypress(self.mute_sound, 'M')
            self._screen.onkeypress(self.restart, 'r')
            self._screen.onkeypress(self.restart, 'R')

    def run(self):

        # main loop
        while self._done:

            # update screen
            self._screen.update()

            # check pause
            if not self._pause:

                # check level up
                if self.player_left_score > 0 and self.player_right_score > 0:
                    if self.player_left_score == self._level_limit and self.player_right_score == self._level_limit:
                        self._level_up = True
                        self._level_limit += 5

                # level up
                if self._level_up:
                    self.level_up()
                    self._level_up = False

                # move ball
                self.ball.setx(self.ball.xcor() + self.ball.dx)
                self.ball.sety(self.ball.ycor() + self.ball.dy)

                # check if ball hit wall
                if self.ball.ycor() >= 260:
                    self.ball.sety(260)
                    self.ball.dy *= -1
                    self.play_sound()

                # check if ball hit wall
                if self.ball.ycor() <= -255:
                    self.ball.sety(-255)
                    self.ball.dy *= -1
                    self.play_sound()

                # check if ball out of bounds
                if self.ball.xcor() >= 470:
                    self.play_sound_bounce_away()
                    self._score.clear()
                    self._score.write("<~~~~ {} WON!!!!!".format(self._player_left_name), align="center", font=("Arial", 24, "normal"))
                    time.sleep(5)
                    self.restart()

                # check if ball out of bounds
                if self.ball.xcor() <= -470:
                    self.play_sound_bounce_away()
                    self._score.clear()
                    self._score.write("{} WON!!!!!! ~~~~>".format(self._player_right_name), align="center", font=("Arial", 24, "normal"))
                    time.sleep(5)
                    self.restart()

                # check if player hit ball
                if 430 <= self.ball.xcor() <= 440 and self.player_right.ycor() - 70 <= self.ball.ycor() <= self.player_right.ycor() + 70:
                    self.ball.setx(430)
                    self.ball.dx *= -1
                    self.play_sound()
                    self.player_right_score += 1
                    # update score
                    self._score.clear()
                    self._score.write("{}".format(self.player_left_score + self.player_right_score), align="center", font=("Arial", 24, "normal"))

                # check if player hit ball
                if -440 <= self.ball.xcor() <= -430 and self.player_left.ycor() - 70 <= self.ball.ycor() <= self.player_left.ycor() + 70:
                    self.ball.setx(-430)
                    self.ball.dx *= -1
                    self.play_sound()
                    self.player_left_score += 1
                    # update score
                    self._score.clear()
                    self._score.write("{}".format(self.player_left_score + self.player_right_score), align="center", font=("Arial", 24, "normal"))


if __name__ == "__main__":
    game = PingPong()
    game.run()
