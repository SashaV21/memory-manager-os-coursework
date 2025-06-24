import unittest
from memory_manager import MemoryManager
from strategies import FirstFitStrategy, BestFitStrategy, WorstFitStrategy


class TestAllocationStrategies(unittest.TestCase):

    def test_first_fit_simple(self):
        manager = MemoryManager(100, FirstFitStrategy())
        p1, a1 = manager.allocate_memory(30)
        p2, a2 = manager.allocate_memory(20)
        self.assertEqual(a1, 0)
        self.assertEqual(a2, 30)

    def test_best_fit_smallest_block(self):
        manager = MemoryManager(100, BestFitStrategy())
        manager.allocate_memory(40)
        manager.allocate_memory(20)
        p3, a3 = manager.allocate_memory(10)
        self.assertEqual(a3, 60)

    def test_worst_fit_largest_block(self):
        manager = MemoryManager(100, WorstFitStrategy())
        p1, a1 = manager.allocate_memory(30)
        p2, a2 = manager.allocate_memory(20)
        self.assertEqual(a1, 0)
        self.assertEqual(a2, 30)

    def test_free_memory_and_defragmentation(self):
        manager = MemoryManager(100, FirstFitStrategy())
        p1, a1 = manager.allocate_memory(20)
        p2, a2 = manager.allocate_memory(20)
        manager.free_memory(p1)
        manager.free_memory(p2)
        self.assertEqual(len(manager.memory_blocks), 1)
        self.assertTrue(manager.memory_blocks[0].is_free)
        self.assertEqual(manager.memory_blocks[0].size, 100)

    def test_no_suitable_block(self):
        manager = MemoryManager(100, BestFitStrategy())
        manager.allocate_memory(50)
        manager.allocate_memory(30)
        pid, address = manager.allocate_memory(30)
        self.assertEqual(address, -1)

    def test_fragmentation_after_multiple_allocations(self):
        manager = MemoryManager(100, FirstFitStrategy())
        allocations = []
        sizes = [10, 20, 30, 25]
        for size in sizes:
            pid, addr = manager.allocate_memory(size)
            allocations.append(pid)
        for pid in allocations:
            manager.free_memory(pid)
        self.assertEqual(len(manager.memory_blocks), 1)
        self.assertTrue(manager.memory_blocks[0].is_free)
        self.assertEqual(manager.memory_blocks[0].size, 100)

    def test_best_fit_exact_fit(self):
        manager = MemoryManager(100, BestFitStrategy())
        manager.allocate_memory(40)
        manager.allocate_memory(30)
        manager.allocate_memory(29)
        pid, addr = manager.allocate_memory(1)
        self.assertEqual(addr, 99)

    def test_worst_fit_with_multiple_blocks(self):
        manager = MemoryManager(200, WorstFitStrategy())
        p1, a1 = manager.allocate_memory(50)
        p2, a2 = manager.allocate_memory(30)
        p3, a3 = manager.allocate_memory(60)
        manager.free_memory(p2)
        manager.free_memory(p1)
        p4, a4 = manager.allocate_memory(70)
        self.assertEqual(a4, 0)
    def test_strategy_change_runtime(self):
        manager = MemoryManager(100, FirstFitStrategy())
        manager.allocate_memory(30)
        manager.set_strategy(BestFitStrategy())
        p2, a2 = manager.allocate_memory(20)
        self.assertEqual(a2, 30)


if __name__ == '__main__':
    unittest.main()