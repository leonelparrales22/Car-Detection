import requests

url = 'http://127.0.0.1:5000/InsertarCarDetectionRegistration'

myobj = {
    "placa": "AAA-333",
    "ruta_frame": "detection_2022-01-23-14_29_12.jpg",
    "ruta_placa": "recorte4.jpg",
    "tipo": 1
}
x = requests.post(url, json=myobj)
print(x.text)