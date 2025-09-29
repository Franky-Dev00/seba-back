from flask import Blueprint, request, jsonify
from models.db import db
from models.grade import Grade
from models.student import Student
from models.course import Course

grades_bp = Blueprint("grades", __name__)

@grades_bp.route("/", methods=["GET"])
def get_grades():
    grades = Grade.query.all()
    return jsonify([g.to_dict() for g in grades])

@grades_bp.route("/", methods=["POST"])
def create_grade():
    data = request.get_json() or {}
    student_id = data.get("student_id")
    course_id = data.get("course_id")
    grade_value = data.get("grade")

    if student_id is None or course_id is None or grade_value is None:
        return jsonify({"error": "Faltan campos obligatorios: student_id, course_id, grade"}), 400

    student = Student.query.get(student_id)
    course = Course.query.get(course_id)
    if not student or not course:
        return jsonify({"error": "Student o Course no encontrado"}), 404

    try:
        grade_value = float(grade_value)
    except (ValueError, TypeError):
        return jsonify({"error": "Grade debe ser un número"}), 400

    new_grade = Grade(student_id=student_id, course_id=course_id, grade=grade_value)
    db.session.add(new_grade)
    db.session.commit()
    return jsonify(new_grade.to_dict()), 201

@grades_bp.route("/<int:grade_id>", methods=["PUT"])
def update_grade(grade_id):
    grade = Grade.query.get_or_404(grade_id)
    data = request.get_json() or {}

    if "grade" in data:
        try:
            grade.grade = float(data.get("grade"))
        except (ValueError, TypeError):
            return jsonify({"error": "Grade debe ser un número"}), 400

    db.session.commit()
    return jsonify(grade.to_dict())

@grades_bp.route("/<int:grade_id>", methods=["DELETE"])
def delete_grade(grade_id):
    grade = Grade.query.get_or_404(grade_id)
    db.session.delete(grade)
    db.session.commit()
    return jsonify({"message": "Nota eliminada"})
