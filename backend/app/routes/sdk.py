import time
from flask import Blueprint, jsonify, request
import jwt

from app import db, rq
import logging

import os
from ..models import Users, Databases, Usertables, t_tokens
import re 
from sqlalchemy import text 

signing_secret = os.environ["SLACK_SIGNING_SECRET"]

sdk = Blueprint('sdk', __name__, url_prefix='/api/sdk/v1')
logger = logging.getLogger(__name__)

@sdk.route('/validatetoken', methods=['GET'])
def validate_token():
    token = request.headers.get('Authorization')
    if not token or not re.match(r"^Bearer hkdb_tkn_[a-f0-9\-]{36}$", token):
        return jsonify({"error": "Invalid or missing token"}), 401


    if db.session.query(t_tokens).filter(t_tokens.key == token.split(" ")[1]).first():
        return jsonify({"valid": True}), 200
    else:
        return jsonify({"valid": False}), 401