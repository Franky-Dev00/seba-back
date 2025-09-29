from flask import Blueprint, request, jsonify
from models.db import db
from models.student import Student

students_bp = Blueprint("students", __name__)

@students_bp.route("/", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])

@students_bp.route("/", methods=["POST"])
def create_student():
    data = request.get_json() or {}
    new_student = Student(
        name=data.get("name"),
        email=data.get("email"),
        age=data.get("age")
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify(new_student.to_dict()), 201

@students_bp.route("/<int:student_id>", methods=["GET"])
def get_student(student_id):
    s = Student.query.get_or_404(student_id)
    return jsonify(s.to_dict())

@students_bp.route("/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Estudiante no encontrado"}), 404
    data = request.get_json() or {}
    student.name = data.get("name", student.name)
    student.email = data.get("email", student.email)
    student.age = data.get("age", student.age)
    db.session.commit()
    return jsonify(student.to_dict())

@students_bp.route("/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Estudiante no encontrado"}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Estudiante eliminado"})

