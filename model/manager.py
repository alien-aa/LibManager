from model.imanager import ILibManager, IUserManager
from model.book import Book
from model.author import Author
from model.user import User
from providers.iprovider import ILibProvider, IUserProvider

from views.imanagerview import IManagerView

class Library:
    def __init__(self,
                 books: list[Book] = None,
                 authors: list[Author] = None,
                 users: list[User] = None,
                 current_user: User = None):
        self._books = books if books is not None else []
        self._authors = authors if authors is not None else []
        self._users = users if users is not None else []
        self._current_user = current_user

    @property
    def books(self):
        return self._books

    @books.setter
    def books(self, value: list[Book] = None) -> None:
        self._books = value if value is not None else []

    @property
    def authors(self):
        return self._authors

    @authors.setter
    def authors(self, value: list[Author] = None) -> None:
        self._authors = value if value is not None else []

    @property
    def users(self):
        return self._users

    @users.setter
    def users(self, value: list[User] = None) -> None:
        self._users = value if value is not None else []

    @property
    def current_user(self):
        return self._current_user

    @current_user.setter
    def current_user(self, value: User = None) -> None:
        self._current_user = value


class LibManager(ILibManager):
    def __init__(self,
                 library: Library = None,
                 view: IManagerView = None,
                 provider: ILibProvider = None):
        super().__init__(view=view, provider=provider)
        self._library = library

    @property
    def view(self) -> IManagerView:
        return self._view

    @property
    def provider(self) -> ILibProvider:
        return self._provider

    @property
    def library(self) -> Library:
        return self._library

    def _find_author(self, author_name: str) -> Author | None:
        for author in self._library.authors:
            if author.name.lower() == author_name.lower():
                return author
        return None

    def _find_books(self, title: str, author: str) -> list[Book]:
        return [book for book in self._library.books if title.lower() in book.title.lower()
                and (author.lower() in book.author.lower() if author else True)]

    def _status_error_check(self) -> bool:
        if self._library.current_user is None or not self._library.current_user.admin:
            self.view.show_error("You do not have permission to perform this action.")
            return True
        return False

    def get_books_list(self, title: str = '', author: str = '') -> list[dict] | None:
        book_list = self._find_books(title=title, author=author)
        self.view.show_msg("Here's what we managed to find for your query:")
        if len(book_list) == 0:
            self.view.show_msg("Empty book list.")
            return None
        num = 1
        return_list = []
        for item in book_list:
            return_list.append(item.to_dict())
            self.view.show_msg(f"NUMBER : {num}")
            self.view.show_msg(f"{item}")
            num += 1
        return return_list

    def get_author(self, author: str = '') -> dict | None:
        result = self._find_author(author_name=author)
        return result.to_dict() if result is not None else None

    def show_books(self, title: str = '', author: str = '') -> bool:
        book_list = self._find_books(title=title, author=author)
        self.view.show_msg("Here's what we managed to find for your query:")
        if len(book_list) == 0:
            self.view.show_msg("Empty book list.")
            return False
        num = 1
        for item in book_list:
            self.view.show_msg(f"NUMBER : {num}")
            self.view.show_msg(f"{item}")
            num += 1
        return True

    def show_authors_page(self, author: str = '') -> bool:
        author_found = self._find_author(author_name=author)
        self.view.show_msg("Here's what we managed to find for your query:")
        if author_found is None:
            self.view.show_msg("Author not found.")
            return False
        self.view.show_msg(f"{author_found}")
        return False

    def reserve_book(self, title: str = '', author_name: str = '', price: float = 0.0, genre: str = '') -> bool:
        if self._library.current_user is None:
            self.view.show_error('You could not reserve book without logging in')
            return False
        book_list = self._find_books(title=title, author=author_name)
        if len(book_list) == 0:
            self.view.show_error('Book not found')
            return False
        book = None
        for item in book_list:
            if item.price == price and item.genre == genre:
                book = item
                break
        if book is None:
            self.view.show_error('Book not found')
            return False
        if book in self._library.current_user.currently_borrowed:
            self.view.show_error('The book has already been reserved.')
            return False
        if book.copies - book.borrowed_copies < 1:
            self.view.show_error('There are no copies left for the reservation.')
            return False
        book.borrowed_copies += 1
        self._library.current_user.currently_borrowed.append(book)
        self.view.show_msg(f'Book \"{book.title}\" by {book.author} has been successfully reserved.')
        return True

    def return_book(self, title: str = '', author_name: str = '', price: float = 0.0, genre: str = '') -> bool:
        if self._library.current_user is None:
            self.view.show_error('You could not return book without logging in')
            return False
        book_list = self._find_books(title=title, author=author_name)
        if len(book_list) == 0:
            self.view.show_error('Book not found')
            return False
        book = None
        for item in book_list:
            if item.price == price and item.genre == genre:
                book = item
                break
        if book is None:
            self.view.show_error('Book not found')
            return False
        if book not in self._library.current_user.currently_borrowed:
            self.view.show_error('The book was not reserved by this user.')
            return False
        book.borrowed_copies -= 1
        self._library.current_user.currently_borrowed.remove(book)
        self.view.show_msg(f'Book \"{book.title}\" by {book.author} has been successfully returned.')
        return True

    def add_book(self, title: str = '', author_name: str = '', price: float = 0.0, genre: str = '') -> bool:
        if self._status_error_check():
            return False
        if price < 0:
            self.view.show_error("Price must be greater thar 0.")
            return False
        author = self._find_author(author_name)
        if not author:
            author = Author(name=author_name)
            if author in self._library.authors:
                self.view.show_error("Author already exists.")
                return False
            self._library.authors.append(author)
        existing_book = self._find_books(title, author_name)
        if existing_book:
            existing_book[0].copies += 1
            return True
        new_book = Book(title=title, author=author_name, price=price, genre=genre)
        self._library.books.append(new_book)
        author.books.append(new_book)
        self.view.show_msg(f"Book \"{new_book.title}\" by {new_book.author} added successfully.")
        return True

    def edit_book(self,
                  old_title: str = '', old_author: str = '', old_price: float = 0.0, old_genre: str = '',
                  title: str = '', author: str = '', price: float = -1, genre: str = '') -> bool:
        if self._status_error_check():
            return False
        book_list = self._find_books(title=old_title, author=old_author)
        found_book = None
        for item in book_list:
            if item.price == old_price and item.genre == old_genre:
                found_book = item
                break
        if found_book is None:
            self.view.show_error("Book not found.")
            return False
        if found_book.borrowed_copies > 0:
            self.view.show_error("Is not available to edit.")
            return False
        if title:
            found_book.title = title
        if author:
            old_author = self._find_author(found_book.author)
            old_author.books.remove(found_book)
            found_book.author = author
            if not self._find_author(author):
                self.add_author(author=author, biography='')
            new_author = self._find_author(author)
            new_author.books.append(found_book)
        if price >= 0:
            found_book.price = price
        if genre:
            found_book.genre = genre
        self.view.show_msg("Book edited successfully.")
        return True

    def delete_book(self, title: str = '', author: str = '', price: float = 0.0, genre: str = '',
                    copies: int = 1) -> bool:
        if self._status_error_check():
            return False
        book_list = self._find_books(title=title, author=author)
        found_book = None
        for item in book_list:
            if item.price == price and item.genre == genre:
                found_book = item
                break
        if found_book is None:
            self.view.show_error("Book not found.")
            return False
        if copies < 0 or copies > found_book.copies - found_book.borrowed_copies:
            self.view.show_error("Invalid number of copies to delete.")
            return False
        found_book.copies -= copies
        if found_book.copies <= 0:
            author = self._find_author(author_name=found_book.author)
            author.books.remove(found_book)
            self._library.books.remove(found_book)
        self.view.show_msg("Book deleted successfully.")
        return True

    def add_author(self, author: str = '', biography: str = '') -> bool:
        if self._status_error_check():
            return False
        if author in self._library.authors:
            self.view.show_error("Author already exists.")
            return False
        new_author = Author(name=author, biography=biography)
        self._library.authors.append(new_author)
        self.view.show_msg(f"{new_author.name}'s page added successfully.")
        return True

    def edit_author(self,
                    old_name: str = '', old_biography: str = '',
                    name: str = '', biography: str = '') -> bool:
        if self._status_error_check():
            return False
        found_author = self._find_author(author_name=old_name)
        if found_author is None or found_author.biography != old_biography:
            self.view.show_error("Author not found.")
            return False
        if any(book.borrowed_copies > 0 for book in found_author.books):
            self.view.show_error("Is not available to edit.")
            return False
        if name:
            found_author.name = name
            for item in found_author.books:
                self.edit_book(old_title=item.title, old_author=item.author, old_price=item.price, old_genre=item.genre,
                               title='', author=name, price=-1, genre='')
        if biography:
            found_author.biography = biography
        self.view.show_msg("Author's page edited successfully.")
        return True

    def delete_author(self, author: str = '') -> bool:
        if self._status_error_check():
            return False
        author_found = self._find_author(author_name=author)
        if not author_found:
            self.view.show_error("Author's page not found.")
            return False
        if any(book.borrowed_copies > 0 for book in author_found.books):
            self.view.show_error("Is not available to delete.")
            return False
        for item in author_found.books:
            self._library.books.remove(item)
        author_found.books.clear()
        self._library.authors.remove(author_found)
        self.view.show_msg("Author's page deleted successfully.")
        return True


class UserManager(IUserManager):
    def __init__(self,
                 library: Library = None,
                 view: IManagerView = None,
                 provider: IUserProvider = None):
        super().__init__(view=view, provider=provider)
        self._library = library

    @property
    def view(self) -> IManagerView:
        return self._view

    @property
    def provider(self) -> IUserProvider:
        return self._provider

    @property
    def library(self) -> Library:
        return self._library

    def login(self, username: str = '', password: str = '') -> bool:
        if self._library.current_user is not None:
            self.view.show_error("You already logged in")
            return False
        user_found = None
        for item in self._library.users:
            if item.username == username:
                user_found = item
                break
        if user_found is None:
            self.view.show_error("User not found.")
            return False
        if user_found.check_password(password):
            self._library.current_user = user_found
            self.view.show_msg(f"User {user_found.username} has successfully logged in.")
            return True
        self.view.show_error("Wrong password.")
        return False

    def logout(self) -> bool:
        if self._library.current_user is None:
            self.view.show_error("User is not logged in.")
            return False
        self.view.show_msg(f"User {self._library.current_user.username} has successfully logged out.")
        self._library.current_user = None
        return True

    def new_user(self, username: str = "", email: str = "", status: bool = False, password: str = "") -> bool:
        if self._library.current_user is not None:
            self.view.show_error("You already logged in")
            return False
        if (any(user.username == username for user in self._library.users)
            or any(user.email == email for user in self._library.users)):
            self.view.show_error("User already exists.")
            return False
        new_one = User(username, email, status, None, password)
        self._library.users.append(new_one)
        self._library.current_user = new_one
        self.view.show_msg(f"User {self._library.current_user.username} has successfully registered and logged in.")
        return True

    def delete_user(self) -> bool:
        if self._library.current_user is None:
            self.view.show_error("User is not logged in.")
            return False
        self.view.show_msg(f"User {self._library.current_user.username} has successfully deleted.")
        self._library.users.remove(self._library.current_user)
        self._library.current_user = None
        return True

    def update_user(self, username: str = "", email: str = "", password: str = "") -> bool:
        if username != '':
            self._library.current_user.username = username
        if email != '':
            self._library.current_user.email = email
        if password != '':
            self._library.current_user.password_hash = password
        self.view.show_msg("User fields updated successfully.")
        return True

