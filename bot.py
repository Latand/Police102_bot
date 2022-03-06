import asyncio
import logging

import gspread_asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config, Config
from tgbot.filters.admin import BotAdminFilter
from tgbot.handlers.submit_form import register_submit_form
from tgbot.handlers.user import register_user
from tgbot.infrastructure.telegraph.service import TelegraphService
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.services.broadcaster import broadcast

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, **kwargs):
    dp.setup_middleware(EnvironmentMiddleware(**kwargs))


def register_all_filters(dp):
    dp.filters_factory.bind(BotAdminFilter)


def register_all_handlers(dp):
    register_user(dp)
    register_submit_form(dp)


async def on_startup(bot, config: Config):
    await broadcast(bot, config.tg_bot.admin_ids, 'Бот запущен!')


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2(host='redis_cache', db=4,
                            password=config.tg_bot.redis_password) if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config
    google_client_manager = gspread_asyncio.AsyncioGspreadClientManager(
        config.misc.scoped_credentials
    )
    file_uploader = TelegraphService()
    register_all_middlewares(dp,
                             google_client_manager=google_client_manager,
                             file_uploader=file_uploader,
                             config=config)
    register_all_filters(dp)
    register_all_handlers(dp)
    await on_startup(bot, config)
    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
