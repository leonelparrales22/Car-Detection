from datetime import datetime

import cv2
import numpy as np
from crooped_image import cropped_plate
import asyncio
import requests
import threading

cap = cv2.VideoCapture('videos/video-17min-6am.mp4')
from ocr import ocr_plate

fgbg = cv2.createBackgroundSubtractorMOG2()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

def process_image (frame):
    nameFile = 'detection_' + datetime.today().strftime('%Y-%m-%d-%H_%M_%S') + '.jpg'
    cv2.imwrite("bdd/" + nameFile, frame)
    cropped_image = cropped_plate(frame)
    placa = ocr_plate(frame[500:800, 34:600])
    if placa:
        print(placa)
        nameFile2 = 'detectionPlate_' + datetime.today().strftime('%Y-%m-%d-%H_%M_%S') + '.jpg'
        cv2.imwrite("bordes/" + nameFile2, cropped_image)
        # url = 'http://127.0.0.1:5000/InsertarCarDetectionRegistration'
        # myobj = {
        #            "placa": placa,
        #            "ruta_frame": nameFile,
        #            "ruta_placa": namefile2,
        #            "tipo": 1
        #         }
        # requests.post(url, json=myobj)
    # url = 'http://127.0.0.1:5000/InsertarCarDetectionRegistration'
    # myobj = {
    #            "placa": "No tiene placa",
    #            "ruta_frame": nameFile,
    #            "ruta_placa": "recorte4.jpg",
    #            "tipo": 1
    #         }
    # requests.post(url, json=myobj)

async def main (cap):
    while True:
        ret, frame = cap.read()
        if ret == False: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Dibujamos un rectángulo en frame, para señalar el estado
        # del área en análisis (movimiento detectado o no detectado)
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (0, 0, 0), -1)
        color = (0, 255, 0)
        texto_estado = "Estado: No se ha detectado movimiento"
        # Especificamos los puntos extremos del área a analizar
        area_pts = np.array([[5, 600], [frame.shape[1] - 550, 600], [frame.shape[1] - 550, 790], [5, 790]])

        # Con ayuda de una imagen auxiliar, determinamos el área
        # sobre la cual actuará el detector de movimiento
        imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
        imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
        image_area = cv2.bitwise_and(gray, gray, mask=imAux)

        # Obtendremos la imagen binaria donde la región en blanco representa
        # la existencia de movimiento
        fgmask = fgbg.apply(image_area)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        fgmask = cv2.dilate(fgmask, None, iterations=2)

        # Encontramos los contornos presentes en fgmask, para luego basándonos
        # en su área poder determina si existe movimiento
        cnts = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        for cnt in cnts:
            if cv2.contourArea(cnt) > 30500 and cv2.contourArea(cnt) < 36000:
            #if cv2.contourArea(cnt) > 30000:
                print(cv2.contourArea(cnt))
                x, y, w, h = cv2.boundingRect(cnt)
                #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                texto_estado = "Estado: Alerta Movimiento Detectado!"
                # Create process to image
                thread = threading.Thread(name="processImage",target=process_image,args=[frame])
                thread.start()
                color = (0, 0, 255)
        # Visuzalizamos el alrededor del área que vamos a analizar
        # y el estado de la detección de movimiento
        cv2.drawContours(frame, [area_pts], -1, color, 2)
        cv2.putText(frame, texto_estado, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.imshow('fgmask', fgmask)
        cv2.imshow("frame", frame)
        k = cv2.waitKey(70) & 0xFF
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(main(cap))
ioloop.close()