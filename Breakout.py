# File: Breakout.py

"""
This program (once you have finished it) implements the Breakout game.
"""

from pgl import GWindow, GOval, GRect, GLabel
import random

# Constants

GWINDOW_WIDTH = 360               # Width of the graphics window
GWINDOW_HEIGHT = 600              # Height of the graphics window
N_ROWS = 10                       # Number of brick rows
N_COLS = 10                       # Number of brick columns
BRICK_ASPECT_RATIO = 4 / 1        # Width to height ratio of a brick
BRICK_TO_BALL_RATIO = 3 / 2       # Ratio of brick width to ball size
BRICK_TO_PADDLE_RATIO = 2 / 3     # Ratio of brick to paddle width
BRICK_SEP = 2                     # Separation between bricks
TOP_FRACTION = 0.1                # Fraction of window above bricks
BOTTOM_FRACTION = 0.05            # Fraction of window below paddle
N_BALLS = 3                       # Number of balls in a game
TIME_STEP = 10                    # Time step in milliseconds
INITIAL_Y_VELOCITY = 3.0          # Starting y velocity downward
MIN_X_VELOCITY = 1.0              # Minimum random x velocity
MAX_X_VELOCITY = 3.0              # Maximum random x velocity

# Derived constants

BRICK_WIDTH = (GWINDOW_WIDTH - (N_COLS + 1) * BRICK_SEP) / N_COLS
BRICK_HEIGHT = BRICK_WIDTH / BRICK_ASPECT_RATIO
PADDLE_WIDTH = BRICK_WIDTH / BRICK_TO_PADDLE_RATIO
PADDLE_HEIGHT = BRICK_HEIGHT / BRICK_TO_PADDLE_RATIO
PADDLE_Y = (1 - BOTTOM_FRACTION) * GWINDOW_HEIGHT - PADDLE_HEIGHT
BALL_SIZE = BRICK_WIDTH / BRICK_TO_BALL_RATIO

# Function: Breakout

def Breakout():
	"""
	The main program for the Breakout game.
	"""
	def mousemoveAction(e):
		paddle_X = paddle.getX()
		dx = e.getX() - paddle_X
		if 0 <= dx + paddle_X <= GWINDOW_WIDTH - PADDLE_WIDTH:
			paddle.move(dx, 0)
		elif 0 > dx + paddle_X:
			paddle.setLocation(0, PADDLE_Y)
		else:
			paddle.setLocation(GWINDOW_WIDTH - PADDLE_WIDTH, PADDLE_Y)

	def AnimatedBall():
		def step():
			nonlocal vx, vy, ball, bricks_hit, balls_left, x_text, y_text
			collider = getCollidingObject()
			if ball.getX() < 0 or ball.getX() > GWINDOW_WIDTH - BALL_SIZE:
				vx *= -1
			elif ball.getY() < 0:
				vy *= -1
			elif ball.getY() > GWINDOW_HEIGHT - BALL_SIZE:
				timer.stop()
				gw.remove(ball)
				balls_left -= 1
				if balls_left > 0:
					ball = GOval((GWINDOW_WIDTH - BALL_SIZE) / 2, (GWINDOW_HEIGHT - BALL_SIZE) / 2, BALL_SIZE, BALL_SIZE)
					ball.setFilled(True)
					gw.add(ball)
					gw.add(instruct)
				else:
					msg = GLabel('You Lose.')
					msg.setColor('red')
					msg.setFont('bold 36px sans-serif')
					x = (GWINDOW_WIDTH - msg.getWidth()) / 2
					y = (GWINDOW_HEIGHT - msg.getHeight()) / 2
					gw.add(msg, x, y)
			if collider == paddle:
				vy *= -1
			elif not (collider == paddle or collider ==gw.getElementAt(x_text, y_text)) and collider is not None:
				vy *= -1
				gw.remove(collider)
				bricks_hit += 1
				if bricks_hit == N_COLS * N_ROWS:
					timer.stop()
					msg = GLabel('You Win!')
					msg.setColor('green')
					msg.setFont('bold 36px sans-serif')
					x = (GWINDOW_WIDTH - msg.getWidth()) / 2
					y = (GWINDOW_HEIGHT - msg.getHeight()) / 2
					gw.add(msg, x, y)
			ball.move(vx,vy)

			gw.remove(gw.getElementAt(x_text,y_text))
			lives = GLabel('Lives: ' + str(balls_left))
			gw.add(lives, x_text, y_text)


		vx = random.choice([-1, 1]) * random.uniform(MIN_X_VELOCITY, MAX_X_VELOCITY)
		vy = INITIAL_Y_VELOCITY
		x_text = 20
		y_text = GWINDOW_HEIGHT - 10
		timer = gw.createTimer(step, TIME_STEP)
		timer.setRepeats(True)
		timer.start()

	def clickAction(e):
		gw.remove(instruct)
		AnimatedBall()

	def getCollidingObject():
		loc = gw.getElementAt(ball.getX(), ball.getY())
		if loc is not None:
			return loc
		else:
			loc = gw.getElementAt(ball.getX() + BALL_SIZE, ball.getY())
			if loc is not None:
				return loc
			else:
				loc = gw.getElementAt(ball.getX(), ball.getY() + BALL_SIZE)
				if loc is not None:
					return loc
				else:
					loc = gw.getElementAt(ball.getX() + BALL_SIZE, ball.getY() + BALL_SIZE)
					return loc

	random.seed()
	gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)

	colors = ['red', 'red', 'orange', 'orange', 'green', 'green', 'cyan', 'cyan', 'blue', 'blue']
	for row in range(N_ROWS):
		for col in range(N_COLS):
			rect = GRect(((GWINDOW_WIDTH - ((N_COLS * (BRICK_WIDTH + BRICK_SEP)) - BRICK_SEP)) / 2) + (row * (BRICK_WIDTH + BRICK_SEP)),
				(TOP_FRACTION * GWINDOW_HEIGHT) + (col * (BRICK_HEIGHT + BRICK_SEP)), BRICK_WIDTH, BRICK_HEIGHT)
			rect.setFilled(True)
			rect.setColor(colors[col])
			gw.add(rect)

	paddle = GRect((GWINDOW_WIDTH - PADDLE_WIDTH) / 2, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
	paddle.setFilled(True)
	gw.add(paddle)
	gw.addEventListener('mousemove', mousemoveAction)

	ball = GOval((GWINDOW_WIDTH - BALL_SIZE) / 2, (GWINDOW_HEIGHT - BALL_SIZE) / 2, BALL_SIZE, BALL_SIZE)
	ball.setFilled(True)
	gw.add(ball)
	gw.addEventListener('click', clickAction)

	instruct = GLabel('Click to Start!')
	instruct.setFont('bold 24px sans-serif')
	x_inst = (GWINDOW_WIDTH - instruct.getWidth()) / 2
	y_inst = ((GWINDOW_HEIGHT - instruct.getHeight()) / 2) + (3 * BALL_SIZE)
	gw.add(instruct, x_inst, y_inst)

	balls_left = N_BALLS
	bricks_hit = 0

# Startup code

if (__name__ == "__main__"):
    Breakout()
