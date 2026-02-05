/**
 * Updates the UI with the given prediction data.
 * @param {Object} data - The prediction data.
 * @param {string} data.prediction - The predicted class label.
 * @param {number} data.confidence - The confidence score (0 to 1).
 */
export function updatePredictionUI({
    prediction,
    confidence
}) {
    const predictionLabel = document.getElementById('prediction-label');
    const confidenceBar = document.getElementById('confidence-bar');
    const confidencePercent = document.getElementById('confidence-percent');
    const statusIndicator = document.getElementById('status-indicator');
    const errorMessage = document.getElementById('error-message');

    if (prediction && prediction !== 'Error') {
        predictionLabel.textContent = prediction;
        const confidenceValue = (confidence * 100).toFixed(2);
        confidenceBar.style.width = `${confidenceValue}%`;
        confidencePercent.textContent = `${confidenceValue}%`;
        statusIndicator.classList.remove('bg-red-500', 'bg-gray-500', 'animate-pulse');
        statusIndicator.classList.add('bg-green-500');
        errorMessage.classList.add('hidden');

    } else {
        predictionLabel.textContent = 'Error fetching prediction';
        confidenceBar.style.width = '0%';
        confidencePercent.textContent = '0%';
        statusIndicator.classList.remove('bg-green-500', 'bg-gray-500', 'animate-pulse');
        statusIndicator.classList.add('bg-red-500');
        showError('Failed to get prediction from server.');

    }
}


/**
 * Displays an error message in the UI.
 * @param {string} message - The error message to display.
 */
export function showError(message) {
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
}