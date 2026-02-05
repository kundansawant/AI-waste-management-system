const API_URL = "http://localhost:8000";

// Change these to match YOUR dataset classes
const CLASS_NAMES = [
    "Cardboard",
    "Food Organics",
    "Glass",
    "Metal",
    "Miscellaneous Trash",
    "Paper",
    "Plastic",
    "Textile Trash",
    "Vegetation"
];

/**
 * Sends an image blob to the backend for prediction.
 */
export async function fetchPrediction(imageBlob) {
    const formData = new FormData();
    formData.append('file', imageBlob, 'frame.jpg');

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
        }

        const backendData = await response.json();

        // Convert backend format to UI format
        const predictionLabel = CLASS_NAMES[backendData.class_id] || "Unknown";

        return {
            prediction: predictionLabel,
            confidence: backendData.confidence
        };

    } catch (error) {
        console.error("Failed to fetch prediction:", error);
        return {
            prediction: "Error",
            confidence: 0
        };
    }
}
