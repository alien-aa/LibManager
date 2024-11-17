from model.book import Book

class Author:
    def __init__(self,
                 name: str = "",
                 biography: str = "",
                 books: list[Book] = None):
        self._name = name
        self._biography = biography
        self._books = books if books is not None else []

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str = "") -> None:
        self._name = value

    @property
    def biography(self) -> str:
        return self._biography

    @biography.setter
    def biography(self, value: str = "") -> None:
        self._biography = value

    @property
    def books(self) -> list[Book]:
        return self._books

    @books.setter
    def books(self, value: list[Book] = None) -> None:
        self._books = value if value is not None else []

    def to_dict(self) -> dict:
        return { "name": self.name,
                 "biography": self.biography,
                 "books" : [item.to_dict() for item in self.books] }

    def from_dict(self, data: dict) -> None:
        self.name = data["name"]
        self.biography = data["biography"]
        for item in data["books"]:
            new_one = Book()
            new_one.from_dict(item)
            self.books.append(new_one)
        return

    def __str__(self) -> str:
        books_list = "\n".join(book.title for book in self.books) if self.books else 'The author has no books.'
        return (f"Author Name: {self.name}\n"
                f"Biography: {self.biography}\n"
                f"Books:\n{books_list}")
