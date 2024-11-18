import xml.etree.ElementTree as Et

from providers.iprovider import ILibProvider, IUserProvider


class XmlLibProvider(ILibProvider):
    def __init__(self, filepath: str = ""):
        self._filepath = filepath

    def load(self) -> list[dict]:
        authors = []
        try:
            tree = Et.parse(self._filepath)
            root = tree.getroot()
            for author_elem in root.findall('author'):
                new_author = {"name": author_elem.find('name').text,
                              "biography": author_elem.find('biography').text,
                              "books": []}
                for book_elem in author_elem.findall('book'):
                    new_book = {"title": book_elem.find('title').text,
                                "author": book_elem.find('author').text,
                                "price": float(book_elem.find('price').text),
                                "genre": book_elem.find('genre').text,
                                "copies": int(book_elem.find('copies').text),
                                "borrowed_copies": int(book_elem.find('borrowed_copies').text)}
                    new_author["books"].append(new_book)
                authors.append(new_author)
            return authors
        except FileNotFoundError:
            return []
        except Et.ParseError:
            return []

    def save(self, data: list[dict]) -> None:
        try:
            root = Et.Element('library')
            for item in data:
                author_elem = Et.SubElement(root, 'author')
                Et.SubElement(author_elem, 'name').text = item["name"]
                Et.SubElement(author_elem, 'biography').text = item["biography"]
                for book in item["books"]:
                    book_elem = Et.SubElement(author_elem, 'book')
                    Et.SubElement(book_elem, 'title').text = book["title"]
                    Et.SubElement(book_elem, 'author').text = book["author"]
                    Et.SubElement(book_elem, 'price').text = str(book["price"])
                    Et.SubElement(book_elem, 'genre').text = book["genre"]
                    Et.SubElement(book_elem, 'copies').text = str(book["copies"])
                    Et.SubElement(book_elem, 'borrowed_copies').text = str(book["borrowed_copies"])
            tree = Et.ElementTree(root)
            tree.write(self._filepath, encoding='utf-8', xml_declaration=True)
            return
        except IOError:
            return

class XmlUserProvider(IUserProvider):
    def __init__(self, filepath: str = ""):
        self._filepath = filepath

    def load(self) -> list[dict]:
        users = []
        try:
            tree = Et.parse(self._filepath)
            root = tree.getroot()
            for user_elem in root.findall('user'):
                new_user = {"username": user_elem.find('username').text,
                            "email": user_elem.find('email').text,
                            "admin": user_elem.find('admin').text.lower() == 'true',
                            "password_hash": user_elem.find('password_hash').text,
                            "currently_borrowed": []}
                for book_elem in user_elem.findall('currently_borrowed/book'):
                    new_book = {"title": book_elem.find('title').text,
                                "author": book_elem.find('author').text,
                                "price": float(book_elem.find('price').text),
                                "genre": book_elem.find('genre').text,
                                "copies": int(book_elem.find('copies').text),
                                "borrowed_copies": int(book_elem.find('borrowed_copies').text)}
                    new_user["currently_borrowed"].append(new_book)
                users.append(new_user)
            return users
        except FileNotFoundError:
            return []
        except Et.ParseError:
            return []

    def save(self, data: list[dict]) -> None:
        try:
            root = Et.Element('users')
            for item in data:
                user_elem = Et.SubElement(root, 'user')
                Et.SubElement(user_elem, 'username').text = item["username"]
                Et.SubElement(user_elem, 'email').text = item["email"]
                Et.SubElement(user_elem, 'admin').text = str(item["admin"]).lower()
                Et.SubElement(user_elem, 'password_hash').text = item["password_hash"]
                borrowed_elem = Et.SubElement(user_elem, 'currently_borrowed')
                for book in item["currently_borrowed"]:
                    book_elem = Et.SubElement(borrowed_elem, 'book')
                    Et.SubElement(book_elem, 'title').text = book["title"]
                    Et.SubElement(book_elem, 'author').text = book["author"]
                    Et.SubElement(book_elem, 'price').text = str(book["price"])
                    Et.SubElement(book_elem, 'genre').text = book["genre"]
                    Et.SubElement(book_elem, 'copies').text = str(book["copies"])
                    Et.SubElement(book_elem, 'borrowed_copies').text = str(book["borrowed_copies"])
            tree = Et.ElementTree(root)
            tree.write(self._filepath, encoding='utf-8', xml_declaration=True)
            return
        except IOError:
            return
