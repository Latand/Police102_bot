from dataclasses import dataclass
from typing import Any

from environs import Env

from google.oauth2.service_account import Credentials


def get_scoped_credentials(credentials, scopes):
    def prepare_credentials():
        return credentials.with_scopes(scopes)

    return prepare_credentials


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool
    redis_password: str


@dataclass
class Miscellaneous:
    scoped_credentials: Any
    sheet_id: int


@dataclass
class Config:
    tg_bot: TgBot
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    scopes = [
        "https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"
    ]
    google_credentials = Credentials.from_service_account_file('./tgbot/config.json')
    scoped_credentials = get_scoped_credentials(google_credentials, scopes)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
            redis_password=env.str("REDIS_PASSWORD")
        ),

        misc=Miscellaneous(
            scoped_credentials=scoped_credentials,
            sheet_id=env.str('SHEET_ID')
        )
    )
