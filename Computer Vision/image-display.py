import cv2
from matplotlib import pyplot as plt

img = cv2.imread('src/img.jpg',cv2.IMREAD_GRAYSCALE)
cv2.imshow('Open Image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()