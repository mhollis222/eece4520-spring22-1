from View.UI.login_window import LoginWindow
from Controller.client import ReversiClient
import threading
from Controller.message import ReversiMessage as msg

if __name__ == "__main__":
    client = ReversiClient()
    app = LoginWindow()
    app.mainloop()
