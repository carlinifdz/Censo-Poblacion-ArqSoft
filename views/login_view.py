# views/login_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from core.session import session
from registro.usuarios import usuario

class LoginView(ttk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master, padding=24)
        self.on_success = on_success
        self.usuario_model = usuario()

        ttk.Label(self, text="Censo INEGI – Login", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 14)
        )

        ttk.Label(self, text="Usuario").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(self, text="Contraseña").grid(row=2, column=0, sticky="e", padx=6, pady=6)

        self.user = ttk.Entry(self, width=32)
        self.pwd = ttk.Entry(self, show="*", width=32)
        self.user.grid(row=1, column=1, pady=6)
        self.pwd.grid(row=2, column=1, pady=6)

        ttk.Button(self, text="Ingresar", command=self._login).grid(row=3, column=0, columnspan=2, pady=12)
        ttk.Button(self, text="Registrar usuario", command=self._open_register).grid(row=4, column=0, columnspan=2, pady=(0, 12))
        ttk.Label(self, text="Tip (demo): admin / admin", foreground="#666").grid(row=5, column=0, columnspan=2)

    # ---------- LOGIN ----------
    def _login(self):
        username = self.user.get().strip()
        password = self.pwd.get().strip()

        if not username or not password:
            messagebox.showwarning("Login", "Por favor, ingrese usuario y contraseña.")
            return

        ok = self.usuario_model.iniciar_sesion(username, password)

        if ok:
            session.login(username)
            self.on_success()
        else:
            messagebox.showerror("Login", "usuario o contraseña incorrectos.")

    # ---------- REGISTRO ----------
    def _open_register(self):
        """Abre una ventana modal para registrar un nuevo usuario"""
        reg_win = tk.Toplevel(self)
        reg_win.title("Registrar nuevo usuario")
        reg_win.resizable(False, False)
        reg_win.transient(self)
        reg_win.grab_set()  # bloquea la ventana principal hasta cerrar el registro

        ttk.Label(reg_win, text="Registro de usuario", font=("Segoe UI", 13, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(10, 15)
        )

        ttk.Label(reg_win, text="usuario").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(reg_win, text="Contraseña").grid(row=2, column=0, sticky="e", padx=6, pady=6)

        user_entry = ttk.Entry(reg_win, width=30)
        pwd_entry = ttk.Entry(reg_win, show="*", width=30)
        user_entry.grid(row=1, column=1, pady=6)
        pwd_entry.grid(row=2, column=1, pady=6)

        def registrar():
            user = user_entry.get().strip()
            pwd = pwd_entry.get().strip()

            if not user or not pwd:
                messagebox.showwarning("Registro", "Debe ingresar usuario y contraseña.")
                return

            ok = self.usuario_model.registrar_usuario(user, pwd)
            if ok:
                messagebox.showinfo("Registro", "usuario registrado correctamente.")
                reg_win.destroy()
            else:
                messagebox.showerror("Registro", "No se pudo registrar el usuario (puede que ya exista).")

        ttk.Button(reg_win, text="Registrar", command=registrar).grid(row=3, column=0, columnspan=2, pady=12)
