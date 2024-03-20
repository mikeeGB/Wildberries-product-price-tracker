import requests
from config import url_patterns
from data_models.models import WBCardData, SizeLeft


def parse_product_card_by_code(articul: int) -> WBCardData:
    url = url_patterns.WB_CARD_PARSE_URL.format(card_articul=articul)
    card_data = requests.get(url).json()
    return WBCardData(**card_data['data'])


def get_sizes_left(card_response: WBCardData) -> list[SizeLeft]:
    return card_response.products[0].get_available_sizes()


def get_product_price(card_response: WBCardData) -> float:
    return card_response.products[0].sale_price_float


def get_product_brand(card_response: WBCardData) -> str:
    brand = card_response.products[0].brand
    return brand


def get_product_name(card_response: WBCardData) -> str:
    name = card_response.products[0].name
    return name


def get_product_articul(card_response: WBCardData) -> int:
    return card_response.products[0].id


def make_tg_message_about_sizes(card_response: WBCardData) -> str:
    sizes_left: list[SizeLeft] = get_sizes_left(card_response)
    sizes_message = "Sizes left: \n"
    if sizes_left:
        for size in sizes_left:
            sizes_message += f"[[{size.INTERNATIONAL}, {size.RU}]] -> _{size.left}_\n"
    else:
        sizes_message = "No products in store :("
    message = f"{sizes_message}"
    return message


def make_full_info_message(card_response: WBCardData) -> str:
    price = get_product_price(card_response)
    brand, name = get_product_brand(card_response), get_product_name(card_response)
    size_message = make_tg_message_about_sizes(card_response)
    articul = get_product_articul(card_response)
    message = (f"_{brand}_: {name}\n"
               f"Article: _{articul}_\n"
               f"Price: *{price} BYN*\n"
               f"{size_message}")
    return message


def make_full_info_message_v2(card_response: WBCardData) -> str:
    response_data = card_response.products[0].model_dump()
    brand = response_data['brand']
    name = response_data['name']
    articul = response_data['id']
    price = response_data['sale_price']
    size_message = make_tg_message_about_sizes(card_response)

    message = (f"_{brand}_: {name}\n"
               f"Article: _{articul}_\n"
               f"Price: *{price} BYN*\n"
               f"{size_message}")
    return message
