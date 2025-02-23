from flask import Flask, request, jsonify
import cv2
import numpy as np
from fer import FER
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image

app = Flask(__name__)

# Load Emotion Recognition Model
detector = FER()

# Spotify API Authentication
SPOTIPY_CLIENT_ID = "79d2dcdcae934bdfb9943f92ece5cf7b"
SPOTIPY_CLIENT_SECRET = "6495ecde874b442e8abf6456d8686e5c"
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="user-modify-playback-state"))

# Mood-based Playlist Mapping
mood_playlist = {
    "happy": "spotify:playlist:37i9dQZF1DXdPec7aLTmlC",  # Happy Songs
    "sad": "spotify:playlist:37i9dQZF1DX7qK8ma5wgG1",     # Sad Songs
    "neutral": "spotify:playlist:37i9dQZF1DWXJfnUiYjUKT", # Chill/Neutral Songs
    "angry": "spotify:playlist:37i9dQZF1DX76Wlfdnj7AP"    # Angry Songs
}

@app.route("/")
def home():
    return "Mood-Based Music Player API is running!"

@app.route("/detect-mood", methods=["POST"])
def detect_mood():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]
    image = Image.open(file).convert("RGB")
    image = np.array(image)

    # Detect emotion
    result = detector.top_emotion(image)
    mood = result[0] if result else "neutral"

    # Fetch playlist based on mood
    playlist_uri = mood_playlist.get(mood, mood_playlist["neutral"])
    sp.start_playback(context_uri=playlist_uri)

    return jsonify({"mood": mood, "message": f"Playing {mood} music!"})

if __name__ == "__main__":
    app.run(debug=True)
