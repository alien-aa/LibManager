class Book:
    def __init__(self,
                 title: str = "",
                 author: str = "",
                 price: float = 0.0,
                 genre: str = "",
                 copies: int = 1):
        self._title = title
        self._author = author
        self._price = price
        self._genre = genre
        self._copies = copies
        self._borrowed_copies = 0

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str = "") -> None:
        self._title = value

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, value: str = "") -> None:
        self._author = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float = 0.0) -> None:
        self._price = value

    @property
    def genre(self) -> str:
        return self._genre

    @genre.setter
    def genre(self, value: str = "") -> None:
        self._genre = value

    @property
    def copies(self) -> int:
        return self._copies

    @copies.setter
    def copies(self, value: int = 0) -> None:
        self._copies = value

    @property
    def borrowed_copies(self) -> int:
        return self._borrowed_copies

    @borrowed_copies.setter
    def borrowed_copies(self, value: int = 0) -> None:
        self._borrowed_copies = value

    def to_dict(self) -> dict:
        return { "title" : self.title,
                 "author" : self.author,
                 "price" : self.price,
                 "genre" : self.genre,
                 "copies" : self.copies,
                 "borrowed_copies" : self.borrowed_copies }

    def from_dict(self, data: dict) -> None:
        self.title = data["title"]
        self.author = data["author"]
        self.price = data["price"]
        self.genre = data["genre"]
        self.copies = data["copies"]
        self.borrowed_copies = data["borrowed_copies"]
        return

    def __str__(self) -> str:
        return (f"* Title: {self.title}\n"
                f"* Author: {self.author}\n"
                f"* Price: {self.price:.2f} ₽\n"
                f"* Genre: {self.genre}\n"
                f"* Available Copies: {self.copies}\n"
                f"* Borrowed Copies: {self.borrowed_copies}\n")