
import tkinter as tk, os, time
from tkinter import scrolledtext
class LyricsDisplay:
    def __init__(self, master):
        self.frame = tk.Frame(master, bg="#050505")
        self.text = scrolledtext.ScrolledText(self.frame, height=6, bg="#050505", fg="#00ff88", state="disabled")
        self.text.pack(fill="both", expand=True)
        self.lines = []
        self.times = []
        self.playing = False

    def load_lrc(self, path):
        self.lines=[]; self.times=[]
        if not os.path.exists(path): return
        with open(path, encoding="utf-8", errors="ignore") as f:
            for ln in f:
                parts = ln.strip().split("]")
                if len(parts) >=2 and parts[0].startswith("["):
                    ts = parts[0][1:]
                    try:
                        m,s = ts.split(":")
                        t = int(m)*60 + float(s)
                        self.times.append(t); self.lines.append("]".join(parts[1:]))
                    except: pass
        self.text.configure(state="normal"); self.text.delete("1.0","end")
        for l in self.lines: self.text.insert("end", l+"\\n")
        self.text.configure(state="disabled")

    def sync(self, current_seconds):
        for i,t in enumerate(self.times):
            if current_seconds >= t and (i==len(self.times)-1 or current_seconds < self.times[i+1]):
                self.text.configure(state="normal"); self.text.tag_remove("hl","1.0","end")
                self.text.tag_add("hl", f"{i+1}.0", f"{i+1}.end"); self.text.tag_config("hl", background="#00ff88", foreground="#000")
                self.text.see(f"{i+1}.0"); self.text.configure(state="disabled"); break
