import cv2
import cv2.aruco as aruco

# Define the dictionary and marker size
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
marker_size = 200

# Create a video capture object
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Start the video capture loop
while True:
    # Read a frame from the video capture
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the markers in the grayscale image
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(dictionary, parameters)
    corners, ids, rejected = detector.detectMarkers(gray)

    # If at least one marker was detected
    if ids is not None:
        # Draw the detected markers on the frame
        aruco.drawDetectedMarkers(frame, corners, ids)

        # Get the center of the first detected marker
        center_x = int((corners[0][0][0][0] + corners[0][0][2][0]) / 2)
        center_y = int((corners[0][0][0][1] + corners[0][0][2][1]) / 2)

        # Draw a circle at the center of the marker
        cv2.circle(frame, (center_x, center_y), 2, (0, 255, 0), -1)


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
