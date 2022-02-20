from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime, timezone
import psycopg2
import math
import constantes


def conexionPostgres():
    connection = psycopg2.connect(user=constantes.POSTGRES_USER,
                                  password=constantes.POSTGRES_PASSWORD,
                                  host=constantes.POSTGRES_HOST,
                                  port=constantes.POSTGRES_PORT,
                                  database=constantes.POSTGRES_DATABASE)
    return connection;


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
            record_to_insert = (
                datetime.now(timezone.utc), json["placa"], json["ruta_frame"], json["ruta_placa"], json["tipo"])
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
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')
    queryDate = f"where fecha > '{desde}' and fecha < '{hasta}'"
    try:
        connection = conexionPostgres()
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT * FROM car_detection_registration {queryDate} order by fecha desc limit 5 offset " + offset)
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
        desde = request.args.get('desde')
        hasta = request.args.get('hasta')
        queryDate = f"where fecha > '{desde}' and fecha < '{hasta}'"
        cursor.execute(f"select count(id_car_detection_registration) from car_detection_registration {queryDate}")
        record = cursor.fetchall()
        rounded = math.ceil(record[0][0] / 5)
        return str(rounded)
    except (Exception, psycopg2.Error) as error:
        print("Failed to get records from car_detection_registration table", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
    return jsonify([])
