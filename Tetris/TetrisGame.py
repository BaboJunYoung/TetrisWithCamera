# 기한: 9월 26일 전까지

import Tetromino
import turtle

BLOCK_SIZE = 50

screen = turtle.Screen()
screen.title("Tetris with camera")
screen.setup(width=BLOCK_SIZE*27, height=BLOCK_SIZE*23)
t = turtle.Turtle(shape="turtle")
t.speed(10)
t.penup()


def run():
    print("IN RUN")
    __drawMap()

# DRAWING FUNCTIONS
def __drawMap():
    # 큰 네모
    t.goto(BLOCK_SIZE * -13, BLOCK_SIZE * 11)
    __drawBox(26, 22, "#000000")

    # 모서리 다듬기
    ## 왼쪽 아래
    t.goto(BLOCK_SIZE * -13, BLOCK_SIZE * 5)
    __drawBox(7, 16, "#ffffff")

    ## 오른쪽 아래
    t.goto(BLOCK_SIZE * 6, BLOCK_SIZE * -7)
    __drawBox(8, 5, "#ffffff")

    # 작은 네모 (HOLD)
    t.goto(BLOCK_SIZE * -12, BLOCK_SIZE * 10)
    __drawBox(6, 4, "#ffffff")

    # 작은 네모 (FIELD)
    t.goto(BLOCK_SIZE * -5, BLOCK_SIZE * 10)
    __drawBox(10, 20, "#ffffff")

    # 작은 네모 (NEXT)
    t.goto(BLOCK_SIZE * 6, BLOCK_SIZE * 10)
    __drawBox(6, 16, "#ffffff")

    # # END
    __goAway()

def __drawBox(width: int, height: int, color: str = "#000000"):
    t.setheading(0)

    t.color(color)
    t.fillcolor(color)
    t.pendown()
    t.begin_fill()

    t.forward(BLOCK_SIZE * width)
    t.right(90)
    t.forward(BLOCK_SIZE * height)
    t.right(90)
    t.forward(BLOCK_SIZE * width)
    t.right(90)
    t.forward(BLOCK_SIZE * height)
    t.end_fill()

    t.penup()

def __drawBlock(color: str = "#000000"):
    t.setheading(0)
    t.color(color)
    t.begin_fill()
    t.fillcolor(color)
    t.pendown()
    for _ in range(4):
        t.forward(BLOCK_SIZE)
        t.right(90)
    t.end_fill()
    t.penup()

def __goAway():
    t.goto(BLOCK_SIZE * -13, BLOCK_SIZE * 11)
    t.setheading(0)

screen.exitonclick()