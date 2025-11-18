import customtkinter as ctk
from views.login_view import LoginView
from views.menu_view import MainMenu

def on_login_success(username):
    MainMenu(username)

if __name__ == "__main__":
    LoginView(on_success=on_login_success)