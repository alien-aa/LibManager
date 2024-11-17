from abc import ABC, abstractmethod

class ILibProvider(ABC):
    @abstractmethod
    def load(self) -> list[dict]:
        pass

    @abstractmethod
    def save(self, data: list[dict]) -> None:
        pass

class IUserProvider(ABC):
    @abstractmethod
    def load(self) -> list[dict]:
        pass

    @abstractmethod
    def save(self, data: list[dict]) -> None:
        pass