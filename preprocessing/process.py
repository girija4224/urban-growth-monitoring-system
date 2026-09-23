import cv2
import numpy as np

def resize_image(image, size=(224, 224)):
    return cv2.resize(image, size)

def bgr_to_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def normalize_image(image):
    return image.astype('float32') / 255.0

def full_preprocess(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found")
        
    orig_shape = img.shape
    resized = resize_image(img)
    rgb = bgr_to_rgb(resized)
    normalized = normalize_image(rgb)
    
    return {
        "original_shape": orig_shape,
        "resized_shape": resized.shape,
        "processed_array": normalized,
        "rgb_array": rgb # used for visualization
    }
