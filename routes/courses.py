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
    title = data.get("title")
    teacher_id = data.get("teacher_id")

    if not title or not teacher_id:
        return jsonify({"error": "Faltan campos obligatorios: title y teacher_id"}), 400

    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return jsonify({"error": "Teacher no encontrado"}), 404

    new_course = Course(
        title=title,
        description=data.get("description"),
        teacher_id=teacher_id
    )
    db.session.add(new_course)
    db.session.commit()
    return jsonify(new_course.to_dict()), 201

@courses_bp.route("/<int:course_id>", methods=["GET"])
def get_course(course_id):
    c = Course.query.get_or_404(course_id)
    return jsonify(c.to_dict())

@courses_bp.route("/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.get_json() or {}

    if "teacher_id" in data:
        teacher = Teacher.query.get(data.get("teacher_id"))
        if not teacher:
            return jsonify({"error": "Teacher no encontrado"}), 404
        course.teacher_id = data.get("teacher_id")

    course.title = data.get("title", course.title)
    course.description = data.get("description", course.description)
    db.session.commit()
    return jsonify(course.to_dict())

@courses_bp.route("/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": "Curso eliminado"})
