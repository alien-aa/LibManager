from views.imanagerview import IManagerView

class ManagerView(IManagerView):
    def show_msg(self, msg: str = "") -> None:
        print(msg)

    def show_error(self, msg: str = "") -> None:
        print(f"\033[31mERROR:\033[0m {msg}")