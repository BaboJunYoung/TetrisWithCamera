import cv2
import mediapipe as mp
from TetrisGame import Tetromino, TetrisGame
import time
from collections import deque
import math


mp_hands = mp.solutions.hands
hands_module = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)


game = TetrisGame(20)
game.updateTetris()


last_drop_time = time.time()
FALL_INTERVAL = 0.1 
last_gesture_time = 0
GESTURE_COOLDOWN = 0.3  

tip_x_history = deque(maxlen=5)
tip_y_history = deque(maxlen=5)


def get_tip_position(hand_landmarks):
    tip = hand_landmarks.landmark[8]
    return tip.x, tip.y

def is_fist(hand_landmarks):
    wrist = hand_landmarks.landmark[0]
    tips = [4, 8, 12, 16, 20]
    total = sum(math.hypot(hand_landmarks.landmark[tip].x - wrist.x,
                           hand_landmarks.landmark[tip].y - wrist.y) for tip in tips)
    return (total / len(tips)) < 0.1

def detectGesture(frame):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands_module.process(image)
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]

        if is_fist(hand_landmarks):
            return None

        tip_x, tip_y = get_tip_position(hand_landmarks)
        tip_x_history.append(tip_x)
        tip_y_history.append(tip_y)

        avg_x = sum(tip_x_history) / len(tip_x_history)
        avg_y = sum(tip_y_history) / len(tip_y_history)


        if avg_y < 0.3:
            return "ROTATE"    
        elif avg_y > 0.7:
            return "DOWN"      
        elif avg_x < 0.4:
            return "RIGHT"
        elif avg_x > 0.6:
            return "LEFT"
    return None

def handleGesture():
    global last_gesture_time
    ret, frame = cap.read()
    if not ret:
        return

    current_time = time.time()
    gesture = detectGesture(frame)
    if gesture and (current_time - last_gesture_time) > GESTURE_COOLDOWN:
        if gesture == "LEFT":
            game.moveLeft()
        elif gesture == "RIGHT":
            game.moveRight()
        elif gesture == "DOWN":
            game.hardDrop()
        elif gesture == "ROTATE":
            game.turnRight()
        last_gesture_time = current_time

    game.screen.ontimer(handleGesture, 50)

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

def handleUpdate():
    global last_drop_time, game
    current_time = time.time()

    if current_time - last_drop_time >= FALL_INTERVAL:
        game.fallingMino.softDrop()
        last_drop_time = current_time

    if not game.updateTetris():
        game = TetrisGame(20)
        handleListener()
        handleGesture()

    game.screen.ontimer(handleUpdate, 10)

handleListener()
handleGesture()
handleUpdate()
game.screen.mainloop()

cap.release()
cv2.destroyAllWindows()
