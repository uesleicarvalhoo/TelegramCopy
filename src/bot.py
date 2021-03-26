import re

from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import PeerChannel

from src.settings import API_HASH, API_TOKEN, TELEGRAM_BOT_API_KEY, TELEGRAM_STRING_SESSION
from src.utils.logger import logger
from src.utils.signals_factory import load_signal

telegram_bot = TeleBot(TELEGRAM_BOT_API_KEY)
client = TelegramClient(StringSession(TELEGRAM_STRING_SESSION), API_TOKEN, API_HASH)


@client.on(events.NewMessage())
async def handler_new_message(event):
    logger.debug("New message: %s" % event.message.message)
    channel_id = get_channel_id_from_peer(str(event.message.to_id))

    signal = load_signal(channel_id)
    event_message = event.message.message

    if not signal or not signal.validate_message(event_message):
        return

    signal.parse_message(event_message)

    if not signal.validate_signal():
        return

    for channel_id, message in signal.channels_messages.items():
        logger.info("Signal validated, sending message to Channel %s.." % channel_id)
        try:
            telegram_bot.send_message(chat_id=channel_id, text=message)

        except ApiTelegramException:
            # TODO: Colocar alguma try/except para ignorar os canais que deram erro aqui
            channel = await client.get_entity(PeerChannel(channel_id))
            await client.send_message(entity=channel, message=message)


def get_channel_id_from_peer(peer: str) -> str:
    return re.findall(r'\b\d+\b', peer)[0]


if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()
