
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from audio_engine import AudioEngine
from playlist_manager import PlaylistManager
from visualizer import WaveformVisualizer, BarsVisualizer
from eq_presets import EQ_BANDS, EQ_PRESETS
from lyrics import LyricsDisplay
from ai_autoeq import AutoEQ

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class AIMPlayerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AIM PLAYER — Desktop Edition (Full)")
        self.geometry("1200x720")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.engine = AudioEngine()
        self.playlist = PlaylistManager()
        self.auto_eq = AutoEQ(self.engine)
        self.lyrics = LyricsDisplay(self)
        self.current_visualizer = None

        self.build_ui()
        self.bind_hotkeys()

    def build_ui(self):
        top = ctk.CTkFrame(self); top.pack(fill="x", padx=12, pady=6)
        ctk.CTkButton(top, text="Add Files", command=self.add_files).pack(side="left", padx=8)
        ctk.CTkButton(top, text="Auto-EQ (AI)", command=self.run_autoeq).pack(side="left", padx=8)
        ctk.CTkButton(top, text="Toggle Mini Player", command=self.toggle_mini).pack(side="right", padx=8)

        main = ctk.CTkFrame(self); main.pack(fill="both", expand=True, padx=12, pady=6)
        left = ctk.CTkFrame(main, width=280); left.pack(side="left", fill="y", padx=6, pady=6)
        ctk.CTkLabel(left, text="Playlist", font=("Helvetica", 18)).pack(pady=6)
        self.listbox = tk.Listbox(left, bg="#0b0b0b", fg="#00ff88", selectbackground="#00ff88", selectforeground="#000")
        self.listbox.pack(fill="both", expand=True, padx=6, pady=6)
        ctk.CTkButton(left, text="Play Selected", command=self.play_selected).pack(pady=6)
        self.lyrics.frame.pack_forget()

        right = ctk.CTkFrame(main); right.pack(side="right", fill="both", expand=True, padx=6, pady=6)
        tab = ctk.CTkTabview(right); tab.pack(fill="both", expand=True, pady=6)
        tab.add("Waveform"); tab.add("Bars")
        self.waveform_canvas = tk.Canvas(tab.tab("Waveform"), bg="black", height=220); self.waveform_canvas.pack(fill="both", expand=True, padx=6, pady=6)
        self.bars_canvas = tk.Canvas(tab.tab("Bars"), bg="black", height=220); self.bars_canvas.pack(fill="both", expand=True, padx=6, pady=6)
        self.wave_vis = WaveformVisualizer(self.waveform_canvas); self.bars_vis = BarsVisualizer(self.bars_canvas)

        ctrl = ctk.CTkFrame(right); ctrl.pack(fill="x", pady=6)
        ctk.CTkButton(ctrl, text="⏮ Prev", command=self.prev_track).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="▶ Play/Pause", command=self.toggle_play).pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="⏭ Next", command=self.next_track).pack(side="left", padx=6)
        self.vol_slider = ctk.CTkSlider(ctrl, from_=0, to=1, number_of_steps=100, command=self.engine.set_volume); self.vol_slider.set(0.8); self.vol_slider.pack(side="right", padx=10)

        eq_frame = ctk.CTkFrame(right); eq_frame.pack(fill="x", pady=6)
        self.eq_sliders = {}
        for i, f in enumerate(EQ_BANDS):
            sl = ctk.CTkSlider(eq_frame, from_=-12, to=12, number_of_steps=48, orientation="vertical", command=lambda v, freq=f: self.update_eq(freq, v))
            sl.grid(row=0, column=i, padx=2, pady=6)
            self.eq_sliders[f] = sl
        preset_box = ctk.CTkComboBox(right, values=list(EQ_PRESETS.keys()), command=self.apply_preset); preset_box.set("Flat"); preset_box.pack(pady=6)

        self.mini = None

    def add_files(self):
        paths = filedialog.askopenfilenames(title="Select audio files", filetypes=[("Audio","*.mp3 *.wav *.flac *.m4a")])
        for p in paths:
            self.playlist.add(p); self.listbox.insert("end", os.path.basename(p))

    def play_selected(self):
        sel = self.listbox.curselection()
        if not sel: return
        idx = sel[0]; path = self.playlist.items[idx]
        threading.Thread(target=self.engine.play, args=(path, self.wave_vis, self.bars_vis), daemon=True).start()

    def toggle_play(self):
        self.engine.toggle_pause()

    def next_track(self):
        p = self.playlist.next(); threading.Thread(target=self.engine.play, args=(p, self.wave_vis, self.bars_vis), daemon=True).start()

    def prev_track(self):
        p = self.playlist.prev(); threading.Thread(target=self.engine.play, args=(p, self.wave_vis, self.bars_vis), daemon=True).start()

    def update_eq(self, freq, value):
        self.engine.update_eq(freq, float(value))

    def apply_preset(self, name):
        preset = EQ_PRESETS.get(name, {})
        for f, v in preset.items():
            if f in self.eq_sliders:
                self.eq_sliders[f].set(v); self.engine.update_eq(f, v)

    def toggle_mini(self):
        if self.mini and self.mini.winfo_exists():
            self.mini.destroy(); self.mini = None; return
        self.mini = ctk.CTkToplevel(self); self.mini.geometry("300x80"); self.mini.title("AIM MINI")
        ctk.CTkButton(self.mini, text="Prev", command=self.prev_track).pack(side="left", padx=6, pady=12)
        ctk.CTkButton(self.mini, text="Play/Pause", command=self.toggle_play).pack(side="left", padx=6, pady=12)
        ctk.CTkButton(self.mini, text="Next", command=self.next_track).pack(side="left", padx=6, pady=12)

    def toggle_lyrics(self):
        if self.show_lyrics_var.get():
            self.lyrics.frame.pack(side="bottom", fill="x")
        else:
            self.lyrics.frame.pack_forget()

    def apply_theme(self, name):
        if name == "Dark":
            ctk.set_appearance_mode("dark")
        elif name == "Light":
            ctk.set_appearance_mode("light")
        elif name == "Neon":
            ctk.set_appearance_mode("dark"); ctk.set_default_color_theme("green")
        elif name == "Glass":
            ctk.set_appearance_mode("dark"); ctk.set_default_color_theme("blue")

    def run_autoeq(self):
        sel = self.listbox.curselection()
        if not sel: messagebox.showinfo("Auto-EQ", "Select a track first"); return
        idx = sel[0]; path = self.playlist.items[idx]
        suggested = self.auto_eq.suggest_preset(path)
        if suggested:
            messagebox.showinfo("Auto-EQ", f"Suggested preset: {suggested}\\nApplied")
            self.apply_preset(suggested)

    def bind_hotkeys(self):
        self.bind("<space>", lambda e: self.toggle_play())
        self.bind("<Right>", lambda e: self.next_track())
        self.bind("<Left>", lambda e: self.prev_track())
        self.bind("<plus>", lambda e: self.engine.volume_up())
        self.bind("<minus>", lambda e: self.engine.volume_down())

    def on_close(self):
        self.engine.stop_all(); self.destroy()

if __name__ == '__main__':
    app = AIMPlayerApp(); app.mainloop()
