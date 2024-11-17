from abc import ABC, abstractmethod

class IManagerView(ABC):
    @abstractmethod
    def show_msg(self, msg: str = '') -> None:
        pass

    @abstractmethod
    def show_error(self, msg: str = '') -> None:
        pass