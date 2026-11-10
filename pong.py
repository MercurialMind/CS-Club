import random
import turtle

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_INCREMENT = 10
BALL_SPEED = 5

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_RADIUS = 10

class Scoreboard:
    def __init__(self):
        self.score_left = 0
        self.score_right = 0
        self.writer = turtle.Turtle()
        self.writer.hideturtle()
        self.writer.penup()
        self.writer.color("black")
        self.update_display()

    def update_display(self):
        self.writer.clear()
        self.writer.goto(0, 240)
        text = f"Score: {self.score_left}                 Score: {self.score_right}"
        self.writer.write(text, align="center", font=("Arial", 16, "bold"))

    def point_left(self):
        self.score_left += 1
        self.update_display()

    def point_right(self):
        self.score_right += 1
        self.update_display()

class Paddle:
    def __init__(self, start_x, start_y):
        self.body = turtle.Turtle()
        self.body.penup()
        self.body.shape("square")
        self.body.shapesize(stretch_wid=5, stretch_len=1)
        self.body.color("black")
        self.body.goto(start_x, start_y)
        self.speed = 0

    def move_up(self):
        self.speed = 1

    def move_down(self):
        self.speed = -1

    def stop_up(self):
        if self.speed == 1:
            self.speed = 0

    def stop_down(self):
        if self.speed == -1:
            self.speed = 0

    def update(self):
        new_y = self.body.ycor() + (self.speed * PADDLE_INCREMENT)
        new_y = max(-240, min(new_y, 240))
        self.body.sety(new_y)

class Ball:
    def __init__(self):
        self.body = turtle.Turtle()
        self.body.shape("circle")
        self.body.penup()
        self.body.color("blue")
        self.dx = 0
        self.dy = 0
        self.is_paused = False
        self.reset_ball()

    def reset_ball(self):
        self.body.goto(0, 0)
        self.dx = 0
        self.dy = 0
        self.is_paused = True
        turtle.Screen().ontimer(self.serve, 1000)

    def serve(self):
        self.dx = BALL_SPEED * random.choice([-1, 1])
        self.dy = BALL_SPEED * random.choice([-1, 1])
        self.is_paused = False

    def move(self):
        if self.is_paused:
            return

        self.body.setx(self.body.xcor() + self.dx)
        self.body.sety(self.body.ycor() + self.dy)

        if abs(self.body.ycor()) >= 285:
            self.dy *= -1
            sign = 1 if self.body.ycor() > 0 else -1
            self.body.sety(285 * sign)

screen = turtle.Screen()
screen.title("Pong")
screen.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
screen.tracer(0)

left_paddle = Paddle(-370, 0)
right_paddle = Paddle(370, 0)
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkeypress(right_paddle.move_up, "Up")
screen.onkeyrelease(right_paddle.stop_up, "Up")
screen.onkeypress(right_paddle.move_down, "Down")
screen.onkeyrelease(right_paddle.stop_down, "Down")

screen.onkeypress(left_paddle.move_up, "w")
screen.onkeyrelease(left_paddle.stop_up, "w")
screen.onkeypress(left_paddle.move_down, "s")
screen.onkeyrelease(left_paddle.stop_down, "s")

def check_paddle_collision(paddle, is_left_side):
    px, py = paddle.body.xcor(), paddle.body.ycor()
    bx, by = ball.body.xcor(), ball.body.ycor()

    paddle_half_h = PADDLE_HEIGHT / 2
    paddle_half_w = PADDLE_WIDTH / 2

    within_y_range = (py - paddle_half_h) <= by <= (py + paddle_half_h)

    if is_left_side:
        within_x_range = (px - paddle_half_w) <= (bx - BALL_RADIUS) <= (px + paddle_half_w)
        if within_x_range and within_y_range and ball.dx < 0:
            ball.body.setx(px + paddle_half_w + BALL_RADIUS)
            ball.dx *= -1
            offset = (by - py) / paddle_half_h
            ball.dy += offset * 2
    else:
        within_x_range = (px - paddle_half_w) <= (bx + BALL_RADIUS) <= (px + paddle_half_w)
        if within_x_range and within_y_range and ball.dx > 0:
            ball.body.setx(px - paddle_half_w - BALL_RADIUS)
            ball.dx *= -1
            offset = (by - py) / paddle_half_h
            ball.dy += offset * 2

def check_collisions():
    if ball.is_paused:
        return

    check_paddle_collision(left_paddle, is_left_side=True)
    check_paddle_collision(right_paddle, is_left_side=False)

    if ball.body.xcor() > 390:
        scoreboard.point_left()
        ball.reset_ball()

    elif ball.body.xcor() < -390:
        scoreboard.point_right()
        ball.reset_ball()

def game_loop():
    left_paddle.update()
    right_paddle.update()
    ball.move()
    check_collisions()

    screen.update()
    screen.ontimer(game_loop, 32)  # ~60 FPS

game_loop()
turtle.done()
