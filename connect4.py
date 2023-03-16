import cv2
import cv2.aruco as aruco

# Utility
def getkey(thelist, value):
    for i, val in enumerate(thelist):
        if val == value:
            return i
    return None

def getpoint(key, corners):
    return [int(corners[key][0][0][0]), int(corners[key][0][0][1])]


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

        listids = list(ids)

        for i in range(20,24,1):

            if i in ids and i-1 in ids:
                key = getkey(listids, i)
                otherkey = getkey(listids, i-1)
                cv2.line(frame, getpoint(key, corners), getpoint(otherkey, corners), (0,0,255), 3)

            elif i in ids and i+3 in ids:
                key = getkey(listids, i)
                otherkey = getkey(listids, i+3)
                cv2.line(frame, getpoint(key, corners), getpoint(otherkey, corners), (0,0,255), 3)
            
            if i== 20 and 21 in ids and 22 in ids and 23 in ids:
                cord21 = getpoint(getkey(listids, 21), corners)
                cord22 = getpoint(getkey(listids, 22), corners)
                cord23 = getpoint(getkey(listids, 23), corners)

                cord20 = [cord23[0]+cord21[0]-cord22[0], cord21[1]+cord23[1]-cord22[1]]

                cv2.circle(frame, cord20, 2, (255, 0, 0), 4)
            




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