import argparse

from model.author import Author
from model.user import User
from model.manager import LibManager, UserManager, Library

from views.view import View
from views.managerview import ManagerView

from controllers.controller import LibController, UserController

from providers.jsonprovider import JsonLibProvider, JsonUserProvider
from providers.xmlprovider import XmlLibProvider, XmlUserProvider


def main(lib_file: str = '', user_file: str = '') -> None:
    file_format_lib = lib_file.split('.')[-1].lower()
    file_format_users = user_file.split('.')[-1].lower()
    data_provider, user_provider = None, None
    if file_format_lib == 'json':
        data_provider = JsonLibProvider(lib_file)
    elif file_format_lib == 'xml':
        data_provider = XmlLibProvider(lib_file)
    else:
        print("Unsupported library file format!")
        return
    if file_format_users == 'json':
        user_provider = JsonUserProvider(user_file)
    elif file_format_users == 'xml':
        user_provider = XmlUserProvider(user_file)
    else:
        print("Unsupported users file format!")
        return
    lib = Library([], [], [], None)
    lib_manager = LibManager(library=lib, view=ManagerView(), provider=data_provider)
    user_manager = UserManager(library=lib, view=ManagerView(), provider=user_provider)
    print(lib_manager.provider)
    lib_data_load = lib_manager.provider.load()
    user_data_load = user_manager.provider.load()
    for item in lib_data_load:
        new_author = Author()
        new_author.from_dict(item)
        lib_manager.library.authors.append(new_author)
        for book in new_author.books:
            lib_manager.library.books.append(book)
    for item in user_data_load:
        new_user = User()
        new_user.from_dict(item)
        user_manager.library.users.append(new_user)
    main_view = View(LibController(lib_manager), UserController(user_manager))
    main_view.main_menu()
    lib_data_save = []
    user_data_save = []
    for item in lib_manager.library.authors:
        lib_data_save.append(item.to_dict())
    for item in user_manager.library.users:
        user_data_save.append(item.to_dict())
    lib_manager.provider.save(lib_data_save)
    user_manager.provider.save(user_data_save)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Library Manager")
    parser.add_argument("lib_file", type=str, help="Path to library file")
    parser.add_argument("user_file", type=str, help="Path to user file")
    args = parser.parse_args()
    main(args.lib_file, args.user_file)