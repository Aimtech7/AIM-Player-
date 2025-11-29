
# visualizer.py - waveform and bars visualizers for Tkinter Canvas
import time, numpy as np

class WaveformVisualizer:
    def __init__(self, canvas):
        self.canvas = canvas
        self.running = False

    def run(self, samples, rate):
        self.running = True
        width = int(self.canvas.winfo_width() or 800)
        height = int(self.canvas.winfo_height() or 200)
        step = max(1, len(samples) // width)
        while self.running:
            try:
                self.canvas.delete("all")
                for x in range(0, width, 4):
                    i = x*step
                    amp = int(abs(int(samples[i]))/1000) if i < len(samples) else 0
                    y = height//2 - amp
                    self.canvas.create_line(x, height//2, x, y, fill="#00ff88")
                self.canvas.update()
                time.sleep(0.03)
            except Exception:
                break

class BarsVisualizer:
    def __init__(self, canvas):
        self.canvas = canvas
        self.running = False

    def run(self, samples, rate):
        self.running = True
        import numpy as np
        bars = 40
        chunk = max(1, len(samples)//bars)
        while self.running:
            try:
                self.canvas.delete("all")
                for i in range(bars):
                    seg = samples[i*chunk:(i+1)*chunk]
                    val = int(np.mean(np.abs(seg))/500)
                    x = i*(self.canvas.winfo_width()//bars)
                    self.canvas.create_rectangle(x, self.canvas.winfo_height()-val, x+10, self.canvas.winfo_height(), fill="#00ff88")
                self.canvas.update()
                time.sleep(0.04)
            except Exception:
                break
