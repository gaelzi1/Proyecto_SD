document.getElementById('transactionForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevenir el envío normal del formulario

    // Obtener los valores de los campos
    const phone_number = document.getElementById('phone_number').value.trim();
    const amount = parseFloat(document.getElementById('amount').value.trim());
    const company = document.getElementById('company').value.trim();

    // Limpiar mensajes de error
    document.getElementById('phoneError').textContent = '';
    document.getElementById('amountError').textContent = '';

    // Validaciones
    let hasError = false;

    // Validar número de teléfono (10 dígitos)
    if (!/^\d{10}$/.test(phone_number)) {
        document.getElementById('phoneError').textContent = 'El número debe tener 10 dígitos.';
        hasError = true;
    }

    // Validar monto (solo permitir montos específicos)
    const validAmounts = [20.0, 30.0, 50.0, 100.0, 200.0];
    if (!validAmounts.includes(amount)) {
        document.getElementById('amountError').textContent = 'El monto debe ser uno de los siguientes: $20.00, $30.00, $50.00, $100.00 o $200.00.';
        hasError = true;
    }

    if (hasError) return;

    // Crear el objeto de datos
    const data = {
        phone_number: phone_number,
        amount: amount
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
    }
    const url = `${baseUrl}/transactions`;

    // Enviar la solicitud a la API
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
        .then((data) => {
            alert(`Transacción exitosa!\nID: ${data.transaction_id}\nComisión: ${data.commission}`);
            // Limpiar el formulario después del envío exitoso
            document.getElementById('transactionForm').reset();
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Ocurrió un error al enviar la transacción. Por favor, intenta de nuevo.');
        });
});
