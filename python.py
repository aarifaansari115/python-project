# ==========================================================
#           ULTIMATE PROFESSIONAL SNAKE GAME
#                 (10/10 PROJECT LEVEL)
# ==========================================================

# Importing required modules
import turtle      # Used for graphics and game window
import time        # Used to control speed (delay)
import random      # Used to generate random food position

# ==========================================================
# CONSTANTS (Fixed configuration values)
# ==========================================================

SCREEN_WIDTH = 600      # Width of game window
SCREEN_HEIGHT = 600     # Height of game window
GRID_SIZE = 20          # Movement step size (snake moves 20 pixels at a time)
INITIAL_DELAY = 0.12    # Initial game speed
HIGH_SCORE_FILE = "highscore.txt"  # File to store high score

# ==========================================================
# SNAKE CLASS (Handles snake behavior)
# ==========================================================

class Snake:
    def __init__(self):
        self.segments = []      # List to store snake body parts
        self.create_head()      # Create snake head
        self.direction = "stop" # Initial direction
        self.frame = 0          # Used for tongue animation timing

    # -----------------------------
    # CREATE HEAD
    # -----------------------------
    def create_head(self):
        self.head = turtle.Turtle()        # Create turtle object for head
        self.head.shape("circle")          # Head shape
        self.head.color("#e5e9e7")         # Bright green color
        self.head.shapesize(1.3)           # Slightly bigger size
        self.head.penup()                  # Disable drawing lines
        self.head.goto(0, 0)               # Start at center

        # Create left eye
        self.left_eye = turtle.Turtle()
        self.left_eye.shape("circle")
        self.left_eye.color("white")
        self.left_eye.shapesize(0.25)
        self.left_eye.penup()

        # Create right eye
        self.right_eye = turtle.Turtle()
        self.right_eye.shape("circle")
        self.right_eye.color("white")
        self.right_eye.shapesize(0.25)
        self.right_eye.penup()

        # Create tongue
        self.tongue = turtle.Turtle()
        self.tongue.shape("square")
        self.tongue.color("red")
        self.tongue.shapesize(0.1, 0.5)
        self.tongue.penup()

    # -----------------------------
    # MOVE SNAKE
    # -----------------------------
    def move(self):

        # Move body segments from last to first
        for i in range(len(self.segments)-1, 0, -1):
            self.segments[i].goto(self.segments[i-1].pos())

        # First segment follows head
        if len(self.segments) > 0:
            self.segments[0].goto(self.head.pos())

        # Get current head position
        x = self.head.xcor()
        y = self.head.ycor()

        # Move head based on direction
        if self.direction == "up":
            self.head.sety(y + 20)
        if self.direction == "down":
            self.head.sety(y - 20)
        if self.direction == "left":
            self.head.setx(x - 20)
        if self.direction == "right":
            self.head.setx(x + 20)

        self.update_face()  # Update eyes and tongue position

    # -----------------------------
    # UPDATE EYES + TONGUE
    # -----------------------------
    def update_face(self):
        x = self.head.xcor()
        y = self.head.ycor()
        offset = 6  # Distance of eyes from head center

        # Adjust eyes & tongue based on direction
        if self.direction == "up":
            self.left_eye.goto(x - 4, y + offset)
            self.right_eye.goto(x + 4, y + offset)
            self.animate_tongue(x, y + 12)

        elif self.direction == "down":
            self.left_eye.goto(x - 4, y - offset)
            self.right_eye.goto(x + 4, y - offset)
            self.animate_tongue(x, y - 12)

        elif self.direction == "left":
            self.left_eye.goto(x - offset, y + 4)
            self.right_eye.goto(x - offset, y - 4)
            self.animate_tongue(x - 12, y)

        elif self.direction == "right":
            self.left_eye.goto(x + offset, y + 4)
            self.right_eye.goto(x + offset, y - 4)
            self.animate_tongue(x + 12, y)

    # -----------------------------
    # ANIMATED TONGUE
    # -----------------------------
    def animate_tongue(self, tx, ty):
        self.frame += 1  # Increase frame count

        # Blink tongue every few frames
        if self.frame % 10 < 5:
            self.tongue.goto(tx, ty)
        else:
            self.tongue.goto(1000, 1000)  # Hide tongue off-screen

    # -----------------------------
    # GROW SNAKE
    # -----------------------------
    def grow(self):
        segment = turtle.Turtle()
        segment.shape("circle")

        # Create gradient effect
        white_value = max(80, 255 - len(self.segments)*8)
        color = (white_value/255, white_value/255, white_value/255)

        segment.color(color)
        segment.shapesize(1.1)
        segment.penup()

        self.segments.append(segment)

    # -----------------------------
    # RESET SNAKE
    # -----------------------------
    def reset(self):
        for segment in self.segments:
            segment.goto(1000, 1000)  # Hide segments

        self.segments.clear()  # Clear body list
        self.head.goto(0, 0)   # Reset head position
        self.direction = "stop"

    # -----------------------------
    # CHECK SELF COLLISION
    # -----------------------------
    def collision_with_self(self):
        for segment in self.segments:
            if segment.distance(self.head) < 15:
                return True
        return False


# ==========================================================
# FOOD CLASS
# ==========================================================

class Food(turtle.Turtle):
    def __init__(self):
        super().__init__()       # Inherit from Turtle
        self.shape("circle")
        self.color("red")
        self.penup()
        self.speed(0)
        self.refresh()

    def refresh(self):
        x = random.randint(-270, 270)  # Random X
        y = random.randint(-270, 270)  # Random Y

        # Align food to grid
        x = round(x / GRID_SIZE) * GRID_SIZE
        y = round(y / GRID_SIZE) * GRID_SIZE

        self.goto(x, y)


# ==========================================================
# SCOREBOARD CLASS
# ==========================================================

class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = self.load_high_score()

        self.hideturtle()
        self.color("white")
        self.penup()
        self.goto(0, 260)
        self.update_display()

    def load_high_score(self):
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                return int(file.read())
        except:
            return 0

    def save_high_score(self):
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(self.high_score))

    def update_display(self):
        self.clear()
        self.write(
            f"Score: {self.score}   High Score: {self.high_score}",
            align="center",
            font=("Courier", 18, "bold")
        )

    def increase(self):
        self.score += 10

        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

        self.update_display()

    def reset(self):
        self.score = 0
        self.update_display()


# ==========================================================
# GAME CLASS
# ==========================================================

class Game:
    def __init__(self):

        self.screen = turtle.Screen()     # Create window
        self.screen.title("Ultimate Snake Game - Professional Edition")
        self.screen.bgcolor("black")
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.tracer(0)             # Turn off auto updates

        self.draw_border()
        self.draw_grid()

        self.snake = Snake()
        self.food = Food()
        self.scoreboard = Scoreboard()

        self.delay = INITIAL_DELAY
        self.state = "START"

        self.setup_controls()
        self.show_start_screen()

        self.run_game()

    # Draw border
    def draw_border(self):
        border = turtle.Turtle()
        border.hideturtle()
        border.color("cyan")
        border.pensize(4)
        border.penup()
        border.goto(-290, -290)
        border.pendown()

        for _ in range(4):
            border.forward(580)
            border.left(90)

    # Draw grid background
    def draw_grid(self):
        grid = turtle.Turtle()
        grid.hideturtle()
        grid.color("#111111")
        grid.speed(0)

        for x in range(-280, 300, GRID_SIZE):
            grid.penup()
            grid.goto(x, -280)
            grid.pendown()
            grid.goto(x, 280)

        for y in range(-280, 300, GRID_SIZE):
            grid.penup()
            grid.goto(-280, y)
            grid.pendown()
            grid.goto(280, y)

    # Show start screen text
    def show_start_screen(self):
        self.message = turtle.Turtle()
        self.message.hideturtle()
        self.message.color("cyan")
        self.message.penup()
        self.message.goto(0, 0)
        self.message.write("PRESS SPACE TO START",
                           align="center",
                           font=("Courier", 24, "bold"))

    # Show game over text
    def show_game_over(self):
        self.message.clear()
        self.message.color("red")
        self.message.goto(0, 20)
        self.message.write("GAME OVER",
                           align="center",
                           font=("Courier", 32, "bold"))
        self.message.goto(0, -30)
        self.message.write("Press R to Restart",
                           align="center",
                           font=("Courier", 18, "bold"))

    # Setup keyboard controls
    def setup_controls(self):
        self.screen.listen()
        self.screen.onkeypress(lambda: self.set_direction("up"), "Up")
        self.screen.onkeypress(lambda: self.set_direction("down"), "Down")
        self.screen.onkeypress(lambda: self.set_direction("left"), "Left")
        self.screen.onkeypress(lambda: self.set_direction("right"), "Right")
        self.screen.onkeypress(self.start_game, "space")
        self.screen.onkeypress(self.restart_game, "r")

    # Change direction
    def set_direction(self, direction):
        opposite = {"up": "down", "down": "up",
                    "left": "right", "right": "left"}

        if self.snake.direction != opposite.get(direction):
            self.snake.direction = direction

    # Start game
    def start_game(self):
        if self.state == "START":
            self.message.clear()
            self.state = "PLAYING"

    # Restart game
    def restart_game(self):
        if self.state == "GAME_OVER":
            self.snake.reset()
            self.scoreboard.reset()
            self.delay = INITIAL_DELAY
            self.message.clear()
            self.state = "PLAYING"

    # Check wall collision
    def check_wall_collision(self):
        x = self.snake.head.xcor()
        y = self.snake.head.ycor()
        return abs(x) > 280 or abs(y) > 280

    # Main game loop
    def run_game(self):
        while True:
            self.screen.update()

            if self.state == "PLAYING":
                self.snake.move()

                if self.snake.head.distance(self.food) < 15:
                    self.food.refresh()
                    self.snake.grow()
                    self.scoreboard.increase()
                    self.delay *= 0.97

                if self.check_wall_collision() or self.snake.collision_with_self():
                    self.state = "GAME_OVER"
                    self.show_game_over()

                time.sleep(self.delay)


# Run the game
Game()