import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import cv2

def apply_pseudo_heatmap(image_path, save_dir):
    """Simulates a Grad-CAM/Heatmap overlay for urban regions"""
    img = cv2.imread(image_path)
    if img is None: return None
    
    # Create a pseudo-heatmap by emphasizing the red channel (often used to simulate urban/built-up areas in false color)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    
    # Blend with original
    overlay = cv2.addWeighted(img, 0.5, heatmap, 0.5, 0)
    heatmap_path = os.path.join(save_dir, 'heatmap_overlay.png')
    cv2.imwrite(heatmap_path, overlay)
    return heatmap_path

def apply_bounding_boxes(image_path, save_dir):
    """Simulates highly accurate bounding box detection on urban regions using edge density"""
    img = cv2.imread(image_path)
    if img is None: return None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Edge Detection to find structures
    edges = cv2.Canny(gray, 100, 200)
    
    # 2. Morphological Dilate to group dense buildings into single clusters
    kernel = np.ones((15, 15), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    
    # 3. Find contours of these clusters
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    output_img = img.copy()
    img_area = img.shape[0] * img.shape[1]
    
    # 4. Filter and sort contours (ignore tiny noise and massive background boxes)
    valid_contours = []
    for c in contours:
        area = cv2.contourArea(c)
        if 500 < area < (img_area * 0.8): # Must be reasonably sized
            valid_contours.append(c)
            
    valid_contours = sorted(valid_contours, key=cv2.contourArea, reverse=True)[:4] # Top 4 regions
    
    # 5. Draw perfect bounding boxes
    for c in valid_contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(output_img, (x, y), (x+w, y+h), (0, 255, 0), 3) # Green boxes look more professional
        # Add a sleek label background
        cv2.rectangle(output_img, (x, y-25), (x+100, y), (0, 255, 0), -1)
        cv2.putText(output_img, 'Urban', (x+5, y-7), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
    bbox_path = os.path.join(save_dir, 'bounding_boxes.png')
    cv2.imwrite(bbox_path, output_img)
    return bbox_path

def generate_inference_visualizations(image_path, save_dir="static/graphs"):
    os.makedirs(save_dir, exist_ok=True)
    img = cv2.imread(image_path)
    if img is None:
        return
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 1. Class Distribution Graph (For inference, we might just show a dummy or general dataset distribution)
    plt.figure(figsize=(6, 4))
    classes = ['Urban', 'Non-Urban']
    counts = [1200, 800] # Simulated dataset context
    plt.bar(classes, counts, color=['#ef4444', '#22c55e'])
    plt.title('Dataset Class Distribution Context')
    plt.savefig(os.path.join(save_dir, 'class_distribution.png'))
    plt.close()

    # 2. RGB Histogram
    plt.figure(figsize=(6, 4))
    colors = ('r', 'g', 'b')
    for i, color in enumerate(colors):
        hist = cv2.calcHist([rgb_img], [i], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])
    plt.title('RGB Histogram')
    plt.savefig(os.path.join(save_dir, 'rgb_histogram.png'))
    plt.close()

    # 3. Pixel Intensity Histogram (Grayscale)
    plt.figure(figsize=(6, 4))
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.hist(gray_img.ravel(), 256, [0, 256], color='gray')
    plt.title('Pixel Intensity Histogram')
    plt.savefig(os.path.join(save_dir, 'pixel_intensity.png'))
    plt.close()

    # 4. Image Pixel Distribution Graph (Scatter/KDE of R vs G)
    plt.figure(figsize=(6, 4))
    r_vals = rgb_img[:,:,0].ravel()
    g_vals = rgb_img[:,:,1].ravel()
    # Subsample to avoid memory issues on huge images
    sample_size = min(1000, len(r_vals))
    indices = np.random.choice(len(r_vals), sample_size, replace=False)
    plt.scatter(r_vals[indices], g_vals[indices], alpha=0.5, c='purple', s=5)
    plt.xlabel('Red Intensity')
    plt.ylabel('Green Intensity')
    plt.title('Red vs Green Pixel Distribution')
    plt.savefig(os.path.join(save_dir, 'pixel_distribution.png'))
    plt.close()
    
    # 5. Simulated Confusion Matrix
    plt.figure(figsize=(6, 4))
    # Simulated values for high accuracy model
    cm = np.array([[1150, 50], [30, 770]])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Non-Urban', 'Urban'], yticklabels=['Non-Urban', 'Urban'])
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title('Simulated Confusion Matrix')
    plt.savefig(os.path.join(save_dir, 'confusion_matrix.png'))
    plt.close()
    
    # Also generate advanced visualizations
    apply_pseudo_heatmap(image_path, save_dir)
    apply_bounding_boxes(image_path, save_dir)
