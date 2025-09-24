from flask import Blueprint, request, jsonify
from models.db import db
from models.course import Course
from models.teacher import Teacher

courses_bp = Blueprint("courses", __name__)

@courses_bp.route("/", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return jsonify([c.to_dict() for c in courses])

@courses_bp.route("/", methods=["POST"])
def create_course():
    data = request.get_json() or {}
    # opcional: validar que teacher_id exista si se entrega
    teacher_id = data.get("teacher_id")
    new_course = Course(name=data.get("name"), description=data.get("description"), teacher_id=teacher_id)
    db.session.add(new_course)
    db.session.commit()
    return jsonify(new_course.to_dict()), 201

@courses_bp.route("/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Curso no encontrado"}), 404
    data = request.get_json() or {}
    course.name = data.get("name", course.name)
    course.description = data.get("description", course.description)
    course.teacher_id = data.get("teacher_id", course.teacher_id)
    db.session.commit()
    return jsonify(course.to_dict())

@courses_bp.route("/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Curso no encontrado"}), 404
    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": "Curso eliminado"})
