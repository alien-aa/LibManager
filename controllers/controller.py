from controllers.icontroller import ILibController, IUserController
from model.imanager import IUserManager, ILibManager


class LibController(ILibController):
    def __init__(self,
                 model: ILibManager = None):
        self._model = model

    def _choose_book(self) -> dict | None:
        self._model.view.show_msg("Enter the title of the book:")
        title = input()
        self._model.view.show_msg("Enter the name of the author or press Enter to skip:")
        author = input()
        book_list = self._model.get_books_list(title=title, author=author)
        if book_list is None:
            return None
        number = -1
        while number <= 0 or number > len(book_list):
            try:
                self._model.view.show_msg("Enter the number of book you want to reserve (greater than 0):")
                number = int(input())
            except ValueError:
                self._model.view.show_error("It is not int value. Enter valid int value.")
        return book_list[number]

    def _choose_author(self) -> dict | None:
        self._model.view.show_msg("Enter the name of the author:")
        author = input()
        result = self._model.get_author(author=author)
        return result




    def event_search_book(self) -> bool:
        self._model.view.show_msg("Enter the title of the book to search:")
        title = input()
        self._model.view.show_msg("Enter the name of the author to search or press Enter to skip:")
        author = input()
        return self._model.show_books(title=title, author=author)

    def event_search_author(self) -> bool:
        self._model.view.show_msg("Enter the name of the author to search:")
        author = input()
        return self._model.show_authors_page(author=author)

    def event_reserve(self) -> bool:
        item = self._choose_book()
        if item is None:
            return False
        return self._model.reserve_book(title=item["title"], author_name=item["author"],
                                        price=item["price"], genre=item["genre"])

    def event_return(self) -> bool:
        item = self._choose_book()
        if item is None:
            return False
        return self._model.return_book(title=item["title"], author_name=item["author"],
                                       price=item["price"], genre=item["genre"])

    def event_add_book(self) -> bool:
        self._model.view.show_msg("Enter the title of the book:")
        title = input()
        self._model.view.show_msg("Enter the name of the author:")
        author = input()
        price = -1
        while price < 0:
            try:
                self._model.view.show_msg("Enter the price of the book:")
                price = float(input())
            except ValueError:
                self._model.view.show_error("It is not float value. Enter valid float value.")
        self._model.view.show_msg("Enter the genre of the book:")
        genre = input()
        return self._model.add_book(title=title, author_name=author, price=price, genre=genre)

    def event_add_author(self) -> bool:
        self._model.view.show_msg("Enter the name of the author:")
        author = input()
        self._model.view.show_msg("Enter the biography of the author:")
        biography = input()
        return self._model.add_author(author=author, biography=biography)

    def event_edit_book(self) -> bool:
        item = self._choose_book()
        if item is None:
            return False
        self._model.view.show_msg("Enter the new title of the book or press Enter to skip:")
        title = input()
        self._model.view.show_msg("Enter the new author of the book or press Enter to skip:")
        author = input()
        while True:
            try:
                self._model.view.show_msg("Enter the new price of the book or enter -1 to skip:")
                price = float(input())
                if price == -1:
                    break
                if price < 0:
                    self._model.view.show_error("Price cannot be negative. Please enter a valid price.")
                    continue
                break
            except ValueError:
                self._model.view.show_error("It is not float value. Enter valid float value.")
        self._model.view.show_msg("Enter the new genre of the book:")
        genre = input()
        return self._model.edit_book(old_title=item["title"], old_author=item["author"],
                                     old_price=item["price"], old_genre=item["genre"],
                                     title=title, author=author, price=price, genre=genre)


    def event_edit_author(self) -> bool:
        item = self._choose_author()
        if item is None:
            return False
        self._model.view.show_msg("Enter the new name of the author:")
        author = input()
        self._model.view.show_msg("Enter the new biography of the author:")
        biography = input()
        return self._model.edit_author(old_name=item["name"], old_biography=item["biography"],
                                       name=author, biography=biography)

    def event_delete_book(self) -> bool:
        item = self._choose_book()
        self._model.view.show_msg("Enter how many copies of book you want to delete:")
        copies = -1
        while copies <= 0:
            try:
                self._model.view.show_msg("Enter the number of book you want to reserve (greater than 0):")
                copies = int(input())
            except ValueError:
                self._model.view.show_error("It is not int value. Enter valid int value.")
        return self._model.delete_book(title=item["title"], author=item["author"],
                                       price=item["price"], genre=item["genre"], copies=copies)

    def event_delete_author(self) -> bool:
        item = self._choose_author()
        if item is None:
            return False
        return self._model.delete_author(author=item["name"])

class UserController(IUserController):
    def __init__(self,
                 model: IUserManager = None):
        self._model = model

    def event_login(self) -> bool:
        self._model.view.show_msg("Enter username:")
        username = input()
        self._model.view.show_msg("Enter password:")
        passw = input()
        return self._model.login(username=username, password=passw)

    def event_logout(self) -> bool:
        return self._model.logout()

    def event_register(self) -> bool:
        self._model.view.show_msg("Enter your username:")
        username = input()
        self._model.view.show_msg("Enter your email:")
        email = input()
        self._model.view.show_msg("Enter the administrator's code word (press Enter to skip):")
        status = True if input() == "ADMIN" else False
        passw = ''
        while len(passw) < 1:
            self._model.view.show_msg("Enter your password (at least 1 symbol):")
            passw = input()
        return self._model.new_user(username=username, email=email, status=status, password=passw)

    def event_update(self) -> bool:
        self._model.view.show_msg("Please enter new username or press Enter to skip:")
        username = input()
        self._model.view.show_msg("Please enter new email address or press Enter to skip:")
        email = input()
        self._model.view.show_msg("Please enter new password or press Enter to skip:")
        passw = input()
        return self._model.update_user(username=username,email=email,password=passw)

    def event_delete(self) -> bool:
        return self._model.delete_user()

