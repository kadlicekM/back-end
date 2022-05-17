
from typing import Dict
# endpointy na prácu s dátami
from app import app
from flask import jsonify, request
from app.services.sector import add_sector, get_all_user_sectors
from flask_jwt_extended import jwt_required

from app.utils.helpers import decode_jwt_user_id


@app.route("/api/sector/add", methods=["POST"])
@jwt_required()
def insert_sector():
    body=request.get_json()
    result, status_code = add_sector(body)
    return jsonify(result), status_code


@app.route("/api/area/getAll",methods=["GET"])
@jwt_required()
def get_all_sectors():
    user_id = decode_jwt_user_id(request)
    result, status_code = get_all_user_sectors(user_id)
    return jsonify(result), status_code