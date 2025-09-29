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
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Faltan campos obligatorios: name y email"}), 400

    if Teacher.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "El email ya existe"}), 400

    new_teacher = Teacher(name=data["name"], email=data["email"])
    db.session.add(new_teacher)
    db.session.commit()
    return jsonify(new_teacher.to_dict()), 201

@teachers_bp.route("/<int:teacher_id>", methods=["GET"])
def get_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    return jsonify(teacher.to_dict())

@teachers_bp.route("/<int:teacher_id>", methods=["PUT"])
def update_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    data = request.get_json() or {}
    teacher.name = data.get("name", teacher.name)
    teacher.email = data.get("email", teacher.email)
    db.session.commit()
    return jsonify(teacher.to_dict())

@teachers_bp.route("/<int:teacher_id>", methods=["DELETE"])
def delete_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    return jsonify({"message": "Profesor eliminado"})
