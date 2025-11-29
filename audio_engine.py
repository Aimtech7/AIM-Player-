
# audio_engine.py - playback, EQ, and visualization hooks
import threading, time
from pydub import AudioSegment, effects
import numpy as np, simpleaudio as sa

class AudioEngine:
    def __init__(self):
        self.current_play = None
        self.play_obj = None
        self.volume = 0.8
        self.eq = {}

    def update_eq(self, freq, gain):
        self.eq[freq] = gain

    def apply_eq(self, audio):
        avg_gain = sum(self.eq.values())/len(self.eq) if self.eq else 0
        return audio + avg_gain*0.5

    def play(self, filepath, waveform_vis=None, bars_vis=None):
        audio = AudioSegment.from_file(filepath)
        audio = audio + (self.volume*10)
        audio = self.apply_eq(audio)
        samples = np.array(audio.get_array_of_samples()).astype(np.int16)
        self.play_obj = sa.play_buffer(samples.tobytes(), num_channels=audio.channels, bytes_per_sample=2, sample_rate=audio.frame_rate)
        if waveform_vis:
            threading.Thread(target=waveform_vis.run, args=(samples, audio.frame_rate), daemon=True).start()
        if bars_vis:
            threading.Thread(target=bars_vis.run, args=(samples, audio.frame_rate), daemon=True).start()

    def toggle_pause(self):
        if self.play_obj and self.play_obj.is_playing():
            self.play_obj.stop()

    def set_volume(self, v):
        self.volume = float(v)

    def volume_up(self):
        self.volume = min(1.0, self.volume + 0.05)

    def volume_down(self):
        self.volume = max(0.0, self.volume - 0.05)

    def stop_all(self):
        if self.play_obj:
            try: self.play_obj.stop()
            except: pass
