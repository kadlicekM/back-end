from typing import Dict
# endpointy na prácu s dátami
from app import app
from flask import jsonify, request
from app.services.sensor import remove_sensor,add_sensor
from flask_jwt_extended import jwt_required


@app.route("/api/sensor/delete",methods=["POST"])
@jwt_required()
def delete_data():
    body =request.get_json()
    result:Dict= remove_sensor(body)
    return jsonify(result)

@app.route("/api/sector/addSector", methods=["POST"])
@jwt_required()
def adding_sensor():
    body=request.get_json()
    result, status_code = add_sensor(body)
    return jsonify(result), status_code
    