from memory_manager import MemoryManager
from strategies import FirstFitStrategy, BestFitStrategy, WorstFitStrategy
from tabulate import tabulate

def print_memory_table(manager):
    headers = ["Start", "End", "Size", "Status", "Process ID"]
    table = []

    for block in manager.memory_blocks:
        status = "Free" if block.is_free else f"P{block.process_id}"
        table.append([
            block.start,
            block.start + block.size,
            block.size,
            status
        ])

    print("\n📊 Current Memory State:")
    print(tabulate(table, headers=headers, tablefmt="grid"))
    print()

def main():
    print("=== Memory Manager ===")
    total_size = int(input("Enter total memory size (in KB): "))

    print("\nChoose allocation strategy:")
    print("1. First Fit")
    print("2. Best Fit")
    print("3. Worst Fit")
    choice = input("Enter choice (1/2/3): ").strip()

    strategy_map = {
        '1': FirstFitStrategy(),
        '2': BestFitStrategy(),
        '3': WorstFitStrategy()
    }

    strategy = strategy_map.get(choice, FirstFitStrategy())
    manager = MemoryManager(total_size, strategy)

    while True:
        print("\n===== Menu =====")
        print("1. Allocate memory")
        print("2. Free memory")
        print("3. Change strategy")
        print("4. Print memory state")
        print("5. Exit")

        option = input("Enter your choice: ")

        if option == '1':
            try:
                size = int(input("Enter size to allocate (KB): "))
                pid, addr = manager.allocate_memory(size)
                if addr != -1:
                    print(f"✅ Process {pid} allocated at address {addr}")
                else:
                    print("❌ Not enough memory.")
            except ValueError:
                print("❗ Invalid input.")

        elif option == '2':
            try:
                pid = int(input("Enter PID to free: "))
                manager.free_memory(pid)
                print(f"🔓 Freed memory for process {pid}")
            except ValueError:
                print("❗ Invalid input.")

        elif option == '3':
            print("Change to:")
            print("1. First Fit")
            print("2. Best Fit")
            print("3. Worst Fit")
            new_choice = input("Enter choice: ")
            manager.set_strategy(strategy_map[new_choice])
            print("🔄 Strategy changed.")

        elif option == '4':
            print_memory_table(manager)

        elif option == '5':
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()