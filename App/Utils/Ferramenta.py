from App.Log.Logs import ferramentas_logger
from App.Query.Querys import *


# Salva as contas no banco
def get_conta_tool(valor: float, descricao: str):
    return salva_contas(valor, descricao)

# pega as contas do mes
def get_todas_contas_tool():
    return get_todas_contas()