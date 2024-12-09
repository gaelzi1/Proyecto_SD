document.getElementById('transactionForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevenir el envío normal del formulario

    // Obtener los valores de los campos
    const phone_number = document.getElementById('phone_number').value.trim();
    const amount = document.getElementById('amount').value.trim();
    const company = document.getElementById('company').value.trim();

    // Limpiar mensajes de error
    document.getElementById('phoneError').textContent = '';
    document.getElementById('amountError').textContent = '';

    // Validaciones
    let hasError = false;

    if (!/^\d{10}$/.test(phone_number)) {
        document.getElementById('phoneError').textContent = 'El número debe tener 10 dígitos.';
        hasError = true;
    }

    const validAmounts = [20, 30, 50, 100, 200];
    if (!validAmounts.includes(parseFloat(amount))) {
        document.getElementById('amountError').textContent = 'El monto debe ser uno de los valores permitidos: 20, 30, 50, 100, 200.';
        hasError = true;
    }

    if (hasError) return;

    // Crear el objeto de datos
    const data = {
        phone_number: phone_number,
        amount: parseFloat(amount),
        company: company,
        timestamp: new Date().toISOString(),
    };

    // Construir la URL dinámica basada en la compañía seleccionada
    let baseUrl = '';
    switch (company) {
        case 'uli':
            baseUrl = 'http://127.0.0.1:5000';
            break;
        case 'g':
            baseUrl = 'http://127.0.0.1:5001';
            break;
        case 'e':
            baseUrl = 'http://127.0.0.1:5002';
            break;
        case 'minisuper':
            baseUrl = 'http://127.0.0.1:5003';
            break;
    }
    const url = `${baseUrl}/register`;

    // Enviar la solicitud a la API principal
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Error en el servidor');
            }
            return response.json();
        })
        .then((transactionData) => {
            alert(`Transacción exitosa!\nID: ${transactionData.transaction_id}`);
            
            // Registrar el movimiento en la API de movimientos
            return fetch('http://127.0.0.1:5002/log-movement', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    api_name: company,
                    action: 'create_transaction',
                    details: `Transaction ID: ${transactionData.transaction_id}, Amount: ${transactionData.amount}`
                }),
            });
        })
        .then((movementResponse) => {
            if (!movementResponse.ok) {
                throw new Error('Error al registrar el movimiento');
            }
            return movementResponse.json();
        })
        .then((movementData) => {
            console.log('Movimiento registrado exitosamente:', movementData);
            // Limpiar el formulario después del envío exitoso
            document.getElementById('transactionForm').reset();
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Ocurrió un error al procesar la transacción o registrar el movimiento. Por favor, intenta de nuevo.');
        });
});
