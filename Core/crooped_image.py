import cv2
import imutils
import numpy as np


#async def cropped_plate(img_original):
def cropped_plate(img_original):
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
        #print("Longitud contornos: ",len(approx))
        if len(approx) == 4:
            location = approx
            thereIsLocation = True
            break

    #print(location)

    if len(location) == 0:
        return []

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

    return cropped_image
