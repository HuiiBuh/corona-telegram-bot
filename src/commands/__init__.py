from helpers.message_handler import register_message_handler
from .commands import send_welcome, subscribe_to, subscriptions

message_handlers = [
    register_message_handler(send_welcome, commands=["start", "help"]),
    register_message_handler(subscribe_to, commands=["subscribe"]),
    register_message_handler(subscriptions, commands=["subscriptions"])
]
