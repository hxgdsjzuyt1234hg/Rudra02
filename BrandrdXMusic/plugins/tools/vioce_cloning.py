from pydub import AudioSegment
import numpy as np
import librosa

# Load the audio file
audio_path = 'path_to_your_audio_file.wav'
audio = AudioSegment.from_file(audio_path)

# Convert to numpy array for processing
samples = np.array(audio.get_array_of_samples())
sr = audio.frame_rate

# Transform the voice (simple pitch shift example)
def pitch_shift(samples, sampling_rate, pitch_factor):
    return librosa.effects.pitch_shift(samples.astype(float), sampling_rate, pitch_factor)

# Apply pitch shift to make the voice sound like a girl's voice
pitch_factor = 4.0  # Higher pitch factor for more feminine voice
shifted_samples = pitch_shift(samples, sr, pitch_factor)

# Convert back to AudioSegment
shifted_audio = AudioSegment(
    shifted_samples.tobytes(),
    frame_rate=sr,
    sample_width=audio.sample_width,
    channels=audio.channels
)

# Export the modified audio
shifted_audio.export('output_audio.wav', format='wav')
