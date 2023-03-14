import cv2
import cv2.aruco as aruco
import numpy as np

# Define the dictionary to use
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

# Define the ID and size of the marker to generate
marker_id = 20
marker_size = 200

# Generate the marker image
marker_image = aruco.generateImageMarker(dictionary, marker_id, marker_size)

# Save the marker image to disk
cv2.imwrite("marker.jpg", marker_image)

print("Marker saved as marker.jpg")
