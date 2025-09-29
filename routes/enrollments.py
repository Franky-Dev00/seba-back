from flask import Blueprint, request, jsonify
from models.db import db
from models.enrollment import Enrollment
from models.student import Student
from models.course import Course

enrollments_bp = Blueprint("enrollments", __name__)

@enrollments_bp.route("/", methods=["GET"])
def get_enrollments():
    enrollments = Enrollment.query.all()
    return jsonify([e.to_dict() for e in enrollments])

@enrollments_bp.route("/", methods=["POST"])
def create_enrollment():
    data = request.get_json() or {}
    student_id = data.get("student_id")
    course_id = data.get("course_id")

    if not student_id or not course_id:
        return jsonify({"error": "Faltan campos obligatorios: student_id y course_id"}), 400

    student = Student.query.get(student_id)
    course = Course.query.get(course_id)
    if not student or not course:
        return jsonify({"error": "Student o Course no encontrado"}), 404

    # evitar duplicado
    if Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first():
        return jsonify({"error": "El estudiante ya está inscrito en este curso"}), 400

    new_enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(new_enrollment)
    db.session.commit()
    return jsonify(new_enrollment.to_dict()), 201

@enrollments_bp.route("/<int:enrollment_id>", methods=["DELETE"])
def delete_enrollment(enrollment_id):
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    db.session.delete(enrollment)
    db.session.commit()
    return jsonify({"message": "Inscripción eliminada"})
