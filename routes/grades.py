from flask import Blueprint, request, jsonify
from models.db import db
from models.grade import Grade

grades_bp = Blueprint("grades", __name__)

@grades_bp.route("/", methods=["GET"])
def get_grades():
    grades = Grade.query.all()
    return jsonify([g.to_dict() for g in grades])

@grades_bp.route("/", methods=["POST"])
def create_grade():
    data = request.get_json() or {}
    new_grade = Grade(score=data.get("score"), student_id=data.get("student_id"), course_id=data.get("course_id"))
    db.session.add(new_grade)
    db.session.commit()
    return jsonify(new_grade.to_dict()), 201

@grades_bp.route("/<int:grade_id>", methods=["PUT"])
def update_grade(grade_id):
    grade = Grade.query.get(grade_id)
    if not grade:
        return jsonify({"error": "Nota no encontrada"}), 404
    data = request.get_json() or {}
    grade.score = data.get("score", grade.score)
    db.session.commit()
    return jsonify(grade.to_dict())

@grades_bp.route("/<int:grade_id>", methods=["DELETE"])
def delete_grade(grade_id):
    grade = Grade.query.get(grade_id)
    if not grade:
        return jsonify({"error": "Nota no encontrada"}), 404
    db.session.delete(grade)
    db.session.commit()
    return jsonify({"message": "Nota eliminada"})
