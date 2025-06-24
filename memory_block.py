class MemoryBlock:
    def __init__(self, start, size, is_free=True, process_id=None):
        self.start = start
        self.size = size
        self.is_free = is_free
        self.process_id = process_id

    def __repr__(self):
        status = "Free" if self.is_free else f"Allocated to P{self.process_id}"
        return f"[{self.start}-{self.start + self.size}) {status}]"