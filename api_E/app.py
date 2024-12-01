from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

# Configuración inicial
app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions_E.db'  # Base de datos específica para ULI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de base de datos para las transacciones
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    response = db.Column(db.String(100), nullable=True, default="Pending")  # Estado de la transacción
    commission = db.Column(db.Float, nullable=False)

# Crear la base de datos si aún no existe
with app.app_context():
    db.create_all()

# Endpoint para registrar transacciones para ULI
@app.route('/transactions', methods=['POST'])
def create_transaction_E():
    data = request.json
    try:
        phone_number = data['phone_number']
        amount = data['amount']
        commission_rate = 0.05  

        # Calcular la comisión
        commission = amount * commission_rate

        # Crear la transacción en la base de datos
        new_transaction = Transaction(
            phone_number=phone_number,
            amount=amount,
            response="Pending",  # Estado inicial es "Pending"
            commission=commission
        )

        # Guardar la transacción en la base de datos
        db.session.add(new_transaction)
        db.session.commit()

        # Aquí podrías agregar lógica para cambiar el estado a "Received" si es necesario
        new_transaction.response = "Received"  # Actualizando el estado a "Received"
        db.session.commit()

        # Responder con éxito y detalles de la transacción
        return jsonify({
            "message": "Transaction created successfully for E!",
            "transaction_id": new_transaction.id,
            "amount": new_transaction.amount,
            "commission": new_transaction.commission,
            "status": new_transaction.response  # Incluir el estado de la transacción
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Ejecutar el servidor Flask
if __name__ == '__main__':
    app.run(debug=True, port=5002)
