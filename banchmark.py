import time
import random
from memory_manager import MemoryManager
from strategies import FirstFitStrategy, BestFitStrategy, WorstFitStrategy


def run_benchmark(name, strategy_class, iterations=100_000, memory_size=100_000):
    manager = MemoryManager(memory_size, strategy_class())
    allocations = []

    start = time.time()
    for i in range(iterations):
        size = random.randint(1, 500)  # Случайный размер от 1 до 500 KB
        pid, addr = manager.allocate_memory(size)
        if addr != -1:
            allocations.append(pid)

        # Освобождаем старые блоки каждые 1000 итераций
        if i % 1000 == 0 and i > 0 and allocations:
            manager.free_memory(allocations.pop(0))
    end = time.time()

    fragmentation = manager.count_fragmentation()
    success_allocations = len(allocations)
    duration = end - start

    return {
        "strategy": name,
        "duration": duration,
        "success_allocations": success_allocations,
        "fragmentation": fragmentation
    }


def print_benchmark_results(results):
    print("\n📊 Результаты бенчмарка:")
    print("---------------------------------------------------------------")
    print(f"{'Стратегия':<12} | {'Время (с)':<10} | {'Выделений':<10} | {'Фрагментация (%)':<16}")
    print("---------------------------------------------------------------")
    for res in results:
        print(f"{res['strategy']:<12} | {res['duration']:.4f}     | {res['success_allocations']:<10} | {res['fragmentation']:<16}")
    print("---------------------------------------------------------------")


if __name__ == "__main__":
    print("🚀 Запуск расширенного бенчмарка...\n")

    benchmark_results = []

    print("Running: FirstFitStrategy...")
    result = run_benchmark("FirstFit", FirstFitStrategy)
    benchmark_results.append(result)

    print("Running: BestFitStrategy...")
    result = run_benchmark("BestFit", BestFitStrategy)
    benchmark_results.append(result)

    print("Running: WorstFitStrategy...")
    result = run_benchmark("WorstFit", WorstFitStrategy)
    benchmark_results.append(result)

    print_benchmark_results(benchmark_results)
    print("\n✅ Бенчмарк завершён.")