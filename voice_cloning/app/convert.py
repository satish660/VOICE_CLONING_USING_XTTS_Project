from pydub import AudioSegment

input_file = "samples/input_voice/Barack obama.mp3"
output_file = "samples/input_voice/sample.wav"

audio = AudioSegment.from_mp3(input_file)
audio = audio.set_frame_rate(22050).set_channels(1)  # required format
audio.export(output_file, format="wav")

print("✔ Converted to WAV:", output_file)
