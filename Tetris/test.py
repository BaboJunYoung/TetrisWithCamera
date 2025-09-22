import turtle

screen = turtle.Screen()
screen.title("Turtle Car")
screen.tracer(0)

t = turtle.Turtle("turtle")
t.penup()
t.speed(0)

ANGLE = 5 * 0.5
SPEED = 5 * 0.5
isPenUp = True

leftTurn = False
rightTurn = False
forwardGo = False
backwardGo = False

def leftOn():
    global leftTurn, rightTurn
    leftTurn = True
    rightTurn = False

def leftOff():
    global leftTurn
    leftTurn = False

def rightOn():
    global leftTurn, rightTurn
    leftTurn = False
    rightTurn = True

def rightOff():
    global rightTurn
    rightTurn = False

def goOn():
    global forwardGo, backwardGo
    forwardGo = True
    backwardGo = False

def goOff():
    global forwardGo
    forwardGo = False

def backOn():
    global forwardGo, backwardGo
    forwardGo = False
    backwardGo = True

def backOff():
    global backwardGo
    backwardGo = False

def penUpDown():
    global isPenUp
    if isPenUp:
        t.pendown()
    else:
        t.penup()
    isPenUp = not isPenUp

screen.listen()

screen.onkeypress(leftOn, "a")
screen.onkeyrelease(leftOff, "a")
screen.onkeypress(rightOn, "d")
screen.onkeyrelease(rightOff, "d")
screen.onkeypress(goOn, "w")
screen.onkeyrelease(goOff, "w")
screen.onkeypress(backOn, "s")
screen.onkeyrelease(backOff, "s")
screen.onkeypress(penUpDown, "space")

def update_screen():
    if forwardGo:
        t.forward(SPEED)
    elif backwardGo:
        t.back(SPEED)
    if leftTurn:
        t.left(ANGLE)
    elif rightTurn:
        t.right(ANGLE)
    screen.update()
    screen.ontimer(update_screen, 10)

update_screen()

screen.mainloop()