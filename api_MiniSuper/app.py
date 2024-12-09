from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime

# Configuración inicial
app = Flask(__name__)
CORS(app)

# Configurar conexión a MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/minisuper_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo para Registrar Transacciones
class TransactionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    response = db.Column(db.String(100), nullable=False, default="Pending")
    commission = db.Column(db.Float, nullable=False)

# Endpoint para Registrar Transacciones
@app.route('/transactions', methods=['POST'])
def log_transaction():
    data = request.json
    try:
        # Validar datos de entrada
        phone_number = data['phone_number']
        amount = data['amount']
        response = data.get('response', "Pending")  # Por defecto: "Pending"
        commission = data['commission']

        # Crear registro de transacción
        new_transaction = TransactionLog(
            phone_number=phone_number,
            amount=amount,
            response=response,
            commission=commission
        )

        # Guardar en la base de datos
        db.session.add(new_transaction)
        db.session.commit()

        return jsonify({
            "message": "Transaction logged successfully!",
            "transaction_id": new_transaction.id,
            "phone_number": new_transaction.phone_number,
            "amount": new_transaction.amount,
            "timestamp": new_transaction.timestamp,
            "response": new_transaction.response,
            "commission": new_transaction.commission
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Endpoint opcional para listar todas las transacciones
@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = TransactionLog.query.all()
    result = [{
        "id": t.id,
        "phone_number": t.phone_number,
        "amount": t.amount,
        "timestamp": t.timestamp,
        "response": t.response,
        "commission": t.commission
    } for t in transactions]
    return jsonify(result), 200

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=5003)
