
# AIM PLAYER Desktop - Production Bundle (Full)

This bundle contains the full AIM PLAYER desktop application with additional features:

- Installer script (PyInstaller + Inno Setup)
- Multiple UI themes (Dark, Light, Neon, Glass)
- Lyrics support (.lrc)
- Mini-player window
- Waveform & Bars visualizers
- AI-based Auto-EQ (librosa heuristic)

## How to build the EXE (Windows)

1. Install Python 3.10+ and Git
2. Create and activate a virtualenv
3. Install dependencies:
   pip install -r requirements.txt
4. Build executable using PyInstaller (Windows):
   pyinstaller --noconfirm --onefile --windowed --icon=assets/icon.ico app.py
   This produces `dist\\app.exe`

5. (Optional) Create installer using Inno Setup:
   - Open `AIM_PLAYER_Installer.iss` in Inno Setup Compiler and compile.
   - Or run `iscc AIM_PLAYER_Installer.iss` if `iscc` is on PATH.

## Notes
- pydub requires ffmpeg installed and on PATH.
- AI Auto-EQ uses librosa to analyze the first 60 seconds of track to suggest a preset.
- Visualizers are lightweight and run in background threads.
