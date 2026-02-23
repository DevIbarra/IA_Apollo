from decimal import Decimal
from datetime import datetime

from App.Log.Logs import ferramentas_logger
from App.Query.Querys import *


# Salva as contas no banco
def set_conta_tool(valor: float, descricao: str):
    return salva_contas(valor, descricao)

# Pega todo o gasto do mês
def get_valor_total_contas_tool():
    return get_todas_contas()

# Pega as contas detalhadas
def get_contas_detalhada_tool(limite=200):
    rows = get_contas_detalhada(limite=limite)

    if not rows:
        return "Não foi encontrado gastos esse mês."

    linhas = []

    for (id_, valor, descricao, horario) in rows:
        
        # Converte Decimal para float
        if isinstance(valor, Decimal):
            valor = float(valor)

        # Formata valor em R$
        valor_formatado = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        # Formata data
        if isinstance(horario, datetime):
            data_formatada = horario.strftime("%d/%m/%Y %H:%M")
        else:
            data_formatada = str(horario)

        linhas.append(
            f"Id: {id_}\n"
            f"Descrição: {descricao}\n"
            f"Valor: {valor_formatado}\n"
            f"Data: {data_formatada}\n"
        )

    return "\n".join(linhas)