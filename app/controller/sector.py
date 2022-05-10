
from typing import Dict
# endpointy na prácu s dátami
from app import app
from flask import jsonify, request
from app.services.sector import get_areas_sectors,add_sector
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token

@app.route("/api/sector/getAreasSector",methods=["GET"])
@jwt_required()
def get_sectors():
 #   body= request.get_json()
    result, status_code = get_areas_sectors()
    return jsonify(result), status_code


@app.route("/api/sector/add", methods=["POST"])
@jwt_required()
def adding_sector():
    body=request.get_json()
    result, status_code = add_sector(body)
    return jsonify(result), status_code