from TetrisGame import TetrisGame

game = TetrisGame(2)
game.updateTetris()

game.run()

game.screen.listen()
game.screen.onkey(game.moveLeft, "a")
game.screen.onkey(game.moveRight, "d")
game.screen.onkey(game.softDrop, "s")
game.screen.onkey(game.hardDrop, "w")
game.screen.onkey(game.turnLeft, "j")
game.screen.onkey(game.turnRight, "l")
game.screen.onkey(game.hold, "i")
game.screen.onkey(game.turn180, "k")

game.screen.mainloop()