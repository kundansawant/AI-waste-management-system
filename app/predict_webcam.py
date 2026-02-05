import cv2
import numpy as np
from tensorflow.keras.models import load_model

print("Step 1: Imports loaded.")

# ------------------------------
# Load your trained model
# ------------------------------
print("Step 2: Loading model...")
model = load_model(r"models/waste_model.h5")
print("Step 2: Model loaded successfully.")

# ------------------------------
# Start webcam
# ------------------------------
print("Step 3: Initializing webcam...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Step 3: Webcam initialization complete.")

while True:
    print("Loop running...")   # DEBUG PRINT

    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    display_frame = frame.copy()
    resized = cv2.resize(frame, (224, 224))
    normalized = resized.astype("float32") / 255.0
    expanded = np.expand_dims(normalized, axis=0)

    predictions = model.predict(expanded)
    class_index = np.argmax(predictions)

    class_names = [
        "Cardboard",
        "Food Organics",
        "Glass",
        "Metal",
        "Miscellaneous Trash",
        "Paper",
        "Plastic",
        "Textile Trash",
        "Vegetation"
    ]

    label = class_names[class_index]
    confidence = predictions[0][class_index] * 100

    text = f"{label} ({confidence:.1f}%)"
    cv2.putText(display_frame, text, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow("Waste Classifier - Real Time", display_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
