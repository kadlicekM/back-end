from typing import Dict
# endpointy na prácu s dátami
from app import app
from flask import jsonify, request
from app.services.area import add_area, get_areas_with_sectors, get_all_user_areas
from flask_jwt_extended import jwt_required
from app.utils.helpers import decode_jwt_user_id

#get all users area
@app.route("/api/area/getAll",methods=["GET"])
@jwt_required()
def get_all_areas_for_user():
    user_id = decode_jwt_user_id(request)
    result, status_code = get_all_user_areas(user_id)
    return jsonify(result), status_code


@app.route("/api/area/getSectors",methods=["GET"])
@jwt_required()
def get_areas_and_sectors_for_user():
    user_id = decode_jwt_user_id(request)
    result, status_code = get_areas_with_sectors(user_id)
    return jsonify(result), status_code

#add area to user
@app.route("/api/area/add", methods=["POST"])
@jwt_required()
def insert_area():
    body=request.get_json()
    user_id = decode_jwt_user_id(request)
    result, status_code = add_area(user_id, body)
    print(result)
    return jsonify(result), status_code
    

    
