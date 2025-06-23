import matplotlib.pyplot as plt
import matplotlib.patches as patches

def visualize_memory(manager):
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.set_xlim(0, manager.memory_blocks[-1].start + manager.memory_blocks[-1].size)
    ax.set_ylim(0, 1)
    ax.axis('off')

    y = 0.1
    height = 0.8

    for block in manager.memory_blocks:
        color = 'lightgray' if block.is_free else 'skyblue'
        rect = patches.Rectangle((block.start, y), block.size, height, edgecolor='black', facecolor=color)
        ax.add_patch(rect)
        label = f"P{block.process_id}" if not block.is_free else "Free"
        plt.text(block.start + block.size / 2, y + height / 2, label, ha='center', va='center', fontsize=8)

    plt.draw()
    plt.pause(1)
    plt.cla()