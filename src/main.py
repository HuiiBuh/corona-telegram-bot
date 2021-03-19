import logging

from aiogram.utils import executor
from pycache import add_schedule

from commands import message_handler_list, callback_handler_list
from commands.schedule import send_status_update
from globals import event_loop, initialize_database, dispatcher
from settings import SETTINGS

formatter = logging.Formatter('%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s')


def setup_logging():
    # File logging
    file_logger = logging.FileHandler("logs/bot.log")
    file_logger.setFormatter(formatter)

    # Console logging
    console_logger = logging.StreamHandler()
    console_logger.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if SETTINGS.production:
        logger.addHandler(console_logger)
        logger.addHandler(file_logger)
    else:
        logger.addHandler(console_logger)


if __name__ == "__main__":
    setup_logging()

    event_loop.run_until_complete(initialize_database())
    for handler in message_handler_list:
        dispatcher.register_message_handler(**handler)

    for handler in callback_handler_list:
        dispatcher.register_callback_query_handler(handler[0], *handler[1])

    schedule = add_schedule(send_status_update, call_at="18:15:01", event_loop=event_loop)


    async def on_shutdown(_):
        schedule.stop()


    executor.start_polling(dispatcher, on_shutdown=on_shutdown)
