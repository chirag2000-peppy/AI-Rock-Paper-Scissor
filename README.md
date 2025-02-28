Rock-Paper-Scissors AI Game

A computer vision-based Rock-Paper-Scissors game where you play against an AI that detects your hand gestures using OpenCV and MediaPipe.

Features----

Real-time Hand Gesture Recognition
Interactive GUI with Play & Exit Buttons
3..2..1 Countdown Before Each Round
Automatic Winner Declaration (Best of 5 Rounds)
How It Works
The camera detects your hand sign.
The AI analyzes your gesture (Rock ✊, Paper ✋, or Scissors ✌️).
The game determines who wins the round.
First to 3 wins out of 5 rounds is declared the winner.

Installation-

1. Clone the Repository:

bash
git clone https://github.com/chirag2000-peppy/rock-paper-scissors-ai.git
cd rock-paper-scissors-ai

2. Install Dependencies:

bash
pip install -r requirements.txt

3. Run the Game:

bash
python main.py

Dependencies:
Python 3.x
OpenCV
MediaPipe
NumPy
Tkinter (for GUI)

Install them manually:

bash
pip install opencv-python mediapipe numpy

How to Play:
Show Rock ✊, Paper ✋, or Scissors ✌️ to the camera.
The AI makes its move and compares results.
The first player to win 3 out of 5 rounds is the champion.

Author
Chirag | AI & Data Science Enthusiast

GitHub: @chirag2000-peppy
