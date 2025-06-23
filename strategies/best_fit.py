from memory_block import MemoryBlock
from utils.logger import log_allocation, log_failed_allocation

class BestFitStrategy:
    def allocate(self, blocks, size, process_id):
        best_block = None
        for block in blocks:
            if block.is_free and block.size >= size:
                if best_block is None or block.size < best_block.size:
                    best_block = block
        if best_block:
            new_block = MemoryBlock(best_block.start, size, False, process_id)
            remaining = best_block.size - size
            index = blocks.index(best_block)
            if remaining > 0:
                next_block = MemoryBlock(best_block.start + size, remaining, True)
                blocks[index:index+1] = [new_block, next_block]
            else:
                best_block.is_free = False
                best_block.process_id = process_id
            log_allocation("BestFit", process_id, size, new_block.start)
            return new_block.start
        log_failed_allocation("BestFit", size)
        return -1