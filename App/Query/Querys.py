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