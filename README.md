# VOICE_CLONING_USING_XTTS_Project
📌 Project Overview

VocalMimic Pro is a Voice Cloning Web Application that allows users to upload or record a voice sample and generate speech in the same cloned voice using XTTS v2 (Coqui TTS).

The system supports:

AI voice cloning

Multilingual speech generation

Waveform visualization

Similarity score comparison between original & generated voice

Clean and interactive UI

This project integrates AI + Web + Audio Signal Processing — making it suitable for research, college projects, and real-world AI applications.

🛠️ Tech Stack
🔹 Backend

Python

XTTS v2 (Coqui TTS)

Torch

Resemblyzer (Voice similarity)

Librosa / NumPy / SciPy

🔹 Frontend

HTML

CSS

JavaScript

Audio UI Components

Waveform Visualization

🚀 Features

✔ Clone any voice using short audio
✔ Converts any format → WAV automatically
✔ Adjustable AI Strength (natural vs neural tone)
✔ Generates final WAV speech output
✔ Similarity score calculation
✔ Waveform comparison graphs
✔ Clean UI with user-friendly controls

📂 Project Structure
Voice_Cloning_XTTS_Project
│
├── app/
│   ├── ui.py              → Main Application (Gradio / Flask UI)
│   ├── convert.py         → Converts any audio to WAV
│
├── static/
│   ├── audio/             → UI audio assets
│   ├── css/               → Styling files
│   ├── js/                → record.js & logic scripts
│   ├── waveform/          → waveform graphics
│
├── templates/
│   ├── index.html         → Homepage
│   ├── result.html        → Output page
│
├── samples/
│   ├── input/             → Sample input voices
│   ├── output/            → Generated cloned voices
│
├── requirements.txt
├── README.md
└── .gitignore

▶️ How to Run
1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Run Application
python app/ui.py

3️⃣ Use Application

1️⃣ Upload or record your voice
2️⃣ Enter text to synthesize
3️⃣ Adjust AI Strength
4️⃣ Click Generate 🎧

You’ll get:

Cloned audio

Waveform visuals

Similarity score

🎧 Output

Generated audios are saved in:

samples/output/

📊 Similarity Score

The system uses Resemblyzer encoder embeddings to compare:

Input Voice

Generated Voice

Higher score = Higher similarity
