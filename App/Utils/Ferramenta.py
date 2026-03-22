from decimal import Decimal
from datetime import datetime, date, time
from typing import Optional
from zoneinfo import ZoneInfo

from App.Log.Logs import ferramentas_logger
from App.Query.Querys import *


# Salva as contas no banco ✅
def set_conta_tool(valor: float, descricao: str):
    return salva_contas(valor, descricao)

# Pega todo o gasto do mês ✅
def get_valor_total_contas_tool():
    return get_todas_contas()

# Pega as contas detalhadas ✅
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

# remove alguma conta ✅
def remove_conta_tool(id: int):
    return remove_conta(id)

# Altera conta já existente ✅
def altera_conta_tool(id: int, valor: Optional[float] = None, descricao: Optional[str] = None):
    return altera_conta(id=id, valor=valor, descricao=descricao)

# Salva compromisso no banco ✅
def agenda_evento_tool(data: date, descricao: str, horario: time):
    try:

        resultado = agenda_evento(data, descricao, horario)
        ferramentas_logger.info(f"SUCESSO: Evento salvo | Data: {data} | Horário: {horario} | Descrição: {descricao}")
        return resultado
    except Exception as e:
        ferramentas_logger.exception(f"ERRO: Falha ao salvar evento | Data: {data} | Horário: {horario} | Descrição: {descricao} | Erro: {e}") 

# Vê que dia e horario é ✅
def data_atual_tool():
    agora = datetime.now(ZoneInfo("America/Sao_Paulo"))
    return {
        "data": agora.date().isoformat(),      # "YYYY-MM-DD"
        "hora": agora.strftime("%H:%M"),       # "HH:MM"
        "datetime": agora.isoformat()          # completo
    }

# pega todos os compromissos
def todo_compromissos_tool(data: str = None):
    ferramentas_logger.info(f"ENTROU na todo_compromissos_tool | data recebida: {data}")
    try:
        if not data:
            data_convertida = datetime.now(ZoneInfo("America/Sao_Paulo")).date()
            ferramentas_logger.info(f"Sem data informada. Usando data atual: {data_convertida}")
        else:
            data_convertida = date.fromisoformat(data)
            ferramentas_logger.info(f"Buscando compromissos a partir de {data_convertida}")

        return todo_compromissos(data_convertida)

    except ValueError:
        ferramentas_logger.exception(
            f"Erro ao converter data | esperado YYYY-MM-DD | recebido: {data}"
        )
        return {"erro": "Formato de data inválido. Use YYYY-MM-DD"}
    