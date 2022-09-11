import asyncio
import settings
from asgiref.wsgi import WsgiToAsgi

from script import (db_init, update_data)
from web.app import app

from uvicorn import Config, Server

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    loop.create_task(db_init())
    loop.create_task(update_data())

    config = Config(app=WsgiToAsgi(app), host=settings.WEBAPP_HOST, port=settings.WEBAPP_PORT, loop=loop)
    server = Server(config)
    loop.create_task(server.serve())

    loop.run_forever()