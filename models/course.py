from models.db import db

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # Identificador único del curso
    title = db.Column(db.String(120), nullable=False) # Título del curso
    description = db.Column(db.Text, nullable=True) # Descripción del curso

    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False) # ID del profesor que imparte el curso
    teacher = db.relationship("Teacher", back_populates="courses") # Relación con el modelo Teacher

    enrollments = db.relationship("Enrollment", back_populates="course", cascade="all, delete-orphan") # Relación con el modelo Enrollment
    grades = db.relationship("Grade", back_populates="course", cascade="all, delete-orphan") # Relación con el modelo Grade

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "teacher_id": self.teacher_id
        } # Método para convertir el objeto Course a un diccionario


