# views/login_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from database.conn import get_connection
from core.session import session

def try_login(username, password):
    conn = get_connection()
    if conn is None:
        return False, "Sin conexión a BD"
    try:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT username, password FROM usuarios WHERE username=%s", (username,))
                row = cur.fetchone()
                if row:
                    return (password == row[1], None)  # demo simple
                else:
                    return False, "Usuario no encontrado"
            except Exception:
                # si no existe tabla, modo demo
                if username == "admin" and password == "admin":
                    return True, None
                return False, "Demo: admin/admin"
    finally:
        try: conn.close()
        except: pass

class LoginView(ttk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master, padding=24)
        self.on_success = on_success
        ttk.Label(self, text="Censo INEGI – Login", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0,14))

        ttk.Label(self, text="Usuario").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(self, text="Contraseña").grid(row=2, column=0, sticky="e", padx=6, pady=6)

        self.user = ttk.Entry(self, width=32)
        self.pwd = ttk.Entry(self, show="*", width=32)
        self.user.grid(row=1, column=1, pady=6)
        self.pwd.grid(row=2, column=1, pady=6)

        ttk.Button(self, text="Ingresar", command=self._login).grid(row=3, column=0, columnspan=2, pady=12)
        ttk.Label(self, text="Tip (demo): admin / admin", foreground="#666").grid(row=4, column=0, columnspan=2)

    def _login(self):
        ok, err = try_login(self.user.get().strip(), self.pwd.get().strip())
        if ok:
            session.login(self.user.get().strip())
            self.on_success()
        else:
            messagebox.showerror("Login", err or "Credenciales inválidas")
