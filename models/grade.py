from models.db import db

class Grade(db.Model):
    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Float, nullable=False)   # usamos 'score' como clave
    
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    student = db.relationship("Student", back_populates="grades")
    course = db.relationship("Course", back_populates="grades")

    def to_dict(self):
        return {"id": self.id, "score": self.score, "student_id": self.student_id, "course_id": self.course_id}
