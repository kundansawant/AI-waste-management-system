import {
    fetchPrediction
} from './js/prediction.js';
import {
    updatePredictionUI,
    showError
} from './js/ui.js';
import {
    setupWebcam,
    captureFrame
} from './js/webcam.js';

const PREDICTION_INTERVAL = 2000; // milliseconds

/**
 * Main application logic.
 */
async function main() {
    const webcamElement = document.getElementById('webcam-feed');

    try {
        await setupWebcam(webcamElement);
    } catch (error) {
        console.error(error);
        showError('Could not access webcam. Please ensure it is enabled and permissions are granted.');
        return;
    }

    // Start polling for predictions
    setInterval(async () => {
        try {
            const imageBlob = await captureFrame(webcamElement);
            const predictionData = await fetchPrediction(imageBlob);
            updatePredictionUI(predictionData);
        } catch (error) {
            console.error('Error during prediction polling:', error);
            showError('An error occurred while making a prediction.');
            updatePredictionUI({
                prediction: 'Error',
                confidence: 0
            });
        }
    }, PREDICTION_INTERVAL);
}

// Run the main application
main();