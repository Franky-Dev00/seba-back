from flask import Flask, jsonify
from models.db import db
from routes.students import students_bp
from routes.teachers import teachers_bp
from routes.courses import courses_bp
from routes.enrollments import enrollments_bp
from routes.grades import grades_bp
from flask_cors import CORS              # Importa la extensión CORS para permitir peticiones desde diferentes dominios (Cross-Origin Resource Sharing)

# Crear la app
app = Flask(__name__)

app.url_map.strict_slashes = False

CORS(
    app,
    resources={
        r"/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        },
    },
    supports_credentials=True,
)

# Config DB (puedes dejar tu URL aquí o usar variables de entorno)
DATABASE_URL = 'postgresql://seba:CMG3_seba#@44.199.207.193:5432/seba'
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar DB
db.init_app(app)

# Registrar blueprints con prefijo (las rutas en los archivos usan "/")
app.register_blueprint(students_bp, url_prefix="/students")
app.register_blueprint(teachers_bp, url_prefix="/teachers")
app.register_blueprint(courses_bp, url_prefix="/courses")
app.register_blueprint(enrollments_bp, url_prefix="/enrollments")
app.register_blueprint(grades_bp, url_prefix="/grades")

@app.route("/")
def home():
    return "Bienvenido a la API de Gestión de Estudiantes con Flask"

# Crear tablas (si no existen)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8084)
