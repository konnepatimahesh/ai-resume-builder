from flask import Blueprint, request, jsonify
from utils.decorators import login_required_api

parse_bp = Blueprint("parse", __name__)

@parse_bp.route("/parse", methods=["POST"])
@login_required_api
def parse():
    data = request.get_json(silent=True) or {}
    filename = data.get("filename", "")
    # TODO: wire up services/resume_parser.py
    return jsonify({"message": "Parse endpoint ready.", "filename": filename}), 200