from auth_ui import Auth_Ui


class Main:
    def __init__(self):
        self.auth_ui = Auth_Ui()

    def run(self):
        return self.auth_ui.start_screen()


if __name__ == "__main__":
    app = Main()
    app.run()
