from config.config import BOT_API_KEY

WB_CARD_PARSE_URL = (
    "https://card.wb.ru/cards/v1/detail?appType=128"
    "&curr=byn&lang=ru&dest=-59208&spp=30&nm={card_articul}"
)

CALL_ME_BOT_URL = (
    "http://api.callmebot.com/start.php?user=@{username}"
    "&text={msg_text}&lang=ru-RU-Standard-D&rpt=1"
)

TELEGRAM_API_SEND_MESSAGE_URL = "https://api.telegram.org/bot{0}/{1}".format(BOT_API_KEY, "sendMessage")

