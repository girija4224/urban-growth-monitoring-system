import os
from .data_processing import load_data, preprocess_dataset
from .models import get_model
from .visualization import visualize_data

def train_pipeline(model_type, data_dir="data", model_save_dir="static/models"):
    """
    Simulates the entire training pipeline:
    1. Data Collection
    2. Preprocessing
    3. Model Creation
    4. Training
    5. Visualization
    6. Export
    """
    print(f"Starting training pipeline for {model_type}...")
    os.makedirs(model_save_dir, exist_ok=True)
    
    # 1. & 2. Data Collection & Preprocessing
    images, labels = load_data(data_dir)
    X_train, X_test, y_train, y_test = preprocess_dataset(images, labels)
    
    # 3. Create Model
    model = get_model(model_name=model_type, input_shape=(224, 224, 3), num_classes=1)
    
    # 4. Train Model
    print("Training the model...")
    # Using small epochs/batch_size for simulation speed
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=3,
        batch_size=32,
        verbose=1
    )
    
    # 5. Data Visualization (4 graphs)
    print("Generating visualizations...")
    visualize_data(history)
    
    # 6. Export Model
    model_filename = f"{model_type.replace(' ', '_')}.h5"
    model_path = os.path.join(model_save_dir, model_filename)
    model.save(model_path)
    print(f"Model saved to {model_path}")
    
    # Optional: Save architecture as JSON
    json_config = model.to_json()
    with open(os.path.join(model_save_dir, f"{model_type.replace(' ', '_')}.json"), 'w') as json_file:
        json_file.write(json_config)
        
    return model_path
