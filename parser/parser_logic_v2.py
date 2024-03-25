import requests
from config import url_patterns
from data_models.models import WBCardData, SizeLeft, Product


def parse_product_card_by_code(articul: int) -> Product:
    url = url_patterns.WB_CARD_PARSE_URL.format(card_articul=articul)
    card_data = requests.get(url).json()
    product_card = WBCardData(**card_data['data']).products[0]
    return product_card


def get_sizes_left(card_response: Product) -> list[SizeLeft]:
    return card_response.get_available_sizes()


def get_product_price(card_response: Product) -> float:
    return card_response.sale_price_float


def get_product_brand(card_response: Product) -> str:
    brand = card_response.brand
    return brand


def get_product_name(card_response: Product) -> str:
    name = card_response.name
    return name


def get_product_articul(card_response: Product) -> int:
    return card_response.id


def make_tg_message_about_sizes(card_response: Product) -> str:
    sizes_left: list[SizeLeft] = get_sizes_left(card_response)
    sizes_message = "Sizes left: \n"
    if sizes_left:
        for size in sizes_left:
            sizes_message += f"[[{size.INTERNATIONAL}, {size.RU}]] -> _{size.left}_\n"
    else:
        sizes_message = "No products in store :("
    message = f"{sizes_message}"
    return message


def make_full_info_message(card_response: Product) -> str:
    price = get_product_price(card_response)
    brand, name = get_product_brand(card_response), get_product_name(card_response)
    size_message = make_tg_message_about_sizes(card_response)
    articul = get_product_articul(card_response)
    message = (f"_{brand}_: {name}\n"
               f"Article: _{articul}_\n"
               f"Price: *{price} BYN*\n"
               f"{size_message}")
    return message


def make_full_info_message_v2(card_response: Product) -> str:
    product_data = card_response.model_dump()
    brand = product_data['brand']
    name = product_data['name']
    articul = product_data['id']
    price = product_data['sale_price']
    size_message = make_tg_message_about_sizes(card_response)

    message = (f"_{brand}_: {name}\n"
               f"Article: _{articul}_\n"
               f"Price: *{price:.2f} BYN*\n"
               f"{size_message}")
    return message
