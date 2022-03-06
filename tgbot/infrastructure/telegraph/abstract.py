import abc

from aiogram.types import PhotoSize


class FileUploader(abc.ABC):

    async def upload_photo(self, photo: PhotoSize):
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError
