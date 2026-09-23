import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.applications import VGG16, VGG19, ResNet50

def build_model(model_name="CNN"):
    input_shape = (224, 224, 3)
    if model_name == "CNN":
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
            MaxPooling2D(2, 2),
            Flatten(),
            Dense(128, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
    elif model_name == "CNN + Dense":
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
            MaxPooling2D(2, 2),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Flatten(),
            Dense(512, activation='relu'),
            Dropout(0.5),
            Dense(256, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
    elif model_name == "VGG16":
        base = VGG16(weights='imagenet', include_top=False, input_shape=input_shape)
        x = GlobalAveragePooling2D()(base.output)
        x = Dense(256, activation='relu')(x)
        out = Dense(1, activation='sigmoid')(x)
        model = Model(inputs=base.input, outputs=out)
    elif model_name == "VGG19":
        base = VGG19(weights='imagenet', include_top=False, input_shape=input_shape)
        x = GlobalAveragePooling2D()(base.output)
        x = Dense(256, activation='relu')(x)
        out = Dense(1, activation='sigmoid')(x)
        model = Model(inputs=base.input, outputs=out)
    elif model_name == "ResNet50":
        base = ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)
        x = GlobalAveragePooling2D()(base.output)
        x = Dense(256, activation='relu')(x)
        out = Dense(1, activation='sigmoid')(x)
        model = Model(inputs=base.input, outputs=out)
    else:
        raise ValueError("Invalid model name")
        
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model
