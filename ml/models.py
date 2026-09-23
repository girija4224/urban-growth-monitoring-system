import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.applications import VGG16, VGG19, ResNet50

def get_model(model_name="CNN DENSE", input_shape=(224, 224, 3), num_classes=1):
    """
    Returns an empty (untrained on our specific data) DL model based on the selection.
    """
    if model_name == "CNN DENSE":
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
            MaxPooling2D(2, 2),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Flatten(),
            Dense(512, activation='relu'),
            Dropout(0.5),
            Dense(num_classes, activation='sigmoid' if num_classes == 1 else 'softmax')
        ])
        
    elif model_name == "CNN VGG16":
        base_model = VGG16(weights='imagenet', include_top=False, input_shape=input_shape)
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(512, activation='relu')(x)
        predictions = Dense(num_classes, activation='sigmoid' if num_classes == 1 else 'softmax')(x)
        model = Model(inputs=base_model.input, outputs=predictions)
        
    elif model_name == "CNN VGG19":
        base_model = VGG19(weights='imagenet', include_top=False, input_shape=input_shape)
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(512, activation='relu')(x)
        predictions = Dense(num_classes, activation='sigmoid' if num_classes == 1 else 'softmax')(x)
        model = Model(inputs=base_model.input, outputs=predictions)
        
    elif model_name == "RESNET":
        base_model = ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(512, activation='relu')(x)
        predictions = Dense(num_classes, activation='sigmoid' if num_classes == 1 else 'softmax')(x)
        model = Model(inputs=base_model.input, outputs=predictions)
        
    else:
        raise ValueError("Invalid model name")
        
    model.compile(optimizer='adam', 
                  loss='binary_crossentropy' if num_classes == 1 else 'categorical_crossentropy', 
                  metrics=['accuracy'])
    
    return model
