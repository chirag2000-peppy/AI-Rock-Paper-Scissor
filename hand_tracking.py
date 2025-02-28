import cv2
import mediapipe as mp
import random

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Game choices
choices = ["Rock ✊", "Paper 🖐", "Scissors ✌"]

# Start webcam
cap = cv2.VideoCapture(0)

def detect_gesture(hand_landmarks):
    """Detects Rock, Paper, or Scissors based on hand landmarks."""
    tips = [8, 12, 16, 20]  # Fingertip landmarks (index, middle, ring, pinky)
    base = [6, 10, 14, 18]  # Corresponding knuckle landmarks

    fingers = []
    for tip, knuckle in zip(tips, base):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[knuckle].y:
            fingers.append(1)  # Finger is open
        else:
            fingers.append(0)  # Finger is closed

    if fingers == [0, 0, 0, 0]:  # All fingers closed
        return "Rock ✊"
    elif fingers == [1, 1, 1, 1]:  # All fingers open
        return "Paper 🖐"
    elif fingers == [1, 1, 0, 0]:  # Index & middle fingers open
        return "Scissors ✌"
    else:
        return "Unknown"

def determine_winner(player, computer):
    """Determines the winner between player and computer."""
    if player == computer:
        return "It's a Tie! 🤝"
    elif (player == "Rock ✊" and computer == "Scissors ✌") or \
         (player == "Scissors ✌" and computer == "Paper 🖐") or \
         (player == "Paper 🖐" and computer == "Rock ✊"):
        return "You Win! 🎉"
    else:
        return "Computer Wins! 🤖"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    player_move = "Waiting..."
    computer_move = random.choice(choices)  # AI chooses its move

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            player_move = detect_gesture(hand_landmarks)

    # Determine result
    if player_move in choices:
        result_text = determine_winner(player_move, computer_move)
    else:
        result_text = "Make a valid move!"

    # Display choices
    cv2.putText(frame, f"Your Move: {player_move}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Computer: {computer_move}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, result_text, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Rock-Paper-Scissors AI", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()