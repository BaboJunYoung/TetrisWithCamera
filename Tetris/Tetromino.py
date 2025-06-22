class Tetromino():
    # shape: 미노의 모양(IJOZTSL)
    # position: 콘솔에서 블록의 왼쪽위 좌표 리스트(x, y 순)
    def __init__(self, shapeType: str, field: list, position: list = [-3, 3]):
        self.TETROMINO = {
            "I": [
                [" ", " ", " ", " "],
                ["#", "#", "#", "#"],
                [" ", " ", " ", " "],
                [" ", " ", " ", " "]
            ],
            "J": [
                ["#", " ", " "],
                ["#", "#", "#"],
                [" ", " ", " "]
            ],
            "O": [
                ["#", "#"],
                ["#", "#"]
            ],
            "Z": [
                ["#", "#", " "],
                [" ", "#", "#"],
                [" ", " ", " "]
            ],
            "T": [
                [" ", "#", " "],
                ["#", "#", "#"],
                [" ", " ", " "]
            ],
            "S": [
                [" ", "#", "#"],
                ["#", "#", " "],
                [" ", " ", " "]
            ],
            "L": [
                [" ", " ", "#"],
                ["#", "#", "#"],
                [" ", " ", " "]
            ]
        }
        self.shapeType = shapeType
        self.shape = self.TETROMINO[self.shapeType]
        self.position = position
        self.rotatedDegree = 0 # 시계방향으로 돌아간 정도
        self.field = field
        self.isPlaced = False
        
    def __rotateListRight(self, targetList: list) -> list:
        length = len(targetList)
        rotatedList = [[" " for _ in range(length)] for _ in range(length)] # 얕은 복사 조심
        for i in range(length):
            for ii in range(length):
                rotatedList[i][ii] = targetList[length - ii - 1][i]
        # print(rotatedShape) # 진짜 울고싶엇다ㅜ
        return rotatedList
    def __rotateListLeft(self, targetList: list) -> list:
        length = len(targetList)
        rotatedList = [[" " for _ in range(length)] for _ in range(length)]
        for i in range(length):
            for ii in range(length) :
                rotatedList[i][ii] = targetList[ii][length - i - 1]
        return rotatedList

    def rotateRight(self) -> bool: 
        self.shape = self.__rotateListRight(self.shape)
        if (self.isOut()): 
            self.shape = self.__rotateListLeft(self.shape)
            return False
        return True
    def rotateLeft(self) -> bool : 
        self.shape = self.__rotateListLeft(self.shape)
        if (self.isOut()):
            self.shape = self.__rotateListRight(self.shape)
            return False
        return True

    def __printShape(self) -> None:
        for row in self.shape:
            for char in row:
                print(char, end="")
            print()

    def getShapeType(self) -> str: return str(self.shapeType)
    def getShape(self) -> list: return self.shape

    def getPosition(self) -> list: return list(self.position)


    def moveRight(self) -> bool:
        self.position[1] += 1
        if (self.isOut()):
            self.position[1] -= 1
            return False
        return True

    def moveLeft(self) -> bool:
        self.position[1] -= 1
        if (self.isOut()):
            self.position[1] += 1
            return False
        return True

    def isOut(self) -> bool:
        standardPosition = self.getPosition()
        for i in range(len(self.shape)):
            for ii in range(len(self.shape)):
                if (self.shape[i][ii] == " "): continue
                if (standardPosition[0] + i >= 20): return True
                elif (standardPosition[1] + ii < 0 or standardPosition[1] + ii >= 10): return True
                if (standardPosition[0] + i >= 0): 
                    if (self.field[standardPosition[0] + i][standardPosition[1] + ii] == 1): return True
        return False

    def setBlock(self):
        standardPosition = self.getPosition()
        for i in range(len(self.shape)):
            for ii in range(len(self.shape)):
                if (self.shape[i][ii] == "#"):
                    self.field[standardPosition[0] + i][standardPosition[1] + ii] = 1
        self.isPlaced = True

    def getIsPlaced(self) -> bool:
        return self.isPlaced

    # 성공: True, 멈춤: False
    def softDrop(self) -> bool: 
        self.position[0] += 1
        if self.isOut(): 
            self.position[0] -= 1
            return False
        return True
    
    def hardDrop(self) -> None:
        while (self.softDrop()):pass
        self.setBlock()