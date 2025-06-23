from memory_block import MemoryBlock
from utils.logger import log_allocation, log_failed_allocation

class WorstFitStrategy:
    def allocate(self, blocks, size, process_id):
        worst_block = None
        for block in blocks:
            if block.is_free and block.size >= size:
                if worst_block is None or block.size > worst_block.size:
                    worst_block = block
        if worst_block:
            new_block = MemoryBlock(worst_block.start, size, False, process_id)
            remaining = worst_block.size - size
            index = blocks.index(worst_block)
            if remaining > 0:
                next_block = MemoryBlock(worst_block.start + size, remaining, True)
                blocks[index:index+1] = [new_block, next_block]
            else:
                worst_block.is_free = False
                worst_block.process_id = process_id
            log_allocation("WorstFit", process_id, size, new_block.start)
            return new_block.start
        log_failed_allocation("WorstFit", size)
        return -1