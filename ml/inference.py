import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import os
from .data_processing import preprocess_image

def predict_image(image_path, model_path):
    """
    1. Loads the saved model (.h5)
    2. Loads and preprocesses the input image
    3. Returns prediction
    """
    if not os.path.exists(model_path):
        # Fallback for dummy simulation if model doesn't exist
        import random
        return "Urban Growth Detected" if random.random() > 0.5 else "No Urban Growth"
        
    print(f"Loading model from {model_path}...")
    model = load_model(model_path)
    
    print(f"Processing image {image_path}...")
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Invalid image file.")
        
    processed_img = preprocess_image(image)
    # Add batch dimension
    input_batch = np.expand_dims(processed_img, axis=0)
    
    # Predict
    prediction = model.predict(input_batch)
    
    # Binary classification assuming sigmoid output
    if prediction[0][0] > 0.5:
        return "Urban Growth Detected"
    else:
        return "No Urban Growth"
