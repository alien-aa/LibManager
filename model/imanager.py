from abc import ABC, abstractmethod

from views.imanagerview import IManagerView
from providers.iprovider import ILibProvider, IUserProvider


class ILibManager(ABC):
    def __init__(self,
                 view: IManagerView = None,
                 provider: ILibProvider = None):
        self._view = view
        self._provider = provider

    @property
    def view(self) -> IManagerView:
        return self._view

    @property
    def provider(self) -> ILibProvider:
        return self._provider

    @abstractmethod
    def get_books_list(self, title: str = '', author: str = '') -> list[dict] | None:
        pass

    @abstractmethod
    def get_author(self, author: str = '') -> dict | None:
        pass

    @abstractmethod
    def show_books(self, title: str = '', author: str = '') -> bool:
        pass

    @abstractmethod
    def show_authors_page(self, author: str = '') -> bool:
        pass

    @abstractmethod
    def reserve_book(self, title: str = '', author_name: str = '', price: float = 0.0, genre: str = '') -> bool:
        pass

    @abstractmethod
    def return_book(self, title: str = '', author_name: str = '', price: float = 0.0, genre: str = '') -> bool:
        pass

    @abstractmethod
    def add_book(self, title: str = '', author_name: str = '', price: float = 0.0, genre: str = '') -> bool:
        pass

    @abstractmethod
    def edit_book(self,
                  old_title: str = '', old_author: str = '', old_price: float = 0.0, old_genre: str = '',
                  title: str = '', author: str = '', price: float = -1, genre: str = '') -> bool:
        pass

    @abstractmethod
    def delete_book(self, title: str = '', author: str = '', price: float = 0.0, genre: str = '',
                    copies: int = 1) -> bool:
        pass

    @abstractmethod
    def add_author(self, author: str = '', biography: str = '') -> bool:
        pass

    @abstractmethod
    def edit_author(self,
                    old_name: str = '', old_biography: str = '',
                    name: str = '', biography: str = '') -> bool:
        pass

    @abstractmethod
    def delete_author(self, author: str = '') -> bool:
        pass


class IUserManager(ABC):
    def __init__(self,
                 view: IManagerView = None,
                 provider: IUserProvider = None):
        self._view = view
        self._provider = provider

    @property
    def view(self) -> IManagerView:
        return self._view

    @property
    def provider(self) -> IUserProvider:
        return self._provider

    @abstractmethod
    def login(self, username: str = '', password: str = '') -> bool:
        pass

    @abstractmethod
    def logout(self) -> bool:
        pass

    @abstractmethod
    def new_user(self, username: str = "", email: str = "", status: bool = False, password: str = "") -> bool:
        pass

    @abstractmethod
    def delete_user(self) -> bool:
        pass

    @abstractmethod
    def update_user(self, username: str = "", email: str = "", password: str = "") -> bool:
        pass
