from typing import Dict
# endpointy na prácu s dátami
from app import app
from flask import jsonify, request
from app.services.area import get_all_areas, add_area
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token


@app.route("/api/area/getAll",methods=["GET"])
@jwt_required()
def get_areas():
 #   body= request.get_json()
    result, status_code = get_all_areas()
    return jsonify(result), status_code


@app.route("/api/area/add", methods=["POST"])
@jwt_required()
def adding_area():
    body=request.get_json()
    result, status_code = add_area(body)
    return jsonify(result), status_code
    