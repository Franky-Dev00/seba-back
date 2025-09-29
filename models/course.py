from models.db import db

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)
    teacher = db.relationship("Teacher", back_populates="courses")

    enrollments = db.relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    grades = db.relationship("Grade", back_populates="course", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "teacher_id": self.teacher_id
        }


