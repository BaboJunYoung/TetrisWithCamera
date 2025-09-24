from Tetromino import Tetromino
import turtle, random, copy

class TetrisGame():
    def __init__(self, fallingTimeScale: float = 1) -> None:
        self.BLOCK_SIZE = 35
        self.MINO_TYPES = list("ZSOTJLI")

        self.FALLING_TIME = 1000 / fallingTimeScale
        self.SETTING_TIME = 2


        self.nextMinos: list[Tetromino] = []
        self.bagOfNext: list[Tetromino] = []
        self.holdingMino: Tetromino = None
        self.fallingMino: Tetromino = None


        self.field: list[list[int | str]] = [
            [0 for _ in range(10)] for _ in range(20)
        ] # 빈칸: 0 / 블록: hex코드 색상

        self.previousFallingMinoField: list[list[int | str]] = [
            [0 for _ in range(10)] for _ in range(20)
        ]

        self.screen = turtle.Screen()
        self.screen.title("Tetris with Camera")
        self.screen.setup(
            width=self.BLOCK_SIZE * 27,
            height=self.BLOCK_SIZE * 23
        )
        self.screen.tracer(0)
        self.turtle = turtle.Turtle(shape="turtle", visible=False)
        self.turtle.speed(0)
        self.turtle.penup()

        self.isHolded = False
        self.isRun = True
        self.tick = 0
        self.settingBlockTimer = 0
        #################################################
        self.__fillNext()
        self.__setFallingMino()
        self.__drawMap()
        self.__drawNext()

        self.screen.update()
    
    # Run Tetris
    def run(self, time: int = 10):
        self.updateTetris()
        self.screen.ontimer(self.run, time)

    # Update Screen and Game Status
    ## True: tetris is running
    ## False: tetris is not running
    def updateTetris(self) -> bool:
        if self.isRun != True: return False

        self.tick += 1

        if self.tick % self.FALLING_TIME == 0:
            fallingResult = self.fallingMino.softDrop()

            if fallingResult == False: # 블럭 자동설치
                self.settingBlockTimer += 1
                if self.settingBlockTimer >= self.SETTING_TIME: self.__setMinoBlock()

        self.__removeLine()
        self.__drawField()
        self.screen.update()
        return True

###################################################################
    # Control Functions
    
    # True: Succeed moving
    # False: Fail moving
    def moveLeft(self) -> bool:
        return self.fallingMino.moveLeft()
    def moveRight(self) -> bool:
        return self.fallingMino.moveRight()
    
    def turnLeft(self) -> bool:
        return self.fallingMino.turnLeft()
    def turnRight(self) -> bool:
        return self.fallingMino.turnRight()
    def turn180(self) -> bool:
        return self.fallingMino.turn180()

    # True: Succeed drop
    # False: Fail drop
    def softDrop(self) -> bool:
        return self.fallingMino.softDrop()
    def hardDrop(self) -> None:
        self.fallingMino.hardDrop()
        self.__setMinoBlock()
    def hold(self) -> None:
        if self.isHolded: return -1

        if self.holdingMino == None: # 홀드에 암것도 업슴
            self.holdingMino = self.fallingMino
            self.__setFallingMino()
            self.__drawNext()
        else: # 홀드에 먼가 잇슴
            holdingMino = self.holdingMino
            self.holdingMino = self.fallingMino
            self.fallingMino = Tetromino(holdingMino.getType(), self.field)
        self.isHolded = True
        self.__drawHold()


#################################################################
    # System Function

    def __setMinoBlock(self):
        self.field = self.fallingMino.getFallingMinoField()
        self.__setFallingMino()
        self.__drawNext()
        self.settingBlockTimer = 0
        self.isHolded = False

    def __moveForward(self, distance: int = 1):
        self.turtle.forward(self.BLOCK_SIZE * distance)
    def __moveBackward(self, distance: int = 1):
        self.turtle.back(self.BLOCK_SIZE * distance)

    def __turnRight(self, angle: int = 90):
        self.turtle.right(angle)
    def __turnLeft(self, angle: int = 90):
        self.turtle.left(angle)

    def __moveTurtleTo(self, posX: int, posY: int) -> None:
        self.turtle.goto(self.BLOCK_SIZE * posX, self.BLOCK_SIZE * posY)

    def __printList(self, list: list) -> None:
        for item in list: print(item)
        print("----------------------------")
    
    # 꽉 찬 줄 지우기
    def __removeLine(self):
        for column in range(20):
            isFilled = True
            for row in range(10):
                if self.field[column][row] == 0:
                    isFilled = False
                    break
            if isFilled:
                del self.field[column] # 꽉 찬 줄 제거
                self.field.insert(0, [0 for _ in range(10)]) # 맨 위에 새로운 줄 추가
    
    def __endGame(self):
        self.isRun = False

    def __setFallingMino(self):
        self.fallingMino = Tetromino(self.nextMinos.pop(0).getType(), self.field)
        self.__fillNext()

        if self.fallingMino.isCrash(): # 소환했는데 충돌이 남. -> 위까지 넘침
            self.__endGame()
    
    def __fillBag(self):
        for minoType in self.MINO_TYPES:
            mino = Tetromino(minoType)
            self.bagOfNext.append(mino)
        random.shuffle(self.bagOfNext)
    
    def __fillNext(self):
        for _ in range(5 - len(self.nextMinos)):
            if len(self.bagOfNext) == 0: self.__fillBag()
            self.nextMinos.append(self.bagOfNext.pop())
    

#################################################################
    # Drawing Functions

    def __hide(self):
        self.__moveTurtleTo(0, 12)
        self.turtle.color("#ffffff")
    
    def __drawHold(self):
        self.__moveTurtleTo(-12, 10)
        self.__drawBox(6, 4)
        self.__moveTurtleTo(-11, 9)
        self.__drawMino(self.holdingMino)

    def __drawField(self):
        if self.fallingMino == None: return False

        fallingMinoField = self.fallingMino.getFallingMinoField()

        for column in range(20):
            for row in range(10):
                fallingFieldColor = fallingMinoField[column][row]
                previousFieldColor = self.previousFallingMinoField[column][row]

                if fallingFieldColor != previousFieldColor:
                    self.__moveTurtleTo(row - 5, 10 - column)
                    self.__drawBlock(fallingFieldColor)
        self.previousFallingMinoField = fallingMinoField
        self.__hide()
    
    def __drawNext(self):
        self.__moveTurtleTo(6, 10)
        self.__drawBox(6, 16)

        for nextMinoIndex in range(len(self.nextMinos)):
            self.__moveTurtleTo(7, 9 - 3*nextMinoIndex)
            self.__drawMino(self.nextMinos[nextMinoIndex])

    def __drawMino(self, mino: Tetromino):
        minoType = mino.getType()
        color = mino.getColorOfMino()
        
        match (minoType):
            case "Z":
                self.__drawBox(2, 1, color)
                self.__moveForward()
                self.__turnRight()
                self.__moveForward()
                self.__drawBox(2, 1, color)
            case "S":
                self.__moveForward()
                self.__drawBox(2, 1, color)
                self.__moveBackward()
                self.__turnRight()
                self.__moveForward()
                self.__drawBox(2, 1, color)
            case "O":
                self.__moveForward()
                self.__drawBox(2, 2, color)
            case "T":
                self.__moveForward()
                self.__drawBox(1, 1, color)
                self.__moveBackward()
                self.__turnRight()
                self.__moveForward()
                self.__drawBox(3, 1, color)
            case "J":
                self.__drawBox(3, 2, color)
                self.__moveForward()
                self.__drawBox(2, 1)
            case "L":
                self.__drawBox(3, 2, color)
                self.__drawBox(2, 1)
            case "I":
                self.__turnRight()
                self.__moveForward()
                self.__drawBox(4, 1, color)
    
    def __drawMap(self):
        # 전체 큰 네모
        self.__moveTurtleTo(-13, 11)
        self.__drawBox(26, 22, "#000000")


        ## 모서리 다듬기
        
        # 왼쪽 아래
        self.__moveTurtleTo(-13, 5)
        self.__drawBox(7, 16)

        # 오른쪽 아래
        self.__moveTurtleTo(6, -7)
        self.__drawBox(7, 4)

        # 홀드
        self.__moveTurtleTo(-12, 10)
        self.__drawBox(6, 4)

        # 필드
        self.__moveTurtleTo(-5, 10)
        self.__drawBox(10, 20)

    def __drawBox(self, width: int, height: int, color: str = "#ffffff"):
        self.turtle.setheading(0)

        self.turtle.color(color)
        self.turtle.fillcolor(color)
        self.turtle.pendown()
        self.turtle.begin_fill()

        for _ in range(2):
            self.__moveForward(width)
            self.__turnRight()
            self.__moveForward(height)
            self.__turnRight()
        
        self.turtle.end_fill()
        self.turtle.penup()

        # self.screen.update()
    
    def __drawBlock(self, color: str = "#ffffff"):
        if color == 0: color = "#ffffff"

        self.turtle.setheading(0)
        self.turtle.color(color)
        self.turtle.begin_fill()
        self.turtle.fillcolor(color)
        self.turtle.pendown()

        for _ in range(2):
            self.__moveForward()
            self.__turnRight()         
            self.turtle.forward(self.BLOCK_SIZE - 1)
            self.__turnRight()
        self.turtle.end_fill()
        self.turtle.penup()

        self.screen.update()