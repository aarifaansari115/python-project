# Import required modules
import turtle
import time
import random

# Create game window
SCREEN_WIDTH = 600      # Width of game window
SCREEN_HEIGHT = 600     # Height of game window
GRID_SIZE = 20          # Movement step size (snake moves 20 pixels at a time)
INITIAL_DELAY = 0.12    # Initial game speed
win = turtle.Screen()
win.title("Snake Game")
win.bgcolor("black")
win.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

# Draw simple border
border = turtle.Turtle()
border.speed(0)
border.color("white")
border.penup()
border.goto(-290, -290)
border.pendown()

for i in range(4):          # Draw square border
    border.forward(580)
    border.left(90)

border.hideturtle()


# Create snake head
head = turtle.Turtle()
head.shape("circle")
head.color("green")
head.penup()
head.goto(0,0)
head.direction = "stop"

# Create food
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(0,100)

# Snake body list
segments = []

# Score
score = 0

# Score display
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write("Score : 0", align="center", font=("Arial",18,"bold"))


# Movement functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"


# Move snake
def move():

    if head.direction == "up":
        head.sety(head.ycor()+20)

    if head.direction == "down":
        head.sety(head.ycor()-20)

    if head.direction == "left":
        head.setx(head.xcor()-20)

    if head.direction == "right":
        head.setx(head.xcor()+20)


# Keyboard control
win.listen()
win.onkeypress(go_up,"Up")
win.onkeypress(go_down,"Down")
win.onkeypress(go_left,"Left")
win.onkeypress(go_right,"Right")


# Game loop
while True:

    win.update()

    # Border collision
    if head.xcor()>280 or head.xcor()<-280 or head.ycor()>280 or head.ycor()<-280:
        time.sleep(1)
        head.goto(0,0)
        head.direction="stop"

        # Remove body segments
        for segment in segments:
            segment.goto(1000,1000)

        segments.clear()

        score = 0
        pen.clear()
        pen.write("Score : {}".format(score), align="center", font=("Arial",18,"bold"))


    # Food collision
    if head.distance(food) < 20:

        # Move food randomly
        x = random.randint(-260,260)
        y = random.randint(-260,260)
        food.goto(x,y)

        # Create new body segment
        new_segment = turtle.Turtle()
        new_segment.shape("circle")
        new_segment.color("lightgreen")
        new_segment.penup()
        segments.append(new_segment)

        # Increase score
        score += 10
        pen.clear()
        pen.write("Score : {}".format(score), align="center", font=("Arial",18,"bold"))


    # Move body segments
    for i in range(len(segments)-1,0,-1):
        x = segments[i-1].xcor()
        y = segments[i-1].ycor()
        segments[i].goto(x,y)

    if len(segments)>0:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    time.sleep(0.1)


win.mainloop()