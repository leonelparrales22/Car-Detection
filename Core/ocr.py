import easyocr
import requests

#async def ocr_plate(cropped_image):
def ocr_plate(cropped_image):

    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image, text_threshold=0.8)

    placa = []

    for i in range(len(result)):
        placa.append(result[i][1].upper())


    #if placa[0].upper() == "ECUADOR":
    #    print("La placa es ecuatoriana.")

    return placa

# PBN 6583
# print("Resultado", ocr_core(cropped_image))

# GSN-9520
# GTC-7820,
# PBB 3239
# TDH-398
# PBM6583
