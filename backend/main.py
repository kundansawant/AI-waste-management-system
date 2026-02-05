from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
import cv2
import os

# --- Model and App Initialization ---

# Define the relative path to the model for local execution
# This path is relative to the project's root directory
MODEL_PATH = "backend/waste_model.h5"

# Initialize the FastAPI app
app = FastAPI()
app.state.model = None

@app.on_event("startup")
def load_model():
    """
    Load the model during startup.
    """
    if os.path.exists(MODEL_PATH):
        app.state.model = tf.keras.models.load_model(MODEL_PATH)
        print("--- Model loaded successfully ---")
    else:
        print(f"--- ERROR: Model file not found at {MODEL_PATH} ---")
        print(f"--- Current working directory: {os.getcwd()} ---")


# --- CORS Configuration ---

# Origins for local development, including VS Code Live Server
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Image Preprocessing ---

IMG_SIZE = 224

def preprocess_image(image_bytes):
    """
    Preprocesses the image for the model.
    """
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    image = np.expand_dims(image, axis=0)
    image = image / 255.0
    return image

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the Waste Classification API"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not app.state.model:
        return {"error": "Model is not loaded or failed to load. Please check terminal for errors."}

    image_bytes = await file.read()
    processed_image = preprocess_image(image_bytes)
    prediction = app.state.model.predict(processed_image)
    
    class_id = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    return {
        "class_id": class_id,
        "confidence": confidence
    }