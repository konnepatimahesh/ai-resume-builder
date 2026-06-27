from flask import Blueprint, request, jsonify
from utils.decorators import admin_required
from services.admin_service import get_all_users, get_user_resumes, get_activity

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/users", methods=["GET"])
@admin_required
def users():
    return jsonify({"users": get_all_users()}), 200


@admin_bp.route("/users/<int:user_id>/resumes", methods=["GET"])
@admin_required
def user_resumes(user_id):
    return jsonify({"resumes": get_user_resumes(user_id)}), 200


@admin_bp.route("/activity", methods=["GET"])
@admin_required
def activity():
    from_date = request.args.get("from")
    to_date   = request.args.get("to")
    logs = get_activity(from_date, to_date)
    return jsonify({"logs": logs}), 200