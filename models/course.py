from models.db import db

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(250), nullable=True)

    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=True)
    teacher = db.relationship("Teacher", back_populates="courses")

    enrollments = db.relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    grades = db.relationship("Grade", back_populates="course", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description, "teacher_id": self.teacher_id}

