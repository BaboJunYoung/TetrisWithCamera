import curses
from Tetromino import Tetromino
import threading
import time
import random

# air: 0, block: 1
FIELD = [
    [0 for i in range(10)] for ii in range(20)
]

MINOS = ["I", "J", "O", "Z", "T", "S", "L"]
HOLD = ""
SCORE = 0
NEXT = []
BLOCK = Tetromino("J")

def hardDrop():
    pass

def __drawTetromino(screen, y, x, blockType):
    match(blockType): # 기존 그림 덮어지우기
        case "I":
            screen.addstr(y  , x, "         ")
            screen.addstr(y+1, x, " # # # # ")
        case "J":
            screen.addstr(y  , x, "  #      ")
            screen.addstr(y+1, x, "  # # #  ")
        case "O":
            screen.addstr(y  , x, "   # #   ")
            screen.addstr(y+1, x, "   # #   ")
        case "Z":
            screen.addstr(y  , x, "  # #    ")
            screen.addstr(y+1, x, "    # #  ")
        case "T":
            screen.addstr(y  , x, "    #    ")
            screen.addstr(y+1, x, "  # # #  ")
        case "S":
            screen.addstr(y  , x, "    # #  ")
            screen.addstr(y+1, x, "  # #    ")
        case "L":
            screen.addstr(y  , x, "      #  ")
            screen.addstr(y+1, x, "  # # #  ")
        case "":
            screen.addstr(y  , x, "         ")
            screen.addstr(y+1, x, "         ")
        case _: raise ValueError

def __printScreen(screen: curses.initscr):
    #
    #
    #
    screen.addstr(3 , 0, "$                     $ ┏━━━SCORE━━━┓")
    screen.addstr(4 , 0, "$                     $ ┃ 000000000 ┃")
    screen.addstr(5 , 0, "$                     $ ┗━━━━━━━━━━━┛")
    screen.addstr(6 , 0, "$                     $              ")
    screen.addstr(7 , 0, "$                     $  ┏━━NEXT━━━┓ ")
    screen.addstr(8 , 0, "$                     $  ┃         ┃ ")
    screen.addstr(9 , 0, "$                     $  ┃         ┃ ")
    screen.addstr(10, 0, "$                     $  ┣━━━━━━━━━┫ ")
    screen.addstr(11, 0, "$                     $  ┃         ┃ ")
    screen.addstr(12, 0, "$                     $  ┃         ┃ ")
    screen.addstr(13, 0, "$                     $  ┣━━━━━━━━━┫ ")
    screen.addstr(14, 0, "$                     $  ┃         ┃ ")
    screen.addstr(15, 0, "$                     $  ┃         ┃ ")
    screen.addstr(16, 0, "$                     $  ┗━━━━━━━━━┛ ")
    screen.addstr(17, 0, "$                     $              ")
    screen.addstr(18, 0, "$                     $  ┏━━HOLD━━━┓ ")
    screen.addstr(19, 0, "$                     $  ┃         ┃ ")
    screen.addstr(20, 0, "$                     $  ┃         ┃ ")
    screen.addstr(21, 0, "$                     $  ┗━━━━━━━━━┛ ")
    screen.addstr(22, 0, "$                     $              ")
    screen.addstr(23, 0, "$                     $              ")
    screen.addstr(24, 0, "$ $ $ $ $ $ $ $ $ $ $ $              ")
    
    screen.refresh()


def __updateScreen(screen: curses.initscr) -> None:
    while True:
        screen.addstr(4, 26, f"{SCORE:09}")
        for nextIndex in range(len(NEXT)): __drawTetromino(screen, 8 + 3 * nextIndex, 26, NEXT[nextIndex])
        __drawTetromino(screen, 16, 26, HOLD)
        # 테트리스 필드 그리기
        for _ in range(1, 4): screen.addstr(_, 2, " " * 20) # 필드 위쪽 제거
        for row in range(20):
            for pixel in range(10):
                if FIELD[row][pixel] == 0: screen.addstr(4 + row, 1 + 1 + 2 * pixel, "  ")
                else                     : screen.addstr(4 + row, 1 + 1 + 2 * pixel, "# ")

        # 블록 그리기
        blockPosition = BLOCK.getPosition() # 필드 기준 좌표
        blockPosition[0] += 4 # 값 보정
        blockPosition[1] *= 2 # 값 보정
        blockPosition[1] += 2 # 값 보정
        screen.addstr(0, 0, str(blockPosition))
        
        # screen.addstr(0, 0, str(blockPosition))

        blockShape = BLOCK.getShape()
        for i in range(len(blockShape)):
            for ii in range(len(blockShape)):
                if blockShape[i][ii] == "#":
                    screen.addstr(blockPosition[0] + i, blockPosition[1] + ii * 2, "# ")


        screen.refresh()

        time.sleep(0.1)


def __main(screen: curses.initscr) -> None:
    screen.clear()
    __printScreen(screen)

    # Next 3개 지정
    global NEXT
    for _ in range(3): NEXT.append(random.choice(MINOS))

    screenThread = threading.Thread(target=__updateScreen, args=(screen, ))
    screenThread.daemon = True
    screenThread.start()

    while True:
        # screen.addstr(0, 0, str(screen.getkey()))
        pressedKey = str(screen.getkey())
        
        match(pressedKey):
            case "KEY_LEFT": BLOCK.moveLeft()
            case "KEY_RIGHT": BLOCK.moveRight()
            case "KEY_DOWN": BLOCK.softDrop()
            case "a": BLOCK.moveLeft()
            case "d": BLOCK.moveRight()
        # screen.refresh()

"""
screen.getkey()
화살표
  왼쪽   : KEY_LEFT
  오른쪽 : KEY_RIGHT
  위쪽   : KEY_UP
  아래쪽 : KEY_DOWN
"""

def run():
    curses.wrapper(__main) # curses 모듈을 정성적으로 종료시킴

run()