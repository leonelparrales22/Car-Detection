## LIBRARIES
import threading
from datetime import datetime

import cv2
import asyncio
from crooped_image import cropped_plate
from print_picture import print_photo
from ocr import ocr_plate
from improve_image import filtro_otsu, dilatacion, erosion, ecualizacion, filtro_gauissiano

## GRABAR IMAGEN
async def guardarImagen(frames):
    cropped_image = await cropped_plate(frames[700:800, 100:500])
    if len(cropped_image)>0:
        cv2.imshow('DiegoGonzalez', cropped_image)
        placa = await ocr_plate(cropped_image)
        if len(placa) > 1:
            nameFile = 'bdd/detection_' + datetime.today().strftime('%Y-%m-%d-%H_%M_%S') + '.jpg'
            cv2.imwrite(nameFile, frames)
        print("La placa es: ", placa)

## LEER EL VIDEO

# capture frames from a video
cap = cv2.VideoCapture('videos/VIDEO-PRUEBA-3.mp4')
#cap = cv2.VideoCapture('videos/video-17min-6am.mp4')
#cap = cv2.VideoCapture('videos/video-corto-9am.mp4')

async def main (cap):
    # loop runs if capturing has been initialized.
    while True:
        try:
            # cropped_image = await cropped_plate(frames[700:800, 100:500]) #frames[y,x]
            # cropped_image = await cropped_plate(frames[300:800, 100:600])
            cropped_image = await cropped_plate(frames[500:800, 34:600])
            print(len(cropped_image))
            if 32 <= len(cropped_image) <= 37:
                cv2.imshow('DiegoGonzalez', cropped_image)
                placa = await ocr_plate(cropped_image)
                if len(placa) >= 1:
                    nameFile = 'bordes/detection_' + datetime.today().strftime('%Y-%m-%d-%H_%M_%S') + '.jpg'
                    # cv2.imwrite(nameFile, frames[34:600, 100:500])
                    cv2.imwrite(nameFile, frames[500:800, 34:600])
                    print("La placa es: ", placa)
        except:
            print("Se acabo el video")
            break
        ret, frames = cap.read()

        # thread = threading.Thread(target=guardarImagen, args=[frames])
        # thread.start()

        if cv2.waitKey(33) == 27:
            break

    # De-allocate any associated memory usage
    cv2.destroyAllWindows()

ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(main(cap))
ioloop.close()


#main(cap)

## LEER IMAGEN
# img = cv2.imread("pictures/PROBAR3.PNG")
# cropped_image = img
# cropped_image = cropped_plate(img)
# print_photo(cropped_image)

## OCR
# placa = ocr_plate(cropped_image)
# print("La placa es: ", placa)
