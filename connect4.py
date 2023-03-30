import cv2
import cv2.aruco as aruco

# Utility
def getkey(thelist, value):
    for i, val in enumerate(thelist):
        if val == value:
            return i
    return None

def getpoint(key, corners, cornernumber):
    return [int(corners[key][0][cornernumber][0]), int(corners[key][0][cornernumber][1])]

def findpitch(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    if x2 - x1 == 0:
        return 100000000
    else:
        return (y2 - y1) / (x2 - x1)

cornerdict = {}

def lineintersection(coord1, pitch1, coord2, pitch2):
    x1, y1 = coord1
    x2, y2 = coord2
    m1 = pitch1
    m2 = pitch2

    if m1 == m2:
        return None

    pre1 = m1*x1
    pre2 = m2*y1
    f = pre1-x2-pre2+y2
    r = m1 - m2
    x = f / r

    pre1 = x-x1
    pre2 = m1 * pre1
    y = pre2 + x2

    return (int(x), int(y))

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

        for i in [20,21,22,23]:
            
            if len(ids) == 3 and len(cornerdict) == 4 and i not in ids:

                vid  = i+1 if i in [20,22] else i-1
                hid = 22 if i == 21 else 21 if i == 22 else 23 if i == 20 else 20

                point = lineintersection(cornerdict[vid]["main"], cornerdict[vid]["pv"],
                                         cornerdict[hid]["main"], cornerdict[hid]["ph"])
                cv2.circle(frame, point, 3, (0,0,255), 6)
                
            elif i in ids:

                if i-1 in ids:
                    key = getkey(ids, i)
                    otherkey = getkey(ids, i-1)
                    cv2.line(frame, getpoint(key, corners, 0), getpoint(otherkey, corners, 0), (0,0,255), 3)
                elif i+3 in ids:
                    key = getkey(ids, i)
                    otherkey = getkey(ids, i+3)
                    cv2.line(frame, getpoint(key, corners, 0), getpoint(otherkey, corners, 0), (0,0,255), 3)
                
                cornerdict[i] = {"main": getpoint(getkey(ids,i),corners, 0), 
                                "v": getpoint(getkey(ids,i),corners, 3 if i%2==0 else 1), 
                                "h": getpoint(getkey(ids,i),corners, 1 if i%2==0 else 3)}
                
                cornerdict[i]["pv"] = findpitch(cornerdict[i]["main"], cornerdict[i]["v"])
                cornerdict[i]["ph"] = findpitch(cornerdict[i]["main"], cornerdict[i]["h"])



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