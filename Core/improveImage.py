# External libraries used for
# Image IO
from PIL import Image
import easyocr

# Morphological filtering
from skimage.morphology import opening
from skimage.morphology import disk

# Data handling
import numpy as np

# Connected component filtering
import cv2

black = 0
white = 255
threshold = 127

# Open input image in grayscale mode and get its pixels.
#img = Image.open("C://Users/Diego Gonzalez/Downloads/recorte4.JPG").convert("LA")
img = Image.open("C:/Users/Diego Gonzalez/Desktop/Tesis/Tesis/bordes/detection_2022-01-22-23_48_10.jpg").convert("LA")
pixels = np.array(img)[:,:,0]

# Remove pixels above threshold
pixels[pixels > threshold] = white
pixels[pixels < threshold] = black


# Morphological opening
blobSize = 1 # Select the maximum radius of the blobs you would like to remove
structureElement = disk(blobSize)  # you can define different shapes, here we take a disk shape
# We need to invert the image such that black is background and white foreground to perform the opening
pixels = np.invert(opening(np.invert(pixels), structureElement))


# Create and save new image.
newImg2 = Image.fromarray(pixels).convert('RGB')
newImg2.save("newImageImprove5.PNG")

# Find the connected components (black objects in your image)
# Because the function searches for white connected components on a black background, we need to invert the image
nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(np.invert(pixels), connectivity=8)

# For every connected component in your image, you can obtain the number of pixels from the stats variable in the last
# column. We remove the first entry from sizes, because this is the entry of the background connected component
sizes = stats[1:,-1]
nb_components -= 1

# Define the minimum size (number of pixels) a component should consist of
minimum_size = 100

# Create a new image
newPixels = np.ones(pixels.shape)*255

# Iterate over all components in the image, only keep the components larger than minimum size
for i in range(1, nb_components):
    if sizes[i] > minimum_size:
        newPixels[output == i+1] = 0

# Create and save new image.
newImg = Image.fromarray(newPixels).convert('RGB')
newImg.save("newImageImprove6.PNG")

img_original = np.array(newImg)
img_original1 = np.array(newImg2)

reader = easyocr.Reader(['en'])
result = reader.readtext(img_original, text_threshold=0.7)

#print(result)

placa = []

for i in range(len(result)):
    placa.append(result[i][1].upper())
print(placa)