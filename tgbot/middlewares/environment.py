from typing import Dict, Any

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import CallbackQuery, Message


class EnvironmentMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

    async def pre_process(self, obj: [CallbackQuery, Message], data: Dict, *args: Any) -> None:
        google_client_manager = self.kwargs.get('google_client_manager')
        if google_client_manager:
            google_client = await google_client_manager.authorize()
            self.kwargs.update(google_client=google_client)

        data.update(**self.kwargs)
