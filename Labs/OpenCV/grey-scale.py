import cv2

# Load an image from file
image = cv2.imread('src/ava.jpeg')

# Display the original image
cv2.imshow('Original Image', image)

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('Grayscale Image', gray_image)

# Apply Gaussian Blur
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
cv2.imshow('Blurred Image', blurred_image)

# Perform edge detection using Canny
edges = cv2.Canny(blurred_image, 50, 150)
cv2.imshow('Edge Detection', edges)

# Wait for a key press and close all windows
cv2.waitKey(0)
cv2.destroyAllWindows()