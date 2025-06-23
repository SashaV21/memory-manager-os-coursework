class MemoryBlock:
    def __init__(self, start, size, is_free=True, process_id=None):
        self.start = start         # Адрес начала блока
        self.size = size           # Размер блока
        self.is_free = is_free     # Свободен ли?
        self.process_id = process_id  # ID процесса, если занят

    def __repr__(self):
        status = "Free" if self.is_free else f"Allocated to P{self.process_id}"
        return f"[{self.start}-{self.start + self.size}) {status}]"