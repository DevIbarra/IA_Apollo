import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

# ==== Como Usar ==== #

# try:
#    db_logger.info("Conectou no banco")
# except Exception:
#    db_logger.exception("Erro ao executar query")

# ================= CONFIG =================

_DEFAULT_MAX_BYTES = 5 * 1024 * 1024
_DEFAULT_BACKUP_COUNT = 5

# logs/<YYYY-MM-DD>/<grupo>/<name>.log
BASE_LOG_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__))
)

# ==========================================

def create_logger(
    name: str,
    grupo: str,
    level=logging.INFO,
    console: bool = False,
):
    """
    Cria logger em:
      logs/YYYY-MM-DD/<grupo>/<name>.log         -> tudo >= level (INFO por padrão)
      logs/YYYY-MM-DD/<grupo>/<name>_error.log   -> somente ERROR+ (com stacktrace via logger.exception)
    """

    logger_key = f"{grupo}.{name}"
    logger = logging.getLogger(logger_key)

    # evita duplicar handlers se importar o módulo mais de uma vez
    if getattr(logger, "_configured", False):
        return logger

    # Logger aceita tudo; os handlers filtram
    logger.setLevel(logging.DEBUG)

    # ======== pasta por dia ======== #
    day = datetime.now().strftime("%Y-%m-%d")
    log_dir = os.path.join(BASE_LOG_DIR, day, grupo)
    os.makedirs(log_dir, exist_ok=True)

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    # ===== handler principal =====
    main_path = os.path.join(log_dir, f"{name}.log")
    main_handler = RotatingFileHandler(
        main_path,
        maxBytes=_DEFAULT_MAX_BYTES,
        backupCount=_DEFAULT_BACKUP_COUNT,
        encoding="utf-8",
    )
    main_handler.setLevel(level)
    main_handler.setFormatter(fmt)
    logger.addHandler(main_handler)

    # ===== handler só de erro =====
    error_path = os.path.join(log_dir, f"{name}_error.log")
    error_handler = RotatingFileHandler(
        error_path,
        maxBytes=_DEFAULT_MAX_BYTES,
        backupCount=_DEFAULT_BACKUP_COUNT,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(fmt)
    logger.addHandler(error_handler)

    # ===== console opcional =====
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(fmt)
        logger.addHandler(console_handler)

    logger.propagate = False
    logger._configured = True
    return logger


# ================= LOGGERS PRONTOS ================= #
# Use só esse logger para o banco:
db_logger = create_logger("DataBase", "DataBase", level=logging.INFO, console=False)

ferramentas_logger = create_logger("Ferramentas", "Ferramentas", level=logging.INFO, console=False)