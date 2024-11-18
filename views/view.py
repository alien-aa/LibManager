import inquirer
import os
import time

from views.iview import IView
from controllers.icontroller import IUserController, ILibController

class View(IView):
    def __init__(self,
                 lib_controller: ILibController = None,
                 user_controller: IUserController = None):
        self._lib_controller = lib_controller
        self._user_controller = user_controller

    def main_menu(self) -> None:
        while True:
            os.system('cls')
            question_menu = [
                inquirer.List(
                    "selection_menu",
                    message="=== Library Management ===",
                    choices=[
                        "Account Management",
                        "Library Management",
                        "Exit",
                    ],
                )
            ]
            answer = inquirer.prompt(question_menu)
            selection_menu = answer.get("selection_menu")
            if selection_menu == "Account Management":
                self.user_menu()
            elif selection_menu == "Library Management":
                self.lib_menu()
            elif selection_menu == "Exit":
                os.system('cls')
                break

    def lib_menu(self) -> None:
        while True:
            os.system('cls')
            question_menu = [
                inquirer.List(
                    "selection_menu",
                    message="=== Library Management ===",
                    choices=[
                        "Search Book",
                        "Search Author",
                        "Reserve Book",
                        "Return Book",
                        "Add New Book (admin only)",
                        "Add New Author (admin only)",
                        "Edit Book Fields (admin only)",
                        "Edit Author Fields (admin only)",
                        "Delete Book (admin only)",
                        "Delete Author (admin only)",
                        "Back to Main Menu"
                    ],
                )
            ]
            answer = inquirer.prompt(question_menu)
            selection_menu = answer.get("selection_menu")
            os.system('cls')
            if selection_menu == "Search Book":
                if not self._lib_controller.event_search_book():
                    time.sleep(2)
                    continue
            elif selection_menu == "Search Author":
                if not self._lib_controller.event_search_author():
                    time.sleep(2)
                    continue
            elif selection_menu == "Reserve Book":
                if not self._lib_controller.event_reserve():
                    time.sleep(2)
                    continue
            elif selection_menu == "Return Book":
                if not self._lib_controller.event_return():
                    time.sleep(2)
                    continue
            elif selection_menu == "Add New Book (admin only)":
                if not self._lib_controller.event_add_book():
                    time.sleep(2)
                    continue
            elif selection_menu == "Add New Author (admin only)":
                if not self._lib_controller.event_add_author():
                    time.sleep(2)
                    continue
            elif selection_menu == "Edit Book Fields (admin only)":
                if not self._lib_controller.event_edit_book():
                    time.sleep(2)
                    continue
            elif selection_menu == "Edit Author Fields (admin only)":
                os.system('cls')
                if not self._lib_controller.event_edit_author():
                    time.sleep(2)
                    continue
            elif selection_menu == "Delete Book (admin only)":
                if not self._lib_controller.event_delete_book():
                    time.sleep(2)
                    continue
            elif selection_menu == "Delete Author (admin only)":
                if not self._lib_controller.event_delete_author():
                    time.sleep(2)
                    continue
            elif selection_menu == "Back to Main Menu":
                os.system('cls')
                break

    def user_menu(self) -> None:
        while True:
            os.system('cls')
            question_menu = [
                inquirer.List(
                    "selection_menu",
                    message="=== Account Management ===",
                    choices=[
                        "Login",
                        "Logout",
                        "Register",
                        "Update User Info",
                        "Delete Account",
                        "Back to Main Menu"
                    ],
                )
            ]
            answer = inquirer.prompt(question_menu)
            selection_menu = answer.get("selection_menu")
            os.system('cls')
            #TODO: после реализации контроллера подумать, когда какую задержку надо ставить
            if selection_menu == "Login":
                if not self._user_controller.event_login():
                    time.sleep(2)
                    continue
            elif selection_menu == "Logout":
                self._user_controller.event_logout()
                time.sleep(2)
                continue
            elif selection_menu == "Register":
                if not  self._user_controller.event_register():
                    time.sleep(2)
                    continue
            elif selection_menu == "Update User Info":
                self._user_controller.event_update()
                time.sleep(2)
                continue
            elif selection_menu == "Delete Account":
                if not  self._user_controller.event_delete():
                    time.sleep(2)
                    continue
            elif selection_menu == "Back to Main Menu":
                os.system('cls')
                break
