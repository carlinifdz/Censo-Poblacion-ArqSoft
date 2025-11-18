import customtkinter as ctk
import config
from CTkMessagebox import CTkMessagebox
from core.session import session
from registro.usuarios import usuario

class LoginView():
    def __init__(self, on_success):
        self.usuario_model = usuario()
        self.on_success = on_success
        ctk.set_appearance_mode(config.appearance)

        self.root = ctk.CTk()
        self.root.title("Censo INEGI – Login")
        self.root.geometry("400x400")
        self.root.configure(fg_color=config.bg_color)

        frame = ctk.CTkFrame(self.root, corner_radius=12, fg_color=config.frame_color)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        font_title = config.font_title
        font = config.font
        text_color = config.text_color

        corner_radius = config.corner_radius
        button_color = config.button_color
        button_text_color = config.button_text_color
        pady = config.pady
        padx = config.padx

        ctk.CTkLabel(frame, text="Censo INEGI – Login", font=font_title, text_color=text_color).pack(pady=25)

        self.usr = ctk.CTkEntry(frame, placeholder_text="Usuario", width=250, font=font, corner_radius=corner_radius)
        self.usr.pack(padx=padx, pady=pady)
        self.pwd = ctk.CTkEntry(frame, placeholder_text="Contraseña", show="*", width=250, font=font, corner_radius=corner_radius)
        self.pwd.pack(pady=pady)

        ctk.CTkButton(frame, text="Ingresar", width=150, font=font, corner_radius=corner_radius,
                      fg_color=button_color, text_color=button_text_color, command=self._login).pack(pady=12)
        ctk.CTkButton(frame, text="Registrar usuario", width=150, font=font, corner_radius=corner_radius,
                      fg_color=button_color, text_color=button_text_color, command=self._register).pack(pady=12)

        self.root.mainloop()

    def _login(self):
        username = self.usr.get().strip()
        password = self.pwd.get().strip()

        if not username or not password:
            CTkMessagebox(title="Login", message="Por favor, ingrese usuario y contraseña.", icon="warning")
            return

        ok = self.usuario_model.iniciar_sesion(username, password)

        if ok:
            session.login(username)
            self.root.destroy()
            self.on_success(username)
        else:
            CTkMessagebox(title="Login", message="Usuario o contraseña incorrectos.", icon="warning")

    def _register(self):
        username = self.usr.get().strip()
        password = self.pwd.get().strip()

        if not username or not password:
            CTkMessagebox(title="Login", message="Por favor, ingrese usuario y contraseña.", icon="warning")
            return

        ok = self.usuario_model.registrar_usuario(username, password)

        if ok:
            session.login(username)
            self.root.destroy()
            self.on_success(username)
        else:
            CTkMessagebox(title="Login", message="Usuario o contraseña incorrectos.", icon="warning")