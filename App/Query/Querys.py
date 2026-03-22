from App.Data.Banco import db
from App.Log.Logs import db_logger, Query_logger

from datetime import datetime, timezone, date, time

# ================ Salva as conversar no banco de dados ================ #
def salvar_msg(autor: str, conversa: str):
    db.connect()
    try:
        db.cursor.execute(
            "INSERT INTO conversa (autor, conversa) VALUES (%s, %s)",
            (autor, conversa)
        )
        db.connection.commit()
        Query_logger.info("Mensagem salva")
    except Exception as e:
        Query_logger.exception(f"Erro ao salvar mensagem | {e}")
    db.cursor.close()
    db.close_conect()
# ====================================================================== #
# ================== Salva as contas no banco de dados ================= #
def salva_contas(valor: float, descricao: str):
    db.connect()
    try:
        db.cursor.execute(
            "INSERT INTO valor_gasto (valor, descricao) VALUES (%s, %s)",
            (valor, descricao)
        )
        db.connection.commit()
        Query_logger.info("Conta salva")
    except Exception as e:
        Query_logger.exception(f"Erro ao salvar conta | {e}")
    db.cursor.close()
    db.close_conect()
# ====================================================================== #
# ==================== Pega todo o valor gasto no mes ================== #
def get_todas_contas():
    db.connect()
    try:
        db.cursor.execute("""
            SELECT COALESCE(SUM(valor), 0)
            FROM valor_gasto
            WHERE horario >= date_trunc('month', CURRENT_DATE)
            AND horario <  date_trunc('month', CURRENT_DATE) + INTERVAL '1 month';
        """)
        total = db.cursor.fetchone()[0]
        Query_logger.info("Valor total pego")
    except Exception as e:
        Query_logger.exception(f"Erro ao pegar o valor total | {e}")
    db.cursor.close()
    db.close_conect()
    return {"total": float(total)}
# ====================================================================== #
# ================== Pega uma lista detalhada de gasto ================= #
def get_contas_detalhada(limite=200):
    db.connect()
    try:
        db.cursor.execute("""
            SELECT id, valor, descricao, horario
            FROM valor_gasto
            WHERE horario >= date_trunc('month', CURRENT_DATE)
            AND horario < date_trunc('month', CURRENT_DATE) + INTERVAL '1 month'
            ORDER BY horario ASC
            LIMIT %s;
        """, (limite,))
        rows = db.cursor.fetchall()
        Query_logger.info("Todas contas pegas com sucesso")
    except Exception as e:
        Query_logger.exception(f"Erro ao pegar todas as contas | {e}")
    db.cursor.close()
    db.close_conect()
    return rows
# ====================================================================== #
# ==================== REMOVE UM GASTO JÁ EXISTENTE ==================== #
def remove_conta(id: int):
    db.connect()
    try:
        db.cursor.execute(
            "DELETE FROM valor_gasto WHERE id = %s",
            (id, )
        )
        db.connection.commit()
        Query_logger.info("Conta removida com sucesso")
    except Exception as e:
        Query_logger.exception(f"Erro ao remover conta | {e}")
    db.cursor.close()
    db.close_conect()
# ====================================================================== #
# ==================== ALTERA O NOME/VALOR DA CONTA ==================== #
def altera_conta(id:int, valor:float, descricao: str):
    db.connect()
    try:
        db.cursor.execute(
            "UPDATE valor_gasto SET valor = COALESCE(%s, valor), descricao = COALESCE(%s, descricao) WHERE id = %s",
            (valor, descricao, id)
        )
        db.connection.commit()
        Query_logger.info("Alteração da conta feita com sucesso")
    except Exception as e:
        Query_logger.exception(f"Erro ao alterar conta | {e}")
    db.cursor.close()
    db.close_conect()
# ====================================================================== #
# ==================== AGENDA COMPROMISSOS NO BANCO ==================== #
def agenda_evento(data: date, descricao: str, horario: time):
    db.connect()
    try:
        db.cursor.execute(
            "INSERT INTO agenda (data, descricao, horario) VALUES (%s, %s, %s)",
            (data, descricao, horario)
        )
        db.connection.commit()
        Query_logger.info("Compromisso salvo")
    except Exception as e:
        Query_logger.exception(f"Erro ao salvar compromisso | {e}")
    db.cursor.close()
    db.close_conect()
# ====================================================================== #
# ===================== PEGA TODOS OS COMPROMISSOS ===================== #
def todo_compromissos(data: date):
    db.connect()
    rows = []
    try:
        db.cursor.execute(
            "SELECT * FROM agenda WHERE data >= %s;",
            (data, )
        )
        rows = db.cursor.fetchall()
        Query_logger.info(f"Todos os compromissos pegos apartir de {data}")
        return rows
    except Exception as e:
        Query_logger.exception(f"Erro ao pegar todos os compromissos | {e}")
    finally:
        db.cursor.close()
        db.close_conect()  
# ====================================================================== #
