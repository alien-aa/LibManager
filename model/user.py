import bcrypt

from model.book import Book

class User:
    def __init__(self,
                 username: str = "",
                 email: str = "",
                 admin_flag: bool = False,
                 currently_borrowed: list[Book] = None,
                 password: str = ""):
        self._username = username
        self._email = email
        self._admin = admin_flag
        self._currently_borrowed = currently_borrowed if currently_borrowed is not None else []
        self._password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        self._username = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._email = value

    @property
    def admin(self) -> bool:
        return self._admin

    @admin.setter
    def admin(self, value: bool) -> None:
        self._admin = value

    @property
    def currently_borrowed(self) -> list[Book]:
        return self._currently_borrowed

    @currently_borrowed.setter
    def currently_borrowed(self, value: list[Book]) -> None:
        self._currently_borrowed = value

    @property
    def password_hash(self) -> bytes:
        return self._password_hash

    @password_hash.setter
    def password_hash(self, value_str: str) -> None:
        self._password_hash = bcrypt.hashpw(value_str.encode('utf-8'), bcrypt.gensalt())

    def load_password_hash(self, value_hash: bytes) -> None:
        self._password_hash = value_hash

    def __str__(self) -> str:
        books_list = "\n".join(book.title for book in self.currently_borrowed) if self.currently_borrowed else 'The user has no borrowed books.'
        return (f"Username: {self.username}\n"
                f"Email: {self.email}\n"
                f"Currently Borrowed Books: {books_list}")

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self._password_hash)

    def to_dict(self) -> dict:
        return { "username": self.username,
                 "email": self.email,
                 "admin": self.admin,
                 "currently_borrowed": [book.to_dict() for book in self.currently_borrowed],
                 "password_hash": self._password_hash.decode('utf-8') }

    def from_dict(self, data: dict) -> None:
        self.username = data["username"]
        self.email = data["email"]
        self.admin = data["admin"]
        for item in data["currently_borrowed"]:
            new_one = Book()
            new_one.from_dict(item)
            self.currently_borrowed.append(new_one)
        self.load_password_hash(data["password_hash"].encode('utf-8'))
        return


