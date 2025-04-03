document.getElementById('form-locomotiva').addEventListener('submit', function(event) {
    event.preventDefault();

    const temperaturaMotor = parseFloat(document.getElementById('temperaturaMotor').value);
    const consumoCombustivel = parseFloat(document.getElementById('consumoCombustivel').value);
    const jaSofreuManutencao = document.getElementById('jaSofreuManutencao').value;
    const pressaoOleo = parseFloat(document.getElementById('pressaoOleo').value);
    const temperaturaCombustivel = parseFloat(document.getElementById('temperaturaCombustivel').value);
    const temperaturaOleo = parseFloat(document.getElementById('temperaturaOleo').value);

    const dados = {
        temperaturaMotor,
        consumoCombustivel,
        jaSofreuManutencao,
        pressaoOleo,
        temperaturaCombustivel,
        temperaturaOleo
    };

    fetch('/avaliar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dados)
    })
    .then(response => {
        if (response.ok) {
            return response.json(); 
        } else {
            throw new Error('Erro na resposta do servidor');
        }
    })
    .then(data => {
        if (data.camposForaDoIdeal.length > 0) {
            alert('Campos fora do limite ideal: ' + data.camposForaDoIdeal.join(', '));
        } else {
            alert('Todos os campos estão dentro do limite ideal.');
        }
    })
    .catch(error => {
        console.error('Erro ao enviar dados:', error);
        alert('Ocorreu um erro ao enviar os dados.');
    });
});