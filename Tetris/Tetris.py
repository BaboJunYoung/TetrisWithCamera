import curses
import Tetromino
import threading
import time
import random

# air: 0, block: 1
FIELD = [
    [0 for i in range(10)] for ii in range(20)
]

HOLD = "I"
SCORE = 0
NEXT = ["J", "O", "S"]
BLOCK = ""
isGameRun = False
MINOS = ["I", "J", "O", "Z", "T", "S", "L"]

def drawTetromino(screen, y, x, blockType):
    match(blockType):
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
        case _: raise ValueError

def printScreen(screen: curses.initscr):
    screen.addstr(0 , 0, "$ $ $ $ $ $ $ $ $ $ $ $ ┏━━━SCORE━━━┓")
    screen.addstr(1 , 0, "$                     $ ┃ 000000000 ┃")
    screen.addstr(2 , 0, "$                     $ ┗━━━━━━━━━━━┛")
    screen.addstr(3 , 0, "$                     $              ")
    screen.addstr(4 , 0, "$                     $  ┏━━NEXT━━━┓ ")
    screen.addstr(5 , 0, "$                     $  ┃         ┃ ")
    screen.addstr(6 , 0, "$                     $  ┃         ┃ ")
    screen.addstr(7 , 0, "$                     $  ┣━━━━━━━━━┫ ")
    screen.addstr(8 , 0, "$                     $  ┃         ┃ ")
    screen.addstr(9 , 0, "$                     $  ┃         ┃ ")
    screen.addstr(10, 0, "$                     $  ┣━━━━━━━━━┫ ")
    screen.addstr(11, 0, "$                     $  ┃         ┃ ")
    screen.addstr(12, 0, "$                     $  ┃         ┃ ")
    screen.addstr(13, 0, "$                     $  ┗━━━━━━━━━┛ ")
    screen.addstr(14, 0, "$                     $              ")
    screen.addstr(15, 0, "$                     $  ┏━━HOLD━━━┓ ")
    screen.addstr(16, 0, "$                     $  ┃         ┃ ")
    screen.addstr(17, 0, "$                     $  ┃         ┃ ")
    screen.addstr(18, 0, "$                     $  ┗━━━━━━━━━┛ ")
    screen.addstr(19, 0, "$                     $              ")
    screen.addstr(20, 0, "$                     $              ")
    screen.addstr(21, 0, "$ $ $ $ $ $ $ $ $ $ $ $              ")
    screen.refresh()


def updateScreen(screen: curses.initscr) -> None:
    while True:
        for nextIndex in range(len(NEXT)): drawTetromino(screen, 5 + 3 * nextIndex, 26, NEXT[nextIndex])
        drawTetromino(screen, 16, 26, HOLD)
        # 테트리스 필드 그리기
        for row in range(20):
            for pixel in range(10):
                if FIELD[row][pixel] == 0: screen.addstr(1 + row, 1 + pixel, "  ")
                else                     : screen.addstr(1 + row, 1 + pixel, "# ")
        screen.refresh()
        time.sleep(1)


def main(screen: curses.initscr) -> None:
    screen.clear()
    printScreen(screen)

    # global HOLD, NEXT
    # HOLD = "I"
    # NEXT = ["Z", "S", "J"]

    screenThread = threading.Thread(target=updateScreen, args=(screen, ))
    screenThread.daemon = True
    screenThread.start()

    screen.getkey()
    

def run():
    global isGameRun
    isGameRun = True
    curses.wrapper(main) # curses 모듈을 정성적으로 종료시킴

run()