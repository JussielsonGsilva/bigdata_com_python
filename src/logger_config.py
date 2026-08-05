from loguru import logger

from src.caminhos import LOGS

# Garante que a pasta de logs exista, com caminho absoluto:
# o log precisa cair sempre no mesmo lugar, não onde o script foi chamado.
LOGS.mkdir(parents=True, exist_ok=True)

# Configura o arquivo de log rotativo
logger.add(
    str(LOGS / "pipeline.log"),
    rotation="10 MB",        # cria novo arquivo a cada 10MB
    retention="10 days",     # mantém logs por 10 dias
    level="INFO",
    encoding="utf-8"
)

# Exporta o logger configurado
def get_logger():
    return logger
