
import librosa, numpy as np
from eq_presets import EQ_PRESETS
class AutoEQ:
    def __init__(self, engine):
        self.engine = engine
    def suggest_preset(self, filepath):
        try:
            y, sr = librosa.load(filepath, sr=22050, mono=True, duration=60)
            centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
            if centroid < 2000:
                preset = "Bass Boost"
            else:
                preset = "Vocal Boost"
            return preset
        except Exception:
            return "Flat"
