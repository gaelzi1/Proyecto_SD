from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime

# Configuración inicial
app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Configurar conexión a MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/transactions_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo de base de datos para las transacciones
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    response = db.Column(db.String(100), nullable=True, default="Pending")
    commission = db.Column(db.Float, nullable=False)

# Endpoint para registrar transacciones
@app.route('/transactions', methods=['POST'])
def create_transaction():
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
            response="Pending",
            commission=commission
        )

        # Guardar la transacción en la base de datos
        db.session.add(new_transaction)
        db.session.commit()

        # Actualizar el estado a "Received"
        new_transaction.response = "Received"
        db.session.commit()

        return jsonify({
            "message": "Transaction created successfully!",
            "transaction_id": new_transaction.id,
            "amount": new_transaction.amount,
            "commission": new_transaction.commission,
            "status": new_transaction.response
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Ejecutar el servidor Flask
if __name__ == '__main__':
    app.run(debug=True, port=5002)
