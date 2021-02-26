import logging

from aiogram.utils import executor

from globals import dispatcher, database, event_loop

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    async def initialize():
        database.initialize()


    event_loop.run_until_complete(initialize())
    executor.start_polling(dispatcher)
