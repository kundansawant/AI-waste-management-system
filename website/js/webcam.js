/**
 * Sets up the webcam and streams it to the provided video element.
 * @param {HTMLVideoElement} videoElement - The video element to stream the webcam to.
 * @returns {Promise<boolean>} A promise that resolves to true if setup is successful, false otherwise.
 */
export async function setupWebcam(videoElement) {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error("Webcam not supported by this browser.");
    }
    const stream = await navigator.mediaDevices.getUserMedia({
        video: true
    });
    videoElement.srcObject = stream;
    await videoElement.play();
    return true;
}

/**
 * Captures a single frame from a video element and returns it as a Blob.
 * @param {HTMLVideoElement} videoElement - The video element to capture a frame from.
 * @returns {Promise<Blob>} A promise that resolves with the captured frame as a JPEG Blob.
 */
export function captureFrame(videoElement) {
    return new Promise((resolve, reject) => {
        const canvas = document.createElement('canvas');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(blob => {
            if (blob) {
                resolve(blob);
            } else {
                reject(new Error('Failed to create blob from canvas.'));
            }
        }, 'image/jpeg');
    });
}