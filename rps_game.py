import cv2
import mediapipe as mp
import random
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Game choices
choices = ["Rock ✊", "Paper 🖐", "Scissors ✌"]

# Initialize game variables
player_score = 0
computer_score = 0
round_number = 0
win_threshold = 3
cap = cv2.VideoCapture(0)
game_active = False  # To prevent multiple clicks

# GUI setup
root = tk.Tk()
root.title("Rock Paper Scissors AI")
root.geometry("800x600")
root.configure(bg="#222")

# Labels
title_label = Label(root, text="Rock Paper Scissors", font=("Arial", 28, "bold"), fg="white", bg="#222")
title_label.pack(pady=10)

video_label = Label(root, bg="#222")
video_label.pack()

status_label = Label(root, text="Press Play to Start", font=("Arial", 16), fg="white", bg="#222")
status_label.pack()

score_label = Label(root, text="Player: 0 | Computer: 0", font=("Arial", 16, "bold"), fg="white", bg="#222")
score_label.pack()

# Gesture detection function
def detect_gesture(hand_landmarks):
    tips = [8, 12, 16, 20]  # Fingertips (index, middle, ring, pinky)
    base = [6, 10, 14, 18]  # Corresponding knuckle landmarks

    fingers = []
    for tip, knuckle in zip(tips, base):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[knuckle].y:
            fingers.append(1)  # Open
        else:
            fingers.append(0)  # Closed

    if fingers == [0, 0, 0, 0]:
        return "Rock ✊"
    elif fingers == [1, 1, 1, 1]:
        return "Paper 🖐"
    elif fingers == [1, 1, 0, 0]:
        return "Scissors ✌"
    else:
        return "Unknown"

# Determine winner function
def determine_winner(player, computer):
    if player == computer:
        return "It's a Tie! 🤝"
    elif (player == "Rock ✊" and computer == "Scissors ✌") or \
         (player == "Scissors ✌" and computer == "Paper 🖐") or \
         (player == "Paper 🖐" and computer == "Rock ✊"):
        return "You Win! 🎉"
    else:
        return "Computer Wins! 🤖"

# Countdown function
def countdown():
    for i in range(3, 0, -1):
        status_label.config(text=f"Get Ready... {i}", fg="yellow")
        root.update()
        time.sleep(1)

# Play round function
def play_round():
    global player_score, computer_score, round_number, game_active

    if player_score == win_threshold or computer_score == win_threshold or game_active:
        return

    game_active = True  # Prevent multiple plays at once
    countdown()

    ret, frame = cap.read()
    if ret:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        player_move = "Waiting..."
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                player_move = detect_gesture(hand_landmarks)

        computer_move = random.choice(choices)
        
        if player_move in choices:
            result = determine_winner(player_move, computer_move)
            if "You Win" in result:
                player_score += 1
            elif "Computer Wins" in result:
                computer_score += 1
        else:
            result = "Invalid move, try again!"

        score_label.config(text=f"Player: {player_score} | Computer: {computer_score}")
        status_label.config(text=f"Your Move: {player_move} | AI: {computer_move}\n{result}", fg="cyan")

        round_number += 1

    if player_score == win_threshold:
        status_label.config(text="🎉 You Win the Game! 🎉", fg="green")
        next_round_button.config(state=tk.DISABLED)
    elif computer_score == win_threshold:
        status_label.config(text="🤖 Computer Wins the Game! 🤖", fg="red")
        next_round_button.config(state=tk.DISABLED)

    game_active = False  # Allow next round

# Start a new game
def start_game():
    global player_score, computer_score, round_number, game_active
    player_score = 0
    computer_score = 0
    round_number = 0
    game_active = False
    score_label.config(text="Player: 0 | Computer: 0")
    status_label.config(text="Game Started! Make your move...", fg="white")
    next_round_button.config(state=tk.NORMAL)
    play_round()

# Move to next round
def next_round():
    if player_score < win_threshold and computer_score < win_threshold:
        play_round()

# Exit the game
def exit_game():
    root.quit()

# Buttons
button_style = {"font": ("Arial", 16), "fg": "white", "bg": "#444", "width": 12, "height": 2}

play_button = Button(root, text="Play", command=start_game, **button_style)
play_button.pack(pady=5)

next_round_button = Button(root, text="Next Round", command=next_round, **button_style)
next_round_button.pack(pady=5)
next_round_button.config(state=tk.DISABLED)

exit_button = Button(root, text="Exit", command=exit_game, **button_style)
exit_button.pack(pady=5)

# Function to update webcam feed
def update_video():
    ret, frame = cap.read()
    if ret:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        img = ImageTk.PhotoImage(img)
        video_label.img = img
        video_label.config(image=img)

    root.after(10, update_video)

update_video()
root.mainloop()