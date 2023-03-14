import cv2

# Create a video capture object
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

point1 = [200,200]
point2 = [100, 50]

# Start the video capture loop
while True:
    # Read a frame from the video capture
    ret, frame = cap.read()

    cv2.line(frame, point1, point2, (0, 255, 255), 3)

    # Display the frame
    cv2.imshow('Frame', frame)

    # Wait for a key press
    key = cv2.waitKey(1)

    # If the 'q' key is pressed, break the loop
    if key == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
