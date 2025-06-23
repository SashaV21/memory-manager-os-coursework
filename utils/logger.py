import logging

logging.basicConfig(
    filename='memory_usage.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def log_allocation(strategy, pid, size, address):
    logging.info(f"[{strategy}] Process {pid} allocated {size} KB at {address}")

def log_failed_allocation(strategy, size):
    logging.warning(f"[{strategy}] Failed to allocate {size} KB")

def log_defragmentation():
    logging.info("Defragmentation completed")