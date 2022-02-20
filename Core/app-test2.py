import cv2
import matplotlib.pyplot as plt
import imutils
import numpy as np
from crooped_image import cropped_plate
#lectura de la imagen
img_original = cv2.imread('bordes/detection_2022-01-23-01_02_15.jpg')

img_grayScale = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)  # Gray Scale
img_noiseReduction = cv2.bilateralFilter(img_grayScale, 11, 17, 17)  # Noise reduction
img_Canny = cv2.Canny(img_noiseReduction, 30, 200)  # Put image in black backrgoung with white lines

keypoints = cv2.findContours(img_Canny.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    # Saca la posicion donde se enuentra el rectangulo
thereIsLocation = False
location = []
for contour in contours:
    approx = cv2.approxPolyDP(contour, 10, True)
    #print(len(approx))
    if len(approx) == 4:
       location = approx
       thereIsLocation = True
    break

    #print(location)

if len(location) == 0:
    pass

cropped_image = img_noiseReduction[:]

if thereIsLocation:
    mask = np.zeros(img_Canny.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img_noiseReduction, img_noiseReduction, mask=mask)

    # CORTAR IMAGEN
    (x, y) = np.where(mask == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = img_noiseReduction[x1:x2 + 1, y1:y2 + 1]
    pass

#imprimir su forma
#img2 = cropped_plate(img)
plt.imshow(cropped_image)