from TetrisGame import TetrisGame

game = TetrisGame(2)
game.updateTetris()

def handleUpdate():
    global game
    if game.updateTetris() == False:
        # 게임 재시작
        print("IN")
        game = TetrisGame(5)
        game.updateTetris()
        handleListener()
    game.screen.ontimer(handleUpdate, 1)

def handleListener():
    game.screen.listen()
    game.screen.onkey(game.moveLeft, "a")
    game.screen.onkey(game.moveRight, "d")
    game.screen.onkey(game.softDrop, "s")
    game.screen.onkey(game.hardDrop, "w")
    game.screen.onkey(game.turnLeft, "j")
    game.screen.onkey(game.turnRight, "l")
    game.screen.onkey(game.hold, "i")
    game.screen.onkey(game.turn180, "k")

handleListener()
handleUpdate()

game.screen.mainloop()