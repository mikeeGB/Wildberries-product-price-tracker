"""
Using pydantic settings

import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class BotConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV,
                                      env_file_encoding='utf-8')
    bot_api_key: SecretStr
    chat_id: int
    tg_username: str
    wb_articul: int


bot_config = BotConfig()
"""
import os

BOT_API_KEY = os.getenv('BOT_API_KEY')
CHAT_ID = os.getenv('CHAT_ID')
TG_USERNAME = os.getenv('TG_USERNAME')
WB_ARTICUL = os.getenv('WB_ARTICUL')
