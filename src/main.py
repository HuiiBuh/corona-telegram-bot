import logging

from aiogram.utils import executor

from commands import message_handler_list, callback_handler_list
from globals import event_loop, initialize_database, dispatcher
from settings import SETTINGS

if SETTINGS.production:
    logging.basicConfig(filename="logs/bot.log",
                        format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                        level=logging.DEBUG)
else:
    logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                        level=logging.INFO)

if __name__ == "__main__":
    event_loop.run_until_complete(initialize_database())

    for handler in message_handler_list:
        dispatcher.register_message_handler(**handler)

    for handler in callback_handler_list:
        dispatcher.register_callback_query_handler(**handler)

    executor.start_polling(dispatcher)
