import cv2
import numpy as np
import os
from sklearn.model_selection import train_test_split

def load_data(data_dir):
    """
    Simulated data collection from a directory.
    Returns dummy data if directory is empty or not provided.
    """
    images = []
    labels = []
    
    # In a real scenario, this would read from data_dir
    # For now, we return dummy arrays to allow the pipeline to run
    print(f"Loading data from {data_dir}...")
    
    # Simulating 100 images of size 224x224x3
    dummy_images = np.random.randint(0, 255, (100, 224, 224, 3), dtype=np.uint8)
    dummy_labels = np.random.randint(0, 2, (100,))
    
    return dummy_images, dummy_labels

def preprocess_image(image, target_size=(224, 224)):
    """
    Preprocess a single image:
    1. Resize
    2. Convert BGR to RGB (OpenCV loads as BGR)
    3. Normalize to [0, 1]
    """
    # Resize
    resized = cv2.resize(image, target_size)
    
    # BGR to RGB conversion
    rgb_image = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    
    # Normalize
    normalized = rgb_image.astype('float32') / 255.0
    
    return normalized

def preprocess_dataset(images, labels):
    """
    Preprocess entire dataset and split into train/test
    """
    processed_images = np.array([preprocess_image(img) for img in images])
    
    X_train, X_test, y_train, y_test = train_test_split(
        processed_images, labels, test_size=0.2, random_state=42
    )
    
    return X_train, X_test, y_train, y_test
