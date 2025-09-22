# 기한: 9월 26일 전까지

import Tetromino
import turtle
import random
import time


__BLOCK_SIZE = 50
__HOLD = Tetromino.Tetromino("-", [])
__FALLING = Tetromino.Tetromino("-", [])
__NEXT = []
__BAG = []
__MINOS = list("ZSOTJLI")
__FIELD = [
    [0 for _ in range(10)] for _ in range(20)
]
__BEFORE_FIELD = __FIELD
# TIME = cs : 1/100 초
__FALLING_TIME = 100 / 1
__isRun = True

screen = turtle.Screen()
screen.title("Tetris with camera")
screen.setup(width=__BLOCK_SIZE*27, height=__BLOCK_SIZE*23)
screen.tracer(0) # 이걸로 속도조절
t = turtle.Turtle(shape="turtle")
t.speed(0) # 이걸로 속도조절
t.penup()

__tick = 0
__setBlockCounter = 0

def run():
    global __FIELD

    __drawMap()    
    __addNext()
    __setFallingMino()
    __drawNext()
    screen.update()

def update():
    if not(__isRun): return


    global __tick, __FIELD, __setBlockCounter

    __tick += 1
    # print(__tick)
    if __tick % __FALLING_TIME == 0:
        result = __FALLING.gravityDrop()

        # printList(FALLING.getFallingMinoField())
        if result == False: # 내리기 실패 -> 바닥 닿음
            __setBlockCounter += 1
            if __setBlockCounter == 2:
                __FIELD = __FALLING.getFallingMinoField()
                __setFallingMino()
                __drawNext()
                __setBlockCounter = 0
    
    __removeLine()
    __drawField()
    screen.update()

def __endGame():
    global __isRun, __FALLING, __HOLD, __NEXT, __BAG, __FIELD, __BEFORE_FIELD

    __FALLING = None
    __isRun = False

# CONTROL FUNCTION
def moveLeft(): __FALLING.moveLeft()
def moveRight(): __FALLING.moveRight()
def turnLeft(): __FALLING.turnLeft()
def turnRight(): __FALLING.turnRight()
def turn180(): __FALLING.turn180()
def hardDrop():
    global __FIELD

    __FALLING.hardDrop()
    __FIELD = __FALLING.getFallingMinoField()
    __setFallingMino()
    __drawNext()
def softDrop(): __FALLING.gravityDrop()
def hold():
    global __FALLING, __HOLD
    # 홀드에 암것도 업슴
    if __HOLD.getType() == "-":
        __HOLD = __FALLING
        __setFallingMino()
    # 홀드에 먼가가 잇슴
    else:
        temp = __HOLD
        __HOLD = __FALLING
        __FALLING = Tetromino.Tetromino(temp.getType(), __FIELD)
    __drawHold()



# System Functions
def __printList(lst: list):
    for a in lst: print(a)
    print("-------------")

def __removeLine():
    global __FIELD
    # __printList(__FIELD)
    for column in range(20):
        isFilled = True
        for row in range(10):
            if __FIELD[column][row] == 0:
                isFilled = False
                break
        if isFilled:
            del __FIELD[column]
            __FIELD.insert(0, [0 for _ in range(10)])
        # print(isFilled)

def __setFallingMino():
    global __FALLING

    __FALLING = Tetromino.Tetromino(__NEXT.pop(0).getType(), __FIELD)
    if __FALLING.isCrash(): # 소환 실패 -> 게임 끝!
        
        # print(f"FALLING POSITION : {FALLING.getPosition()}")
        # print(f"FALLING FIELD :")
        # printList(FALLING.getFallingMinoField())

        __endGame()
    __addNext()

def __shuffleBag():
    for minoType in __MINOS:
        mino = Tetromino.Tetromino(minoType, __FIELD)
        __BAG.append(mino)
    random.shuffle(__BAG)

def __addNext():
    for _ in range(5 - len(__NEXT)):
        if len(__BAG) == 0: __shuffleBag()
        __NEXT.append(__BAG.pop())



# DRAWING FUNCTIONS
def __hide():
    t.goto(0, 12 * __BLOCK_SIZE)
    t.color("#ffffff")

def __drawHold():
    t.goto(__BLOCK_SIZE * -12, __BLOCK_SIZE * 10)
    __drawBox(6, 4)
    t.goto(__BLOCK_SIZE * -11, __BLOCK_SIZE * 9)
    __drawMino(__HOLD)

def __drawField():
    global __BEFORE_FIELD
    if type(__FALLING) == type(None): return -1 # Game Over

    field = __FALLING.getFallingMinoField()
    for columnIndex in range(20):
        for rowIndex in range(10):
            color = field[columnIndex][rowIndex]
            beforeColor = __BEFORE_FIELD[columnIndex][rowIndex]

            if color == beforeColor: continue
            elif color != beforeColor:
                t.goto(__BLOCK_SIZE * (-5 + rowIndex), __BLOCK_SIZE * (10 - columnIndex))
                if color == 0: __drawBlock()
                else: __drawBlock(color)
            else:
                t.goto(__BLOCK_SIZE * (-5 + rowIndex), __BLOCK_SIZE * (10 - columnIndex))
                __drawBlock(color)
    __BEFORE_FIELD = field

    __hide()

def __drawNext():
    t.goto(__BLOCK_SIZE * 6, __BLOCK_SIZE * 10)
    __drawBox(6, 16, "#ffffff")

    for nextMinoIndex in range(len(__NEXT)):
        t.goto(__BLOCK_SIZE * 7, __BLOCK_SIZE * (9 - 3 * nextMinoIndex))
        __drawMino(__NEXT[nextMinoIndex])


def __drawMino(mino: Tetromino.Tetromino):
    # ZSOTJLI
    match(mino.getType()):
        case "Z":
            __drawBox(2, 1, mino.getColorOfMino())
            t.forward(__BLOCK_SIZE)
            t.right(90)
            t.forward(__BLOCK_SIZE)
            __drawBox(2, 1, mino.getColorOfMino())
        case "S":
            t.forward(__BLOCK_SIZE)
            __drawBox(2, 1, mino.getColorOfMino())
            t.back(__BLOCK_SIZE)
            t.right(90)
            t.forward(__BLOCK_SIZE)
            __drawBox(2, 1, mino.getColorOfMino())
        case "O":
            t.forward(__BLOCK_SIZE)
            __drawBox(2, 2, mino.getColorOfMino())
        case "T":
            t.forward(__BLOCK_SIZE)
            __drawBlock(mino.getColorOfMino())
            t.back(__BLOCK_SIZE)
            t.right(90)
            t.forward(__BLOCK_SIZE)
            __drawBox(3, 1, mino.getColorOfMino())
        case "J":
            __drawBox(3, 2, mino.getColorOfMino())
            t.forward(__BLOCK_SIZE)
            __drawBox(2, 1)
        case "L":
            __drawBox(3, 2, mino.getColorOfMino())
            __drawBox(2, 1)
        case "I":
            t.right(90)
            t.forward(__BLOCK_SIZE)
            __drawBox(4, 1, mino.getColorOfMino())

def __drawMap():
    # 큰 네모
    t.goto(__BLOCK_SIZE * -13, __BLOCK_SIZE * 11)
    __drawBox(26, 22, "#000000")

    # 모서리 다듬기
    ## 왼쪽 아래
    t.goto(__BLOCK_SIZE * -13, __BLOCK_SIZE * 5)
    __drawBox(7, 16, "#ffffff")

    ## 오른쪽 아래
    t.goto(__BLOCK_SIZE * 6, __BLOCK_SIZE * -7)
    __drawBox(7, 4, "#ffffff")

    # 작은 네모 (HOLD)
    t.goto(__BLOCK_SIZE * -12, __BLOCK_SIZE * 10)
    __drawBox(6, 4, "#ffffff")

    # 작은 네모 (FIELD)
    t.goto(__BLOCK_SIZE * -5, __BLOCK_SIZE * 10)
    __drawBox(10, 20, "#ffffff")

    # # 작은 네모 (NEXT)
    # t.goto(BLOCK_SIZE * 6, BLOCK_SIZE * 10)
    # __drawBox(6, 16, "#ffffff")

    # # END
    # __goAway()

def __drawBox(width: int, height: int, color: str = "#ffffff"):
    t.setheading(0)

    t.color(color)
    t.fillcolor(color)
    t.pendown()
    t.begin_fill()

    t.forward(__BLOCK_SIZE * width)
    t.right(90)
    t.forward(__BLOCK_SIZE * height)
    t.right(90)
    t.forward(__BLOCK_SIZE * width)
    t.right(90)
    t.forward(__BLOCK_SIZE * height)
    t.end_fill()
    
    t.setheading(0)
    t.penup()

def __drawBlock(color: str = "#ffffff"):
    t.setheading(0)
    t.color(color)
    t.begin_fill()
    t.fillcolor(color)
    t.pendown()
    ######################
    t.forward(__BLOCK_SIZE)
    t.right(90)
    
    t.forward(__BLOCK_SIZE - 1)
    t.right(90)
    
    t.forward(__BLOCK_SIZE)
    t.right(90)
    
    t.forward(__BLOCK_SIZE - 1)
    t.right(90)
    ######################
    t.end_fill()
    t.penup()