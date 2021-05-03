from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import PeerChannel

from src.settings import API_HASH, API_TOKEN, TELEGRAM_BOT_API_KEY, TELEGRAM_STRING_SESSION
from src.utils.logger import logger
from src.utils.miscellaneous import error_handler_context
from src.utils.rules_factory import load_rule

telegram_bot = TeleBot(TELEGRAM_BOT_API_KEY)
client = TelegramClient(StringSession(TELEGRAM_STRING_SESSION), API_TOKEN, API_HASH)


@client.on(events.NewMessage())
async def handler_new_message(event):
    logger.debug("New message: %s" % event.message.message)
    channel_id = event.message.chat_id

    rule = load_rule(channel_id)
    event_message = event.message.message

    if not rule:
        logger.debug("No found rule for channel_id: %s, ignored" % channel_id)
        return

    if not rule.validate_message(event_message):
        logger.info("Message: %(message)s not validated, ignored.")
        return

    rule.parse_message(event_message)

    if not rule.validate_signal():
        logger.info("Signal not validated, ignored.")
        return

    for channel_id, message in rule.channels_messages.items():
        logger.info("Signal validated, sending message to Channel %s.." % channel_id)

        with error_handler_context(Exception, context=f"ChannelId {channel_id}"):
            try:
                telegram_bot.send_message(chat_id=channel_id, text=message)

            except ApiTelegramException:
                channel = await client.get_entity(PeerChannel(channel_id))
                await client.send_message(entity=channel, message=message)


if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()
