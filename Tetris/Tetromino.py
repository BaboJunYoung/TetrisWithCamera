class Tetromino():
    # shape: 미노의 모양(IJOZTSL)
    # position: 콘솔에서 블록의 왼쪽위 좌표 리스트(x, y 순)
    def __init__(self, shapeType: str, position: list):
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

    def rorateRight(self) -> None: self.shape = self.__rotateListRight(self.shape)
    def rotateLeft(self) -> None : self.shape = self.__rotateListLeft(self.shape)

    def __printShape(self) -> None:
        for row in self.shape:
            for char in row:
                print(char, end="")
            print()
        
    def testRun(self):
        pass
        # print(self.shape)
        # self.__printShape()
        # self.__rorateRight()
        # print(self.shape)
        # self.__printShape()

    def getShapeType(self) -> str: return self.shapeType
    def getShape(self) -> list: return self.shape