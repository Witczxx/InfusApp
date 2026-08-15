from infusapp.auth_nurse_ui import AuthNurseUi


class Main:
    def __init__(self):
        self.auth_nurse_ui = AuthNurseUi()

    def run(self):
        return self.auth_nurse_ui.start_screen()


if __name__ == "__main__":
    app = Main()
    app.run()
