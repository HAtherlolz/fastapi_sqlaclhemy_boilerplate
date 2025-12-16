from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self) -> None: ...

    @abstractmethod
    async def get_one(self) -> None: ...

    @abstractmethod
    async def get_list(self) -> None: ...

    @abstractmethod
    async def update(self) -> None: ...

    @abstractmethod
    async def delete(self) -> None: ...
