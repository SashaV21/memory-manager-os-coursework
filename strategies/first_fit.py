from memory_block import MemoryBlock
from utils.logger import log_allocation, log_failed_allocation

class FirstFitStrategy:
    def allocate(self, blocks, size, process_id):
        for block in blocks:
            if block.is_free and block.size >= size:
                new_block = MemoryBlock(block.start, size, False, process_id)
                remaining = block.size - size
                if remaining > 0:
                    next_block = MemoryBlock(block.start + size, remaining, True)
                    index = blocks.index(block)
                    blocks[index:index+1] = [new_block, next_block]
                else:
                    block.is_free = False
                    block.process_id = process_id
                log_allocation("FirstFit", process_id, size, new_block.start)
                return new_block.start
        log_failed_allocation("FirstFit", size)
        return -1