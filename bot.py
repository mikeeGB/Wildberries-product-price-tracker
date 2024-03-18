import requests
import time

from config import config, url_patterns
from parser.parser_logic_v2 import parse_product_card_by_code, get_product_price, make_full_info_message


def send_tg_message(chat_id: int, message: str):
    requests.post(
            url=url_patterns.TELEGRAM_API_SEND_MESSAGE_URL,
            data={'chat_id': chat_id, 'text': message, 'parse_mode': 'markdown'}
    )


def make_tg_call_via_callmebot(username: str, msg_text: str):
    requests.get(
        url=url_patterns.CALL_ME_BOT_URL.format(username=username, msg_text=msg_text),
    )


def start_trench_price_monitor(wb_articul: int, price_to_track: float, re_check_time: int):
    while True:
        time.sleep(re_check_time)
        wb_card = parse_product_card_by_code(wb_articul)
        price = get_product_price(card_response=wb_card)
        full_info = make_full_info_message(card_response=wb_card)

        if price <= price_to_track:
            make_tg_call_via_callmebot(username=config.TG_USERNAME, msg_text=f"Скидка! Цена: {price}")
            full_info = "\U00002757" + f"{full_info}"
            send_tg_message(chat_id=config.CHAT_ID, message=full_info)
            break

        send_tg_message(chat_id=config.CHAT_ID, message=full_info)


if __name__ == "__main__":
    start_trench_price_monitor(wb_articul=config.WB_ARTICUL, price_to_track=300.00, re_check_time=1200)
