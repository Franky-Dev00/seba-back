from flask import Blueprint, request, jsonify
from models.db import db
from models.teacher import Teacher

teachers_bp = Blueprint("teachers", __name__)

@teachers_bp.route("/", methods=["GET"])
def get_teachers():
    teachers = Teacher.query.all()
    return jsonify([t.to_dict() for t in teachers])

@teachers_bp.route("/", methods=["POST"])
def create_teacher():
    data = request.get_json() or {}
    new_teacher = Teacher(name=data.get("name"), email=data.get("email"), subject=data.get("subject"))
    db.session.add(new_teacher)
    db.session.commit()
    return jsonify(new_teacher.to_dict()), 201

@teachers_bp.route("/<int:teacher_id>", methods=["PUT"])
def update_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return jsonify({"error": "Profesor no encontrado"}), 404
    data = request.get_json() or {}
    teacher.name = data.get("name", teacher.name)
    teacher.email = data.get("email", teacher.email)
    teacher.subject = data.get("subject", teacher.subject)
    db.session.commit()
    return jsonify(teacher.to_dict())

@teachers_bp.route("/<int:teacher_id>", methods=["DELETE"])
def delete_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return jsonify({"error": "Profesor no encontrado"}), 404
    db.session.delete(teacher)
    db.session.commit()
    return jsonify({"message": "Profesor eliminado"})
