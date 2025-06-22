import curses
from Tetris.Tetromino import Tetromino
import threading
import time
import random



# air: 0, block: 1
__FIELD = [
    [0 for i in range(10)] for ii in range(20)
]
__MINOS = ["I", "J", "O", "Z", "T", "S", "L"]
__AppearedMinos = []
__HOLD = ""
__SCORE = 0
__NEXT = []
__BLOCK = Tetromino("J", __FIELD)
__isPlaying = True
__isHolded = False


# NEXT에 블록 랜덤으로 추가
def __addNext():
    global __NEXT, __AppearedMinos
    mino = ""
    if len(__AppearedMinos) == 7: __AppearedMinos = []
    while True:
        mino = random.choice(__MINOS)
        if mino not in __AppearedMinos:
            __NEXT.append(random.choice(__MINOS))
            break


# 화면 그리기
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
        case "": pass
        case _:
            screen.addstr(y  , x, "         ")
            screen.addstr(y+1, x, "         ")

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



# controller 함수들
def moveRight(): __BLOCK.moveRight()
def moveLeft(): __BLOCK.moveLeft()
def rotateRight(): __BLOCK.rotateRight()
def rotateLeft(): __BLOCK.rotateLeft()
def softDrop(): 
    global __SCORE
    if (__BLOCK.softDrop()): __SCORE += 1
def hardDrop():
    global __SCORE, __isPlaying
    __SCORE += 2 * __BLOCK.hardDrop()
    if __BLOCK.getPosition()[0] < -1: __isPlaying = False
def hold(): 
    global __HOLD, __BLOCK, __isHolded
    
    if __isHolded: return -1

    if __HOLD == "":
        __HOLD = __BLOCK.getShapeType()
        __BLOCK = Tetromino(__NEXT.pop(0), __FIELD)
        __addNext()
    else:
        shapeType = __BLOCK.getShapeType()
        __BLOCK = Tetromino(__HOLD, __FIELD)
        __HOLD = shapeType
    __isHolded = True





# Thread 모음
def __updateScreen(screen: curses.initscr) -> None:
    global __BLOCK
    while __isPlaying:
        screen.addstr(4, 26, f"{__SCORE:09}")
        for nextIndex in range(len(__NEXT)): __drawTetromino(screen, 8 + 3 * nextIndex, 26, __NEXT[nextIndex])
        __drawTetromino(screen, 19, 26, __HOLD)

        # 테트리스 필드 그리기
        for _ in range(1, 4): screen.addstr(_, 2, " " * 20) # 필드 위쪽 제거
        for row in range(20):
            for pixel in range(10):
                if __FIELD[row][pixel] == 0: screen.addstr(4 + row, 1 + 1 + 2 * pixel, "  ")
                else                     : screen.addstr(4 + row, 1 + 1 + 2 * pixel, "# ")


        # 하드드롭 -> 블록 순으로 그리기
        # 하드드롭보다 블록이 보여야되니깐....

        # 하드드롭 위치 그리기
        hardDropPosition = __BLOCK.getHardDropPosition() # 필드 기준 좌표
        hardDropPosition[0] += 4
        hardDropPosition[1] *= 2
        hardDropPosition[1] += 2
        blockShape = __BLOCK.getShape()
        for i in range(len(blockShape)):
            for ii in range(len(blockShape)):
                if blockShape[i][ii] == "#":
                    screen.addstr(hardDropPosition[0] + i, hardDropPosition[1] + ii * 2, ". ")
        
        # 블록 그리기
        blockPosition = __BLOCK.getPosition() # 필드 기준 좌표
        blockPosition[0] += 4 # 값 보정 (필드 -> 콘솔)
        blockPosition[1] *= 2 # 값 보정 (필드 -> 콘솔)
        blockPosition[1] += 2 # 값 보정 (필드 -> 콘솔)
        # screen.addstr(0, 0, str(blockShape))
        for i in range(len(blockShape)):
            for ii in range(len(blockShape)):
                if blockShape[i][ii] == "#":
                    screen.addstr(blockPosition[0] + i, blockPosition[1] + ii * 2, "0 ")
        
        screen.refresh()
        time.sleep(0.1)

def __updateEventSecondly(screen: curses.initscr) -> None:
    isGroundCount = 0
    while __isPlaying:
        __BLOCK.softDrop()
        if (__BLOCK.isGround() == True):
            isGroundCount += 1
        if (isGroundCount >= 2):
            # screen.addstr(0, 0, f"{isGroundCount}, {__BLOCK.isGround()}")
            isGroundCount = 0
            hardDrop() # 자동으로 설치되는거랑 내가 하드드롭하는거 둘 다에게 적용
        time.sleep(1)

def __updateEvent(screen: curses.initscr) -> None:
    while __isPlaying:
        global __SCORE, __isHolded, __BLOCK

        removedRow = 0
        for rowIndex in range(len(__FIELD) - 1, -1, -1):
            if __FIELD[rowIndex] == [1 for _ in range(10)]:
                del __FIELD[rowIndex]
                removedRow += 1
        for _ in range(removedRow): __FIELD.insert(0, [0 for _ in range(10)])
        if (removedRow > 0): 
            __SCORE += 100 + 200 * removedRow
            if removedRow == 4: __SCORE += 100

    
        if (__BLOCK.getIsPlaced()):
            __BLOCK = Tetromino(__NEXT.pop(0), __FIELD)
            __addNext()
            __isHolded = False

    # END SCREEN
    timer = 10
    while timer >= 0:
        screen.addstr(0, 0, f"GAME OVER!!! ({timer} sec) ")
        screen.refresh()
        time.sleep(1)
        timer -= 1
    curses.endwin()

# 실행파트
def __main(screen: curses.initscr) -> None:
    screen.clear()
    curses.curs_set(0)
    __printScreen(screen)

    # Next 3개 지정
    global __NEXT, __BLOCK
    for _ in range(3): __addNext()

    screenThread = threading.Thread(target=__updateScreen, args=(screen, ))
    # screenThread.daemon = True
    screenThread.start()

    secondlyEventThread = threading.Thread(target=__updateEventSecondly, args=(screen, ))
    # secondlyEventThread.daemon = True
    secondlyEventThread.start()
    
    eventThread = threading.Thread(target=__updateEvent, args=(screen, ))
    # eventThread.daemon = True
    eventThread.start()
    

"""
결국엔 이건 안쓰네...

screen.getkey()
화살표
  왼쪽   : KEY_LEFT
  오른쪽 : KEY_RIGHT
  위쪽   : KEY_UP
  아래쪽 : KEY_DOWN
"""

def run(): curses.wrapper(__main) # curses 모듈을 정상적으로 종료시킴