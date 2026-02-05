import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cam 0 not working. Trying Cam 1...")
    cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Cam 1 not working. Trying Cam 2...")
    cap = cv2.VideoCapture(2)

if not cap.isOpened():
    print("No webcam found.")
    exit()

print("Webcam found. Opening window...")

while True:
    ret, frame = cap.read()
    cv2.imshow("Test Webcam", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
