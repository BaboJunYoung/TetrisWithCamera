class Tetromino():
    def __init__(self, TYPE: str, position: list[int] = [0, 0]):
        if TYPE not in "ZSOTJLI": raise Exception(f"{TYPE} is not tetromino name.")
        self.TYPE = TYPE
        self.position = [0, 0]
    
    def getPosition(self):
        return self.position
    

    def __getColorOfMino(self):
        match (self.TYPE):
            case "Z": return "#FF0000"
            case "S": return "#00FF00"
            case "O": return "#FFFF00"
            case "T": return "#FF00FF"
            case "J": return "#0000FF"
            case "L": return "#FF8000"
            case "I": return "#0080FF"
    def __getGhostColorOfMino(self):
        match (self.TYPE):
            case "Z": return "#FFC0C0"
            case "S": return "#C0FFC0"
            case "O": return "#FFFFC0"
            case "T": return "#FFC0FF"
            case "J": return "#C0C0FF"
            case "L": return "#FFDFC0"
            case "I": return "#C0E0FF"