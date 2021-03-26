import logging

logger = logging.getLogger("telegramcopy")
handler = logging.StreamHandler()

formater = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
handler.setFormatter(formater)

logger.addHandler(handler)
logger.setLevel(logging.INFO)
