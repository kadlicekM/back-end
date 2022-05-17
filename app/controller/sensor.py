from typing import Dict
# endpointy na prácu s dátami
from app import app
from flask import jsonify, request
from app.services.sensor import remove_sensor,add_sensor, get_all_sensors_for_user, delete_sensor
from flask_jwt_extended import jwt_required

from app.utils.helpers import decode_jwt_user_id


@app.route("/api/sensor/delete",methods=["DELETE"])
@jwt_required()
def remove_sensor():
    body =request.get_json()
    result:Dict= delete_sensor(body)
    return jsonify(result)


@app.route("/api/sensor/add", methods=["POST"])
@jwt_required()
def insert_sensor():
    body=request.get_json()
    result, status_code = add_sensor(body)
    return jsonify(result), status_code


@app.route("/api/sensor/getAll", methods=["GET"])
@jwt_required()
def get_all_sensors():
    user_id = decode_jwt_user_id(request)
    result, status_code = get_all_sensors_for_user(user_id)
    return jsonify(result), status_code
    