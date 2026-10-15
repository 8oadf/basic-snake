# Simple Snake game
# By 8oadf

import random
import turtle

# Screen
wn = turtle.Screen()
wn.title("Snake Game by 8oadf")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)  # Turns off automatic screen updates

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("green")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Apple
apple = turtle.Turtle()
apple.speed(0)
apple.shape("circle")
apple.color("red")
apple.penup()

# Each item in this list is one body segment
segments = []

# Score display
score = 0
high_score = 0
HUD_LEFT = -280
HUD_RIGHT = 280
HUD_BOTTOM = 180
HUD_TOP = 280

hud_border = turtle.Turtle()
hud_border.speed(0)
hud_border.color("white")
hud_border.pensize(3)
hud_border.penup()
hud_border.goto(HUD_LEFT, HUD_BOTTOM)
hud_border.pendown()
hud_border.goto(HUD_RIGHT, HUD_BOTTOM)
hud_border.goto(HUD_RIGHT, HUD_TOP)
hud_border.goto(HUD_LEFT, HUD_TOP)
hud_border.goto(HUD_LEFT, HUD_BOTTOM)
hud_border.hideturtle()

high_score_display = turtle.Turtle()
high_score_display.speed(0)
high_score_display.color("gold")
high_score_display.penup()
high_score_display.hideturtle()
high_score_display.goto(0, 240)

score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 200)


def draw_score():
    score_display.clear()
    high_score_display.clear()
    high_score_display.write(f"High Score: {high_score}", align="center", font=("Arial", 18, "bold"))
    score_display.write(f"Score: {score}", align="center", font=("Arial", 18, "bold"))


def place_apple():
    """Put the apple at a random location on the 20-pixel grid."""
    while True:
        x = random.randrange(-280, 281, 20)
        y = random.randrange(-280, 281, 20)
        inside_hud = HUD_LEFT <= x <= HUD_RIGHT and HUD_BOTTOM <= y <= HUD_TOP
        on_snake = head.distance(x, y) < 1 or any(
            segment.distance(x, y) < 1 for segment in segments
        )
        if not inside_hud and not on_snake:
            apple.goto(x, y)
            return


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


def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)


def reset_game():
    global score

    head.goto(0, 0)
    head.direction = "stop"
    score = 0
    for segment in segments:
        segment.hideturtle()
    segments.clear()
    place_apple()
    draw_score()


def game_loop():
    global score, high_score

    # Save the old positions so each segment follows the one in front of it.
    old_positions = [(head.xcor(), head.ycor())]
    old_positions.extend((segment.xcor(), segment.ycor()) for segment in segments)

    move()

    # Grow by one segment when the head reaches the apple.
    ate_apple = head.distance(apple) < 20
    if ate_apple:
        score += 10
        high_score = max(high_score, score)
        segment = turtle.Turtle()
        segment.speed(0)
        segment.shape("square")
        segment.color("dark green")
        segment.penup()
        segment.goto(old_positions[-1])
        segments.append(segment)
        place_apple()
        draw_score()

    # Move body segments into the positions their leaders just left.
    for index, segment in enumerate(segments):
        segment.goto(old_positions[index])

    # Start a new game if the snake hits a wall, the HUD zone, or itself.
    inside_hud = (
        HUD_LEFT <= head.xcor() <= HUD_RIGHT
        and HUD_BOTTOM <= head.ycor() <= HUD_TOP
    )
    if (abs(head.xcor()) > 280 or abs(head.ycor()) > 280 or
            inside_hud or
            any(head.distance(segment) < 1 for segment in segments)):
        reset_game()

    wn.update()
    wn.ontimer(game_loop, 100)


# Keyboard controls: arrows or W/A/S/D
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

place_apple()
draw_score()
game_loop()
wn.mainloop()