from abc import ABC, abstractmethod

class IView(ABC):
    @abstractmethod
    def main_menu(self) -> None:
        pass

    @abstractmethod
    def lib_menu(self) -> None:
        pass

    @abstractmethod
    def user_menu(self) -> None:
        pass

