from flask import Flask, render_template, request, jsonify
import os
import numpy as np
import librosa
from utils.audio_tools import convert_to_wav
from utils.voice_clone import clone_voice

app = Flask(__name__)

UPLOAD_FOLDER = "static/audio"
WAVEFORM_FOLDER = "static/waveforms"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(WAVEFORM_FOLDER, exist_ok=True)

def get_waveform_data(path, n_points=800):
    y, sr = librosa.load(path, sr=None)
    y = librosa.resample(y, orig_sr=sr, target_sr=16000)
    if len(y) > n_points:
        y = y[:n_points]
    x = list(range(len(y)))
    return {"x": x, "y": y.tolist()}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    audio_file = request.files.get('audio')
    text_input = request.form.get('text')
    ai_strength = int(request.form.get('ai_strength', 100))

    if not audio_file:
        return jsonify({"error": "No audio file provided."}), 400

    filepath = os.path.join(UPLOAD_FOLDER, audio_file.filename)
    audio_file.save(filepath)
    wav_path = convert_to_wav(filepath, UPLOAD_FOLDER)

    cloned, in_wave, out_wave, sim = clone_voice(
        wav_path, text_input, ai_strength, UPLOAD_FOLDER, WAVEFORM_FOLDER
    )

    input_data = get_waveform_data(wav_path)
    output_data = get_waveform_data(cloned)

    encoder_data = {"x": input_data["x"], "y": (np.array(input_data["y"]) * 0.6).tolist()}
    vocoder_data = {"x": input_data["x"], "y": (np.array(input_data["y"]) * 0.8).tolist()}
    synth_data = {"x": input_data["x"], "y": (np.array(output_data["y"]) * 1.2).tolist()}

    ai_contrib = round(ai_strength / 100, 2)

    return jsonify({
        "cloned_audio": cloned,
        "similarity": sim,
        "ai_contribution": ai_contrib,
        "input_waveform": input_data,
        "encoder_waveform": encoder_data,
        "vocoder_waveform": vocoder_data,
        "synth_waveform": synth_data,
        "output_waveform": output_data
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
