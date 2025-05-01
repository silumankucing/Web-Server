import cv2
import numpy as np

# Access the webcam (0 is the default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the camera.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)

    # Define a region of interest (ROI) for hand detection
    roi = frame[100:400, 100:400]
    cv2.rectangle(frame, (100, 100), (400, 400), (0, 255, 0), 2)

    # Convert the ROI to HSV and create a mask for skin color
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Apply morphological transformations to clean up the mask
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=4)
    mask = cv2.GaussianBlur(mask, (5, 5), 100)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Find the largest contour (assumed to be the hand)
        max_contour = max(contours, key=cv2.contourArea)

        # Draw the contour
        cv2.drawContours(roi, [max_contour], -1, (255, 0, 0), 2)

        # Find the convex hull and convexity defects
        hull = cv2.convexHull(max_contour, returnPoints=False)
        defects = cv2.convexityDefects(max_contour, hull)

        if defects is not None:
            count_fingers = 0
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(max_contour[s][0])
                end = tuple(max_contour[e][0])
                far = tuple(max_contour[f][0])

                # Calculate the angle between fingers
                a = np.linalg.norm(np.array(start) - np.array(far))
                b = np.linalg.norm(np.array(end) - np.array(far))
                c = np.linalg.norm(np.array(start) - np.array(end))
                angle = np.arccos((a**2 + b**2 - c**2) / (2 * a * b))

                # Count fingers if the angle is less than 90 degrees
                if angle <= np.pi / 2:
                    count_fingers += 1
                    cv2.circle(roi, far, 4, (0, 0, 255), -1)

            # Display the number of fingers
            cv2.putText(frame, f"Fingers: {count_fingers + 1}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frames
    cv2.imshow('Hand Recognition', frame)
    cv2.imshow('Mask', mask)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()