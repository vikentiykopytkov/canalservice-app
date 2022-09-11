import os

WEBAPP_HOST = os.getenv('WEBAPP_HOST')
WEBAPP_PORT = int(os.getenv("WEBAPP_PORT"))

UPDATE_RATE = int(os.getenv('UPDATE_RATE'))

TELEGRAM_BOT = os.getenv('TELEGRAM_BOT')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

POSTGRES_DB = os.environ.get("POSTGRES_DB", 'canalservice')
POSTGRES_USER = os.environ.get("POSTGRES_USER", 'postgres')
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", 'canalservice')
POSTGRES_CONTAINER_NAME = os.environ.get("POSTGRES_CONTAINER_NAME", "postgres")