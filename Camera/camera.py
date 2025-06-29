import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# 손가락이 모두 붙어 있는지 확인
def fingers_together(hand_landmarks, threshold=0.08):
    tips = [8, 12, 16, 20]
    for i in range(len(tips) - 1):
        x1, y1 = hand_landmarks.landmark[tips[i]].x, hand_landmarks.landmark[tips[i]].y
        x2, y2 = hand_landmarks.landmark[tips[i + 1]].x, hand_landmarks.landmark[tips[i + 1]].y
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist > threshold:
            return False
    return True

# 손가락이 펼쳐져 있는지 확인 (회전용)
def fingers_spread(hand_landmarks, threshold=0.12):
    tips = [8, 12, 16, 20]
    for i in range(len(tips) - 1):
        x1, y1 = hand_landmarks.landmark[tips[i]].x, hand_landmarks.landmark[tips[i]].y
        x2, y2 = hand_landmarks.landmark[tips[i + 1]].x, hand_landmarks.landmark[tips[i + 1]].y
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist < threshold:
            return False
    return True

# 손가락 평균 방향으로 방향 결정
def get_hand_direction(hand_landmarks):
    tips = [8, 12, 16, 20]
    avg_x = sum(hand_landmarks.landmark[i].x for i in tips) / len(tips)
    avg_y = sum(hand_landmarks.landmark[i].y for i in tips) / len(tips)
    base_x = hand_landmarks.landmark[0].x
    base_y = hand_landmarks.landmark[0].y

    dx = avg_x - base_x
    dy = avg_y - base_y

    angle = math.degrees(math.atan2(dy, dx))

    if -75 <= angle <= 75:
        return "왼쪽"
    elif 75 < angle <= 120:
        return "아래"
    elif angle > 120 or angle < -120:
        return "오른쪽"
    else:
        return "회전"

# 손가락 끝과 손목 간 평균 거리로 주먹 판단
def is_fist(hand_landmarks):
    wrist = hand_landmarks.landmark[0]
    tips = [4, 8, 12, 16, 20]
    total = 0
    for tip in tips:
        x1, y1 = wrist.x, wrist.y
        x2, y2 = hand_landmarks.landmark[tip].x, hand_landmarks.landmark[tip].y
        dist = math.hypot(x2 - x1, y2 - y1)
        total += dist
    avg_dist = total / len(tips)
    return avg_dist < 0.1

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5) as hands:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if is_fist(hand_landmarks):
                # 아무것도 출력하지 않음 (주먹)
                pass

            elif fingers_together(hand_landmarks):
                direction = get_hand_direction(hand_landmarks)
                text = f"{direction} (손가락 붙임)"
                cv2.putText(image, text, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)
                print(direction)

            elif fingers_spread(hand_landmarks):
                direction = get_hand_direction(hand_landmarks)
                if direction == "위":
                    cv2.putText(image, "회전", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                    print("회전")

        cv2.imshow("Hand Gesture", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
