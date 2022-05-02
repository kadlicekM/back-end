from socketserver import ThreadingMixIn
from typing import Dict
# endpointy na prácu s dátami
from app import app
from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token
from app.services.data import insert_data
from app.model.user import User

@app.route('/api/data/add', methods=['POST'])
def add_data():
    body = request.get_json()
    result: Dict = insert_data(body)
    return jsonify(result)

