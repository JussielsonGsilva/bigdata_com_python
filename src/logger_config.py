from loguru import logger
import os

# Configura o diretório de logs
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configura o arquivo de log rotativo
logger.add(
    f"{LOG_DIR}/pipeline.log",
    rotation="10 MB",        # cria novo arquivo a cada 10MB
    retention="10 days",     # mantém logs por 10 dias
    level="INFO",
    encoding="utf-8"
)

# Exporta o logger configurado
def get_logger():
    return logger
