import copy

class Tetromino():
    def __init__(self, type: str, field: list[list[int|str]], position: list[int] = None):
        if type not in "ZSOTJLI-": raise Exception(f"{type} is not tetromino name.")
        self.type = type
        self.position = position if position != None else [-2, 12] if type == "O" else [-2, 11]
        self.shape = self.__getShape()
        self.field = field
        self.length = len(self.shape)

        self.minoTypes = list("ZSOTJLI")
        self.minoColors = ("#FF0000", "#00FF00", "#FFFF00", "#FF00FF", "#0000FF", "#FF8000", "#0080FF")
        self.ghostColors = ("#FFC0C0", "#C0FFC0", "#FFFFC0", "#FFC0FF", "#C0C0FF", "#FFDFC0", "#C0E0FF")
    
    def getPosition(self) -> list[int]: return self.position
    
    def addPosition(self, x: int = 0, y: int = 0) -> None:
        self.position = [self.position[0] + x, self.position[1] + y]
    

    def getType(self) -> str: return self.type


    def getColorOfMino(self) -> str:
        return self.minoColors[self.minoTypes.index(self.getType())]
    
    def getGhostColorOfMino(self) -> str:
        return self.ghostColors[self.minoTypes.index(self.getType())]
    
    def printList(self, lst: list) -> None:
        for i in lst: print(i)
        print("-----------------")

    def getFallingMinoField(self) -> list[list[int|str]]:
        fallingMinoField = copy.deepcopy(self.field)
        ghostPosition = self.__getHardDropPosition()

        # 작동 되니깐 건드리지 말것!!!
        for column in range(self.length):
            for row in range(self.length):

                #####################
                fieldX = self.position[0] + 5 + row
                fieldY = -1 * self.position[1] + 10 + column
                if self.shape[column][row] == 0: continue
                
                ghostX = ghostPosition[0] + 5 + row
                ghostY = -1 * ghostPosition[1] + 10 + column

                fallingMinoField[ghostY][ghostX] = self.getGhostColorOfMino()
                
                if fieldY < 0: continue
                if fieldY >= 20: continue

                fallingMinoField[fieldY][fieldX] = self.getColorOfMino()

                

        return fallingMinoField

    def isCrash(self) -> bool:
        for column in range(self.length):
            for row in range(self.length):
                block = self.shape[column][row] # 블럭 1 0
                if block == 0: continue
                # block은 1임
                blockFieldPosition = [ self.position[0]+row, self.position[1]-column ]

                if blockFieldPosition[0] < -5 or blockFieldPosition[0] > 4: # 좌우로 벗어남
                    return True
                if blockFieldPosition[1] > 10: continue
                if blockFieldPosition[1] <= -10: # 아래로 벗어남
                    return True
            
                fieldX = blockFieldPosition[0] + 5
                fieldY = -1*blockFieldPosition[1] + 10
                if self.field[fieldY][fieldX] != 0: return True
        return False
##############################################################################################
    # CONTROL FUNCTIONS
    def moveLeft(self) -> bool:
        self.position[0] -= 1
        if self.isCrash():
            self.position[0] += 1 # 원상복구
            return False
        else: return True

    def moveRight(self) -> bool:
        self.position[0] += 1
        if self.isCrash():
            self.position[0] -= 1 # 원상복구
            return False
        else: return True
    
    def turnRight(self) -> bool:
        self.__turnArrayRight()
        if self.isCrash():
            self.__turnArrayLeft() # 원상복구
            return False
        else: return True
    def turnLeft(self) -> bool:
        self.__turnArrayLeft()
        if self.isCrash():
            self.__turnArrayRight() # 원상복구
            return False
        else: return True
    def turn180(self) -> bool:
        self.__turnArray180()
        if self.isCrash():
            self.__turnArray180() # 원상복구
            
            
            
            
            
            return False
        else: return True

    def gravityDrop(self) -> bool:
        self.position[1] -= 1
        if self.isCrash(): 
            self.position[1] += 1
            return False
        return True
    
    def hardDrop(self) -> list[int]:
        while not self.isCrash():
            self.position[1] -= 1
        self.position[1] += 1

    def __turnArrayRight(self) -> None:
        beforeShape = self.shape
        maxIndex = len(self.shape) - 1
        for columnIndex in range(len(self.shape)):
            for rowIndex in range(len(self.shape[0])):
                self.shape[rowIndex][maxIndex - columnIndex] = beforeShape[columnIndex][rowIndex]
    def __turnArrayLeft(self) -> None:
        beforeShape = self.shape
        maxIndex = len(self.shape) - 1
        for columnIndex in range(len(self.shape)):
            for rowIndex in range(len(self.shape[0])):
                self.shape[maxIndex - rowIndex][columnIndex] = beforeShape[columnIndex][rowIndex]
    def __turnArray180(self) -> None:
        beforeShape = self.shape
        maxIndex = len(self.shape) - 1
        for columnIndex in range(len(self.shape)):
            for rowIndex in range(len(self.shape[0])):
                self.shape[maxIndex - columnIndex][maxIndex - rowIndex] = beforeShape[columnIndex][rowIndex]
    
##############################################################################################
    # PRIVATE FUNCTIONS    
    def __getHardDropPosition(self) -> list[int]:
        minoPosition = copy.deepcopy(self.position)

        self.hardDrop()
        hardDropPosition = copy.deepcopy(self.position)
        self.position = minoPosition

        return hardDropPosition

    def __getShape(self) -> list[list[int]]:
        lst = []
        match(self.type):
            case "Z": 
                lst.append([1, 1, 0])
                lst.append([0, 1, 1])
                lst.append([0, 0, 0])
            case "S":
                lst.append([0, 1, 1])
                lst.append([1, 1, 0])
                lst.append([0, 0, 0])
            case "O": 
                lst.append([0, 0, 0, 0])
                lst.append([0, 1, 1, 0])
                lst.append([0, 1, 1, 0])
                lst.append([0, 0, 0, 0])
            case "T": 
                lst.append([0, 1, 0])
                lst.append([1, 1, 1])
                lst.append([0, 0, 0])
            case "J": 
                lst.append([1, 0, 0])
                lst.append([1, 1, 1])
                lst.append([0, 0, 0])
            case "L": 
                lst.append([0, 0, 1])
                lst.append([1, 1, 1])
                lst.append([0, 0, 0])
            case "I": 
                lst.append([0, 0, 0, 0])
                lst.append([1, 1, 1, 1])
                lst.append([0, 0, 0, 0])
                lst.append([0, 0, 0, 0])
        return lst