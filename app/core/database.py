
import os
import ssl
import pg8000.dbapi
from dotenv import load_dotenv

load_dotenv()


class Database:
    def get_connection(self):
        return pg8000.dbapi.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=int(os.getenv("DB_PORT", "5432")),
            ssl_context=ssl.create_default_context(),
            timeout=10
        )
