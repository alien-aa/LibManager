import json

from providers.iprovider import ILibProvider, IUserProvider


class JsonLibProvider(ILibProvider):
    def __init__(self, filepath: str = ""):
        self._filepath = filepath

    def load(self) -> list[dict]:
        try:
            with open(self._filepath, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def save(self, data: list[dict]) -> None:
        try:
            with open(self._filepath, 'w') as file:
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            return
        except IOError:
            return


class JsonUserProvider(IUserProvider):
    def __init__(self, filepath: str = ""):
        self._filepath = filepath

    def load(self) -> list[dict]:
        try:
            with open(self._filepath, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def save(self, data: list[dict]) -> None:
        try:
            with open(self._filepath, 'w') as file:
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            return
        except IOError as e:
            return