
def turnRight(array) -> None:
    result = [[0 for _ in range(len(array))] for _ in range(len(array))]
    beforeShape = array
    maxIndex = len(array) - 1
    for columnIndex in range(len(array)):
        for rowIndex in range(len(array[0])):
            result[rowIndex][maxIndex - columnIndex] = beforeShape[columnIndex][rowIndex]
    
    return result


def turnLeft(array) -> None:
    result = [[0 for _ in range(len(array))] for _ in range(len(array))]
    beforeShape = array
    maxIndex = len(array) - 1
    for columnIndex in range(len(array)):
        for rowIndex in range(len(array)):
            result[maxIndex - rowIndex][columnIndex] = beforeShape[columnIndex][rowIndex]
    return result


def printArray(array):
    for arr in array: print(arr)

a = [[1, 2, 3], [4, 5, 6], [7 ,8, 9]]
printArray(a)
print()
printArray(turnRight(a))
print()
printArray(turnLeft(a))