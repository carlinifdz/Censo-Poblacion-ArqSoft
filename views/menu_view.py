# views/menu_view.py
from tkinter import ttk

class MenuView(ttk.Frame):
    def __init__(self, master, username,
                 go_domicilios, go_habitantes, go_reportes,
                 go_registro,                    # ← NUEVO parámetro
                 do_logout, do_exit):
        super().__init__(master, padding=24)

        self.go_domicilios = go_domicilios
        self.go_habitantes = go_habitantes
        self.go_reportes  = go_reportes
        self.go_registro  = go_registro       # ← GUARDA el callback
        self.do_logout    = do_logout
        self.do_exit      = do_exit

        ttk.Label(self, text=f"Menú principal — Usuario: {username}",
                  font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=(0,14))

        ttk.Button(self, text="CRUD Domicilios", command=self.go_domicilios)\
            .grid(row=1, column=0, sticky="ew", padx=6, pady=6)
        ttk.Button(self, text="CRUD Habitantes", command=self.go_habitantes)\
            .grid(row=1, column=1, sticky="ew", padx=6, pady=6)
        ttk.Button(self, text="Reportes y Gráficas", command=self.go_reportes)\
            .grid(row=1, column=2, sticky="ew", padx=6, pady=6)

        # ← NUEVO botón para tu vista combinada
        ttk.Button(self, text="Registro combinado", command=self.go_registro)\
            .grid(row=2, column=0, sticky="ew", padx=6, pady=6, columnspan=3)

        ttk.Separator(self).grid(row=3, column=0, columnspan=3, sticky="ew", pady=10)

        ttk.Button(self, text="Cerrar sesión", command=self.do_logout)\
            .grid(row=4, column=1, sticky="ew", padx=6, pady=6)
        ttk.Button(self, text="Salir", command=self.do_exit)\
            .grid(row=4, column=2, sticky="ew", padx=6, pady=6)
