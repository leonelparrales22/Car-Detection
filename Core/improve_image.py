import cv2
from scipy.ndimage import gaussian_filter
import numpy as np


def ecualizacion(img):
    img_to_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_to_yuv[:, :, 0] = cv2.equalizeHist(img_to_yuv[:, :, 0])
    hist_equalization_result = cv2.cvtColor(img_to_yuv, cv2.COLOR_YUV2BGR)
    return hist_equalization_result


def filtro_gauissiano(img, sigma_value=0.2):
    result = gaussian_filter(img, sigma=sigma_value)  # sigma = kernel
    return result


# Debe de estar en escala de gris
def filtro_otsu(img):
    ret2, th2 = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th2


def erosion(img):
    kernel = np.ones((2, 2), np.uint8)
    erosion = cv2.erode(img, kernel, iterations=1)
    return erosion


def dilatacion(img):
    kernel = np.ones((2, 2), np.uint8)
    dilatacion = cv2.dilate(img, kernel, iterations=1)
    return dilatacion
