import matplotlib.pyplot as plt
import os

def visualize_data(history, save_dir="static/graphs"):
    """
    Creates 4 graphs for data visualization:
    1. Training & Validation Accuracy
    2. Training & Validation Loss
    3. Class Distribution (Dummy for now)
    4. Confusion Matrix (Dummy for now)
    """
    os.makedirs(save_dir, exist_ok=True)
    
    # 1. Accuracy Graph
    plt.figure(figsize=(8, 6))
    plt.plot(history.history.get('accuracy', [0, 1]), label='Train Accuracy')
    plt.plot(history.history.get('val_accuracy', [0, 1]), label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend()
    plt.savefig(os.path.join(save_dir, 'accuracy_graph.png'))
    plt.close()
    
    # 2. Loss Graph
    plt.figure(figsize=(8, 6))
    plt.plot(history.history.get('loss', [1, 0]), label='Train Loss')
    plt.plot(history.history.get('val_loss', [1, 0]), label='Validation Loss')
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend()
    plt.savefig(os.path.join(save_dir, 'loss_graph.png'))
    plt.close()
    
    # 3. Class Distribution
    plt.figure(figsize=(8, 6))
    classes = ['No Urban Growth', 'Urban Growth Detected']
    counts = [500, 300] # Dummy data
    plt.bar(classes, counts, color=['green', 'red'])
    plt.title('Class Distribution in Dataset')
    plt.savefig(os.path.join(save_dir, 'class_distribution.png'))
    plt.close()
    
    # 4. Dummy Confusion Matrix
    import seaborn as sns
    import numpy as np
    plt.figure(figsize=(8, 6))
    cm = np.array([[450, 50], [40, 260]])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig(os.path.join(save_dir, 'confusion_matrix.png'))
    plt.close()
    
    print(f"Visualizations saved to {save_dir}")
