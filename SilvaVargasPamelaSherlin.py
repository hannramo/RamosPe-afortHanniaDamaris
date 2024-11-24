from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la conexión a MySQL/MariaDB
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://{USER}:{PASSWORD}@{SERVER}/{DATABASE}'
).format(
    USER='fortecsy_practicas', 
    PASSWORD='h4nn1aR4m05', 
    SERVER='www.fortecsystems.com.mx',  # Cambia según tu configuración
    DATABASE='fortecsy_hannia'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la tabla
class Empleado(db.Model):
    __tablename__ = 'tblEmpleados'  # Cambia por el nombre de tu tabla

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    carrera = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(10), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'carrera': self.carrera,
            'numero': self.numero
        }

# Ruta para obtener todos los empleados
@app.route('/empleados', methods=['GET'])
def obtener_empleados():
    try:
        empleados = Empleado.query.all()
        empleados_lista = [empleado.to_dict() for empleado in empleados]
        return jsonify(empleados_lista), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Ruta para agregar un nuevo empleado (POST)
@app.route('/empleados', methods=['POST'])
def agregar_empleado():
    data = request.json  # Obtener datos del cuerpo de la solicitud
    try:
        nuevo_empleado = Empleado(
            nombre=data['nombre'],
            carrera=data['carrera'],
            numero=data['numero']
        )
        db.session.add(nuevo_empleado)
        db.session.commit()
        return jsonify({"mensaje": "Empleado agregado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Ruta para actualizar un empleado por ID (PUT)
@app.route('/empleados/<int:id>', methods=['PUT'])
def actualizar_empleado(id):
    data = request.json  # Obtener datos del cuerpo de la solicitud
    try:
        empleado = Empleado.query.get(id)
        if not empleado:
            return jsonify({"error": "Empleado no encontrado"}), 404

        # Actualizar campos
        empleado.nombre = data.get('nombre', empleado.nombre)
        empleado.carrera = data.get('carrera', empleado.carrera)
        empleado.numero = data.get('numero', empleado.numero)

        db.session.commit()
        return jsonify({"mensaje": "Empleado actualizado exitosamente", "empleado": empleado.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Ruta para eliminar un empleado por ID (DELETE)
@app.route('/empleados/<int:id>', methods=['DELETE'])
def eliminar_empleado(id):
    try:
        empleado = Empleado.query.get(id)
        if not empleado:
            return jsonify({"error": "Empleado no encontrado"}), 404

        db.session.delete(empleado)
        db.session.commit()
        return jsonify({"mensaje": "Empleado eliminado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5010)
