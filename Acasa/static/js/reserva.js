document.addEventListener('DOMContentLoaded', () => {
    const dados = document.getElementById('diarias-reserva');
    if (!dados) return;
    const diarias = JSON.parse(dados.textContent);
    const entrada = document.getElementById('id_data_entrada');
    const saida = document.getElementById('id_data_saida');
    const locacao = document.getElementById('id_fk_locacao');
    const total = document.getElementById('id_valor_total');
    const resumo = document.getElementById('resumo-reserva');
    const moeda = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
    function calcular() {
        const diaria = Number(diarias[locacao.value]);
        const dias = (Date.parse(saida.value) - Date.parse(entrada.value)) / 86400000;
        if (!entrada.value || !saida.value || !Number.isFinite(diaria) || !Number.isFinite(dias) || dias <= 0) {
            total.value = '';
            resumo.textContent = 'Selecione o imóvel e um período com saída posterior à entrada.';
            return;
        }
        const valor = Math.round((diaria * dias + Number.EPSILON) * 100) / 100;
        total.value = valor.toFixed(2);
        resumo.textContent = `${dias} diária(s) × ${moeda.format(diaria)} = ${moeda.format(valor)}`;
    }
    [entrada, saida, locacao].forEach(campo => campo.addEventListener('change', calcular));
    calcular();
});
