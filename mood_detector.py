import cv2
import numpy as np
import subprocess
import sys
from fer import FER

detector = FER()
cap = cv2.VideoCapture(0)

print("📷 Press 'P' to detect mood. Press 'Q' to quit.")

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    # Display video feed
    cv2.imshow("Mood Detection", frame)

    # Press 'P' to detect mood
    key = cv2.waitKey(1) & 0xFF
    if key == ord("p"):
        print("🔍 Detecting mood...")

        # Detect emotion
        result = detector.top_emotion(frame)
        mood = result[0] if result else "neutral"

        print(f"🧠 Detected mood: {mood}")

        # Call spotify_player.py with correct virtual environment
        subprocess.run([sys.executable, "spotify_player.py", mood])

    # Press 'Q' to exit
    elif key == ord("q"):
        print("👋 Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
