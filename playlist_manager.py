
class PlaylistManager:
    def __init__(self):
        self.items = []
        self.index = -1
    def add(self, path):
        self.items.append(path)
    def next(self):
        if not self.items: return None
        self.index = (self.index + 1) % len(self.items)
        return self.items[self.index]
    def prev(self):
        if not self.items: return None
        self.index = (self.index - 1) % len(self.items)
        return self.items[self.index]
