from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime, timezone
import psycopg2
import math
import numpy as np
import easyocr


def conexionPostgres():
    connection = psycopg2.connect(user="postgres",
                                  password="123456",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="Car_Detection")
    return connection;


def ocr_plate(cropped_image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image, text_threshold=0.70)
    placa = []
    for i in range(len(result)):
        placa.append(result[i][1])
    return placa

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Server Arriba!</p>"


@app.route("/InsertarCarDetectionRegistration", methods=['POST'])
@cross_origin()
def InsertarCarDetectionRegistration():
    estado = "200"
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        try:
            connection = conexionPostgres()
            cursor = connection.cursor()
            postgres_insert_query = """ INSERT INTO car_detection_registration (fecha, placa, ruta_frame, ruta_placa, tipo) VALUES (%s,%s,%s,%s,%s)"""
            print(datetime.now(timezone.utc))
            record_to_insert = (datetime.now(timezone.utc), json["placa"], json["ruta_frame"],json["ruta_placa"], json["tipo"])
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into mobile table")
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into car_detection_registration table", error)
            estado = "500"
        finally:
            if connection:
                cursor.close()
                connection.close()
    else:
        estado = "300"
    return estado


@app.route("/ObtenerCarDetectionRegistration", methods=['GET'])
def ObtenerCarDetectionRegistration():
    offset = request.args.get('offset')
    try:
        connection = conexionPostgres()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM car_detection_registration order by fecha desc limit 5 offset " + offset)
        record = cursor.fetchall()
        return jsonify(record)
    except (Exception, psycopg2.Error) as error:
        print("Failed to get records from car_detection_registration table", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
    return jsonify([])

@app.route("/ObtenerCarDetectionRegistrationPaginado", methods=['GET'])
def ObtenerCarDetectionRegistrationPaginado():
    try:
        connection = conexionPostgres()
        cursor = connection.cursor()
        cursor.execute("select count(id_car_detection_registration) from car_detection_registration cdr" )
        record = cursor.fetchall()
        rounded = math.ceil(record[0][0]/5)
        return str(rounded)
    except (Exception, psycopg2.Error) as error:
        print("Failed to get records from car_detection_registration table", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
    return jsonify([])

@app.route("/RealziarOCR", methods=['POST'])
def RealziarOCR():
    estado = "200"
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        try:
            for objeto in json:
                #print(type(objeto["frame"]))
                #print(objeto["filename"])
                #print(objeto["fecha"])
                newtuple = tuple(objeto["datashape"].split(' '))
                frame = np.fromstring(objeto["frame"], sep=' ').reshape(tuple(map(int, newtuple)))
                dd = listToString(ocr_plate(frame))
                print(dd)
            return estado
        except Exception as error:
            print("Failed: ", error)
            estado = "500"
    else:
        estado = "300"
    return estado