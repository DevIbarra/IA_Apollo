from App.Data.Banco import db
from App.Log.Logs import db_logger

from datetime import datetime, timezone

# ================ Salva as conversar no banco de dados ================ #
def salvar_msg(autor: str, conversa: str):
    db.connect()
    db.cursor.execute(
        "INSERT INTO conversa (autor, conversa) VALUES (%s, %s)",
        (autor, conversa)
    )
    db.connection.commit()
    db.cursor.close()
    db.close_conect()
# ====================================================================== #
# ================== Salva as contas no banco de dados ================= #
def salva_contas(valor: float, descricao: str):
    db.connect()
    db.cursor.execute(
        "INSERT INTO valor_gasto (valor, descricao) VALUES (%s, %s)",
        (valor, descricao)
    )
    db.connection.commit()
    db.cursor.close()
    db.close_conect()
# ====================================================================== #
# ==================== Pega todo o valor gasto no mes ================== #
def get_todas_contas():
    db.connect()
    db.cursor.execute("""
        SELECT COALESCE(SUM(valor), 0)
        FROM valor_gasto
        WHERE horario >= date_trunc('month', CURRENT_DATE)
          AND horario <  date_trunc('month', CURRENT_DATE) + INTERVAL '1 month';
    """)
    total = db.cursor.fetchone()[0]
    db.cursor.close()
    db.close_conect()
    return {"total": float(total)}
# ====================================================================== #
# ================== Pega uma lista detalhada de gasto ================= #
def get_contas_detalhada(limite=200):
    db.connect()
    db.cursor.execute("""
        SELECT id, valor, descricao, horario
        FROM valor_gasto
        WHERE horario >= date_trunc('month', CURRENT_DATE)
          AND horario < date_trunc('month', CURRENT_DATE) + INTERVAL '1 month'
        ORDER BY horario ASC
        LIMIT %s;
    """, (limite,))
    rows = db.cursor.fetchall()
    db.cursor.close()
    db.close_conect()
    return rows
# ====================================================================== #
# ==================== REMOVE UM GASTO JÁ EXISTENTE ==================== #
def remove_conta(id: int):
    db.connect()
    db.cursor.execute(
        "DELETE FROM valor_gasto WHERE id = %s",
        (id, )
    )
    db.connection.commit()
    db.cursor.close()
    db.close_conect()
# ====================================================================== #
# ==================== ALTERA O NOME/VALOR DA CONTA ==================== #
def altera_conta(id:int, valor:float, descricao: str):
    db.connect()
    db.cursor.execute(
        "UPDATE valor_gasto SET valor = COALESCE(%s, valor), descricao = COALESCE(%s, descricao) WHERE id = %s",
        (valor, descricao, id)
    )
    db.connection.commit()
    db.cursor.close()
    db.close_conect()
# ====================================================================== #