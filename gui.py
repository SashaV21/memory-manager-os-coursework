import tkinter as tk
from tkinter import ttk, messagebox
from memory_manager import MemoryManager
from strategies import FirstFitStrategy, BestFitStrategy, WorstFitStrategy
from tabulate import tabulate


class MemoryManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Manager — GUI")
        self.manager = None

        self.create_widgets()

    def create_widgets(self):
        # === Настройка памяти ===
        config_frame = ttk.LabelFrame(self.root, text="Memory Configuration")
        config_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(config_frame, text="Total Memory Size (KB):").grid(row=0, column=0, padx=5, pady=5)
        self.size_entry = ttk.Entry(config_frame, width=20)
        self.size_entry.insert(0, "100")
        self.size_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(config_frame, text="Allocation Strategy:").grid(row=1, column=0, padx=5, pady=5)
        self.strategy_var = tk.StringVar()
        strategy_combo = ttk.Combobox(config_frame, textvariable=self.strategy_var)
        strategy_combo['values'] = ('FirstFit', 'BestFit', 'WorstFit')
        strategy_combo.current(0)
        strategy_combo.grid(row=1, column=1, padx=5, pady=5)

        start_button = ttk.Button(config_frame, text="Start Simulation", command=self.start_simulation)
        start_button.grid(row=2, columnspan=2, pady=10)

        # === Операции с памятью ===
        action_frame = ttk.LabelFrame(self.root, text="Memory Operations")
        action_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(action_frame, text="Allocate (KB):").grid(row=0, column=0, padx=5, pady=5)
        self.alloc_entry = ttk.Entry(action_frame, width=10)
        self.alloc_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(action_frame, text="Allocate", command=self.allocate_memory).grid(
            row=0, column=2, padx=5, pady=5)

        ttk.Label(action_frame, text="Free Process ID:").grid(row=1, column=0, padx=5, pady=5)
        self.free_entry = ttk.Entry(action_frame, width=10)
        self.free_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(action_frame, text="Free", command=self.free_memory).grid(
            row=1, column=2, padx=5, pady=5)

        # === Вывод состояния памяти ===
        output_frame = ttk.Frame(self.root)
        output_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.output_text = tk.Text(output_frame, wrap="none", height=15, width=80)
        self.output_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.output_text.configure(yscrollcommand=scrollbar.set)

    def start_simulation(self):
        try:
            size = int(self.size_entry.get())
            if size <= 0:
                messagebox.showerror("Error", "Memory size must be a positive number.")
                return
            strategy_name = self.strategy_var.get()
            if strategy_name == "FirstFit":
                strategy = FirstFitStrategy()
            elif strategy_name == "BestFit":
                strategy = BestFitStrategy()
            else:
                strategy = WorstFitStrategy()
            self.manager = MemoryManager(size, strategy)
            self.print_memory_state()
            messagebox.showinfo("Success", f"Started with {size} KB using {strategy_name}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for memory size.")

    def allocate_memory(self):
        if not self.manager:
            messagebox.showwarning("Warning", "Please start the simulation first.")
            return
        try:
            size = int(self.alloc_entry.get())
            if size <= 0:
                messagebox.showerror("Error", "Allocation size must be a positive number.")
                return
            pid, address = self.manager.allocate_memory(size)
            if address != -1:
                self.print_memory_state()
                messagebox.showinfo("Success", f"Process {pid} allocated at address {address}")
            else:
                messagebox.showwarning("Failed", "Not enough memory available.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for allocation.")

    def free_memory(self):
        if not self.manager:
            messagebox.showwarning("Warning", "Please start the simulation first.")
            return
        try:
            pid = int(self.free_entry.get())
            self.manager.free_memory(pid)
            self.print_memory_state()
            messagebox.showinfo("Success", f"Freed memory for process {pid}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid PID.")

    def print_memory_state(self):
        if not self.manager:
            return

        headers = ["Start", "End", "Size", "Status", "Process ID"]
        table_data = []

        for block in self.manager.memory_blocks:
            status = "Free" if block.is_free else "Allocated"
            pid = str(block.process_id) if not block.is_free else "-"
            table_data.append([
                block.start,
                block.start + block.size,
                block.size,
                status,
                pid
            ])

        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, "📊 Current Memory State:\n\n")
        self.output_text.insert(tk.END, tabulate(table_data, headers=headers, tablefmt="grid"))



if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManagerGUI(root)
    root.mainloop()