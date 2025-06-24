from memory_block import MemoryBlock
from utils.logger import log_defragmentation

class MemoryManager:
    def __init__(self, total_size, strategy):
        self.memory_blocks = [MemoryBlock(0, total_size)]
        self.strategy = strategy
        self.next_process_id = 1

    def set_strategy(self, strategy):
        self.strategy = strategy

    def allocate_memory(self, size):
        pid = self.next_process_id
        self.next_process_id += 1
        address = self.strategy.allocate(self.memory_blocks, size, pid)
        return pid, address

    def free_memory(self, process_id):
        freed = False
        for block in self.memory_blocks:
            if not block.is_free and block.process_id == process_id:
                block.is_free = True
                block.process_id = None
                freed = True
        if freed:
            self.defragment()

    def defragment(self):
        i = 0
        while i < len(self.memory_blocks) - 1:
            curr = self.memory_blocks[i]
            next_block = self.memory_blocks[i + 1]
            if curr.is_free and next_block.is_free:
                curr.size += next_block.size
                self.memory_blocks.pop(i + 1)
            else:
                i += 1
        log_defragmentation()

    def get_memory_state(self):
        return [
            {
                'start': block.start,
                'size': block.size,
                'is_free': block.is_free,
                'process_id': block.process_id
            }
            for block in self.memory_blocks
        ]

    def count_fragmentation(self):
        free_blocks = [block for block in self.memory_blocks if block.is_free]
        if not free_blocks:
            return 0
        total_free = sum(block.size for block in free_blocks)
        largest_free = max(block.size for block in free_blocks)
        if len(free_blocks) == 1:
            return 0
        fragmentation_ratio = 1 - (largest_free / total_free)
        return round(fragmentation_ratio * 100, 2)