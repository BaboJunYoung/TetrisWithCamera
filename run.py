import Tetris.TetrisGame as TetrisGame
import keyboard as key

TetrisGame.run()

# 키 이름 → 함수 매핑
key_actions = {
    "w": TetrisGame.hardDrop,
    "a": TetrisGame.moveLeft,
    "s": TetrisGame.softDrop,
    "d": TetrisGame.moveRight,
    "j": TetrisGame.rotateLeft,
    "l": TetrisGame.rotateRight,
    "i": TetrisGame.hold,
}

def control(event):
    if event.event_type != "down":
        return
    action = key_actions.get(event.name)
    if action:
        action()

# 훅 등록
key.hook(control)