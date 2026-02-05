import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import os

# ----------------------------
# 1. Dataset Path
# ----------------------------
dataset_path = r"C:/Users/admin/Documents/waste classifier/datasets"



img_size = 224
batch_size = 32

# ----------------------------
# 2. Image Generators
# ----------------------------
train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    validation_split=0.2,
    rotation_range=20,
    zoom_range=0.2,
    shear_range=0.2,
    horizontal_flip=True
)

train_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode="categorical",
    subset="training"
)

val_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode="categorical",
    subset="validation"
)

num_classes = len(train_generator.class_indices)
print("Classes:", train_generator.class_indices)

# ----------------------------
# 3. Load MobileNetV2 Base
# ----------------------------
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(img_size, img_size, 3)
)

base_model.trainable = False   # Freeze base model

# ----------------------------
# 4. Add Custom Layers
# ----------------------------
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation="relu")(x)
x = Dropout(0.3)(x)
predictions = Dense(num_classes, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=predictions)

# ----------------------------
# 5. Compile Model
# ----------------------------
model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# ----------------------------
# 6. Train Model
# ----------------------------
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=30
)

# ------------------------------
# Save the trained model
# ------------------------------
model.save(r"C:\Users\admin\Documents\waste classifier\models\waste_model.h5")
print("Model saved successfully at: C:\\Users\\admin\\Documents\\waste classifier\\models\\waste_model.h5")


