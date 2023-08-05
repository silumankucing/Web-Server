import cv2
import numpy as np

face_identifier = cv2.CascadeClassifier('src/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture('src/submarine.mp4')

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    human_faces = face_identifier.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in human_faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    if ret == True:
        cv2.imshow('Image Recognition from Video',frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else: 
        break

cap.release()
cv2.destroyAllWindows()