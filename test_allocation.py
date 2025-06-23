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
        manager.allocate_memory(40)  # Остаётся [40–100)
        manager.allocate_memory(20)  # Остаётся [60–100)
        p3, a3 = manager.allocate_memory(10)
        self.assertEqual(a3, 60)

    def test_worst_fit_largest_block(self):
        manager = MemoryManager(100, WorstFitStrategy())
        p1, a1 = manager.allocate_memory(30)
        p2, a2 = manager.allocate_memory(20)
        self.assertEqual(a1, 0)
        self.assertEqual(a2, 30)  # После 30 KB остаётся блок 70 KB, из которого и берём

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
        manager.allocate_memory(29)  # Остается 1 KB
        pid, addr = manager.allocate_memory(1)
        self.assertEqual(addr, 99)

    def test_worst_fit_with_multiple_blocks(self):
        manager = MemoryManager(200, WorstFitStrategy())
        p1, a1 = manager.allocate_memory(50)  # Блок 0–50
        p2, a2 = manager.allocate_memory(30)  # Блок 50–80
        p3, a3 = manager.allocate_memory(60)  # Блок 80–140
        manager.free_memory(p2)
        manager.free_memory(p1)
        p4, a4 = manager.allocate_memory(70)  # Выбираем худший (наибольший) — блок 0–50 + 50–80 → объединён в 0–80
        self.assertEqual(a4, 0)  # Теперь должен начаться с 0

    def test_strategy_change_runtime(self):
        manager = MemoryManager(100, FirstFitStrategy())
        manager.allocate_memory(30)
        manager.set_strategy(BestFitStrategy())
        p2, a2 = manager.allocate_memory(20)
        self.assertEqual(a2, 30)


if __name__ == '__main__':
    unittest.main()