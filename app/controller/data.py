# from crypt import methods
from socketserver import ThreadingMixIn
from typing import Dict
# endpointy na prácu s dátami
from app import app
from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token
from app.services.data import get_chart_data, insert_data
from app.model.user import User


@app.route('/api/data/add', methods=['POST'])
def add_data():
    body = request.get_json()
    result, status_code = insert_data(body)
    return jsonify(result), status_code


@app.route('/api/data/get', methods=['POST'])
def get_data():
    body = request.get_json()
    result, status_code = get_chart_data(body)
    return jsonify(result), status_code
    # Todo structure for chart's dropdown 
    # data = {
    #     "areas": [
    #          {"id": "1", "label": "AREA1", "sectors": [{"id": "1", "sensors": [{"id": "1"}]}, {"id": "2", "sensors": [{"id": "09"}]}]},
    #          {"id": "2", "sectors": [{"id": "6", "sensors": [{"id": "8"}]}]}
    #     ]
    # }

