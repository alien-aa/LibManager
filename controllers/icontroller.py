from abc import ABC, abstractmethod

class ILibController(ABC):
    @abstractmethod
    def event_search_book(self) -> bool:
        pass

    @abstractmethod
    def event_search_author(self) -> bool:
        pass

    @abstractmethod
    def event_reserve(self) -> bool:
        pass

    @abstractmethod
    def event_return(self) -> bool:
        pass

    @abstractmethod
    def event_add_book(self) -> bool:
        pass

    @abstractmethod
    def event_add_author(self) -> bool:
        pass

    @abstractmethod
    def event_edit_book(self) -> bool:
        pass

    @abstractmethod
    def event_edit_author(self) -> bool:
        pass

    @abstractmethod
    def event_delete_book(self) -> bool:
        pass

    @abstractmethod
    def event_delete_author(self) -> bool:
        pass


class IUserController(ABC):
    @abstractmethod
    def event_login(self) -> bool:
        pass

    @abstractmethod
    def event_logout(self) -> bool:
        pass

    @abstractmethod
    def event_register(self) -> bool:
        pass

    @abstractmethod
    def event_update(self) -> bool:
        pass

    @abstractmethod
    def event_delete(self) -> bool:
        pass
