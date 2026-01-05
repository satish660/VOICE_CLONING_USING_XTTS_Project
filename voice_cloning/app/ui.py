import gradio as gr
import os
import numpy as np
import librosa
import matplotlib.pyplot as plt
from scipy.signal import resample
from resemblyzer import VoiceEncoder, preprocess_wav
from TTS.api import TTS
from pydub import AudioSegment
import soundfile as sf

# Load models
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
encoder = VoiceEncoder()

output_dir = "samples/output_audio"
os.makedirs(output_dir, exist_ok=True)

def plot_waveform(audio_path, img_name):
    audio, sr = librosa.load(audio_path)
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.plot(audio)
    ax.set_title(f"Waveform: {img_name}")
    fig_path = os.path.join(output_dir, img_name + ".png")
    fig.savefig(fig_path)
    plt.close(fig)
    return fig_path

def get_similarity(a, b):
    wav1 = preprocess_wav(a)
    wav2 = preprocess_wav(b)
    emb1 = encoder.embed_utterance(wav1)
    emb2 = encoder.embed_utterance(wav2)
    sim = float(np.inner(emb1, emb2))
    return round(sim, 3)

def process(audio, text, ai_level):
    if audio is None:
        return "⚠ Upload or record sample!", None, None, None, None

    cloned = os.path.join(output_dir, "cloned.wav")
    blended = os.path.join(output_dir, "final_output.wav")

    # Step 1 — Generate cloned voice
    tts.tts_to_file(
        text=text,
        speaker_wav=audio,
        language="en",
        file_path=cloned
    )

    # Step 2 — AI mix (style strength)
    if ai_level < 100:
        orig = AudioSegment.from_file(audio).set_frame_rate(16000).set_channels(1)
        gen = AudioSegment.from_file(cloned)
        mix = orig.overlay(gen, gain_during_overlay=-ai_level/3)
        mix.export(blended, format="wav")
        final_audio = blended
    else:
        final_audio = cloned

    # Step 3 — Similarity score
    similarity = get_similarity(audio, final_audio)

    # Step 4 — Waveforms
    in_plot = plot_waveform(audio, "input_waveform")
    out_plot = plot_waveform(final_audio, "output_waveform")

    return (
        f"Similarity Score: {similarity}",
        final_audio,
        in_plot,
        out_plot,
        similarity
    )

ui = gr.Interface(
    fn=process,
    inputs=[
        gr.Audio(type="filepath", label="🎤 Upload or Record Voice"),
        gr.Textbox(label="💬 Enter Text"),
        gr.Slider(0, 100, 100, label="🤖 AI Strength (%)")
    ],
    outputs=[
        gr.Text(label="📈 Metrics"),
        gr.Audio(label="🔊 Output Audio"),
        gr.Image(label="📊 Input Waveform"),
        gr.Image(label="📊 Output Waveform"),
        gr.Number(label="🔍 Similarity Score")
    ],
    title="🎙️ VocalMimic Pro — Voice Cloning Lab",
    description="Record or upload voice, generate cloned audio, compare waveforms, and view similarity score."
)


ui.launch(share=True)

