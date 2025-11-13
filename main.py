import customtkinter as ctk
from views2.login_view import LoginView
from views2.menu_view import MainMenu  # Asegúrate de mover tu ventana de menú a main_menu.py

def on_login_success(username):
    MainMenu(username)

if __name__ == "__main__":
    LoginView(on_success=on_login_success)
