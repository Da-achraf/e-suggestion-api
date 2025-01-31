import os
from abc import ABC, abstractmethod
from typing import Optional


class UploadStrategy(ABC):
    @abstractmethod
    def upload(self, file, file_name: str) -> Optional[str]:
        """Upload a file and return its path or URL."""
        pass

    @abstractmethod
    def delete(self, file_path: str) -> bool:
        """Delete a file given its path or URL."""
        pass


class UploadContext:
    def __init__(self, strategy: UploadStrategy):
        self.strategy = strategy

    async def upload_file(self, file, file_name: str) -> Optional[str]:
        return await self.strategy.upload(file, file_name)

    def delete_file(self, file_path: str) -> bool:
        return self.strategy.delete(file_path)