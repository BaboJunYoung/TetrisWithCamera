import Tetris.Tetris as Tetris
import keyboard as key

Tetris.run()

# 키 이름 → 함수 매핑
key_actions = {
    "w": Tetris.hardDrop,
    "a": Tetris.moveLeft,
    "s": Tetris.softDrop,
    "d": Tetris.moveRight,
    "j": Tetris.rotateLeft,
    "l": Tetris.rotateRight,
    "i": Tetris.hold,
}

def control(event):
    if event.event_type != "down":
        return
    action = key_actions.get(event.name)
    if action:
        action()

# 훅 등록
key.hook(control)