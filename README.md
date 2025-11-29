
# AIM PLAYER — Desktop & PWA (Production)

**AIM PLAYER** is a professional, full-featured media player implemented as both:
- a Streamlit PWA (browser-based), and
- a native Desktop app (Tkinter / CustomTkinter) — now extended with an **offline ML-based Auto-EQ** system and **video support**.

This README documents the full production bundle: how the Auto-EQ model works, training/inference, video support, packaging, and deployment.

---

## Key Features

- 31-band equalizer with presets and custom sliders.
- Visualizer: waveform + bar visualizations in real time.
- Server-side audio effects (pydub): bass boost, reverb, reset.
- **Advanced Offline Auto-EQ (ML)**: small PyTorch model predicts a 31-band EQ tailored to each track.
- **Video support**: extract audio from video for analysis and playback.
- Mini-player, lyrical display (LRC), multiple themes (Dark, Light, Neon, Glass).
- Packaging scripts: PyInstaller build + Inno Setup script for installer on Windows.
- Offline PWA version (service worker & manifest) for browser-based app.

---

## Project structure (production)

aim_player_production/
├─ app.py # Desktop main app (Tkinter / CustomTkinter)
├─ audio_engine.py # Playback, EQ application, simpleaudio wrapper
├─ visualizer.py # Waveform & Bars visualizers
├─ playlist_manager.py
├─ eq_presets.py
├─ ai_autoeq.py # Inference wrapper (loads models/auto_eq.pt)
├─ ai_auto_eq_model.py # PyTorch model definition
├─ train_auto_eq.py # Training script to create models/auto_eq.pt
├─ utils/video_utils.py # Video -> audio extraction
├─ lyrics.py
├─ modules/... (if using Streamlit PWA version)
├─ models/ # models/auto_eq.pt (generated or downloaded)
├─ assets/icon.png
├─ requirements.txt
├─ build_exe.bat
├─ AIM_PLAYER_Installer.iss
└─ README.md


---

## Machine Learning Auto-EQ (Offline)

### Model
- Small convolutional neural network (`TinyEQNet`) implemented in PyTorch.
- Input: normalized mel-spectrogram (shape: `1 x n_mels x T`).
- Output: 31 real-valued gains (dB) — regression.

### Training
- `train_auto_eq.py` is provided. It can:
  - create synthetic training pairs by applying random 31-band gains to audio, or
  - use real (audio, human-chosen gains) pairs if available.
- Recommended dataset: a mixture of music and speech (varied genres) — at least several hours for decent performance.
- Command:
  ```bash
  python train_auto_eq.py "data/audio/*.wav"
