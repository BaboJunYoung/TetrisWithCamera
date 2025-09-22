import TetrisGame
# import turtle
# import threading

game = TetrisGame
game.run()

def moveLeft(): game.moveLeft()
def turnLeft(): game.turnLeft()
def moveRight(): game.moveRight()
def turnRight(): game.turnRight()

def turn180(): game.turn180()

def hardDrop(): game.hardDrop()
def softDrop(): game.softDrop()
def hold(): game.hold()


game.screen.listen()

game.screen.onkey(moveLeft, "a")
game.screen.onkey(moveRight, "d")
game.screen.onkey(hardDrop, "w")
game.screen.onkey(softDrop, "s")
game.screen.onkey(turnLeft, "j")
game.screen.onkey(turnRight, "l")
game.screen.onkey(hold, "i")
game.screen.onkey(turn180, "k")

def update():
    game.update()
    game.screen.ontimer(update, 10)

update()
game.screen.mainloop()
# game.screen.exitonclick()