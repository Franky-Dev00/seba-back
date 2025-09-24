from flask import Blueprint, request, jsonify
from models.db import db
from models.enrollment import Enrollment

enrollments_bp = Blueprint("enrollments", __name__)

@enrollments_bp.route("/", methods=["GET"])
def get_enrollments():
    enrollments = Enrollment.query.all()
    return jsonify([e.to_dict() for e in enrollments])

@enrollments_bp.route("/", methods=["POST"])
def create_enrollment():
    data = request.get_json() or {}
    new_enrollment = Enrollment(student_id=data.get("student_id"), course_id=data.get("course_id"))
    db.session.add(new_enrollment)
    db.session.commit()
    return jsonify(new_enrollment.to_dict()), 201

@enrollments_bp.route("/<int:enrollment_id>", methods=["DELETE"])
def delete_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({"error": "Matrícula no encontrada"}), 404
    db.session.delete(enrollment)
    db.session.commit()
    return jsonify({"message": "Matrícula eliminada"})
