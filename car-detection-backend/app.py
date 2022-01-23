from flask import Flask, request, jsonify
from datetime import datetime, timezone
import psycopg2

def conexionPostgres():
    connection = psycopg2.connect(user="postgres",
                                  password="123456",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="Car_Detection")
    return connection;

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Server Arriba!</p>"


@app.route("/InsertarCarDetectionRegistration", methods=['POST'])
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
    try:
        connection = conexionPostgres()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM car_detection_registration")
        record = cursor.fetchall()
        return jsonify(record)
    except (Exception, psycopg2.Error) as error:
        print("Failed to get records from car_detection_registration table", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
    return jsonify([])