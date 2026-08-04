import os
import logging
import sys
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("app")

ACCOUNT_NAME = os.getenv("AZURE_ACCOUNT_NAME")
CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME", "fotos")
ACCOUNT_URL = f"https://{ACCOUNT_NAME}.blob.core.windows.net"

SQL_SERVER = os.getenv("AZURE_SQL_SERVER")
SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE")
SQL_USERNAME = os.getenv("AZURE_SQL_USERNAME")
SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD")

log.debug("ACCOUNT_NAME=%s CONTAINER=%s", ACCOUNT_NAME, CONTAINER_NAME)
log.debug("SQL_SERVER=%s SQL_DATABASE=%s SQL_USERNAME=%s PWD_set=%s",
          SQL_SERVER, SQL_DATABASE, SQL_USERNAME, bool(SQL_PASSWORD))

MAX_FILE_MB = 1
MAX_FILE_BYTES = MAX_FILE_MB * 1024 * 1024
