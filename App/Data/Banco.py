import os
import psycopg2
from dotenv import load_dotenv
from App.Log.Logs import db_logger

load_dotenv()


class DataBase:
    def __init__(self) -> None:
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")

        self.cursor = None
        self.connection = None

    def connect(self):
        """
        Só cria conexão se não existir ou se estiver fechada.
        Evita reconectar toda hora.
        """
        try:
            if self.connection and not self.connection.closed:
                return self.connection  # já está conectado

            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                dbname=self.database,
            )

            self.cursor = self.connection.cursor()

            db_logger.info("Conectado ao banco com sucesso")
            return self.connection

        except Exception:
            db_logger.exception("Erro ao conectar no banco")
            self.connection = None
            self.cursor = None
            return None

    def close_conect(self):
        """
        Fecha apenas se estiver aberto.
        """
        try:
            if self.cursor and not self.cursor.closed:
                self.cursor.close()
                db_logger.info("Cursor fechado")

            if self.connection and not self.connection.closed:
                self.connection.close()
                db_logger.info("Conexão fechada")

        except Exception:
            db_logger.exception("Erro ao fechar conexão/cursor")
            raise

# instancia global
db = DataBase()