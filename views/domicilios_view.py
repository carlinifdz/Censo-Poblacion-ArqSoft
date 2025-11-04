# views/domicilios_view.py
from tkinter import ttk, messagebox
from core.event_bus import bus
from database.conn import get_connection
from registro.domicilios import domicilio as DomicilioModel

def fetch_colonias():
    conn = get_connection()
    if conn is None:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nombre, localidad FROM colonias ORDER BY localidad, nombre")
            rows = cur.fetchall()
            return [(r[0], f"{r[1]} - {r[2]}") for r in rows]
    finally:
        try: conn.close()
        except: pass

class DomiciliosView(ttk.Frame):
    TIPOS = ["Vivienda de concreto","Vivienda de adobe(antiguo)","Vivienda de ladrillo","Vivienda de madera",
             "Vivienda de cartón","Casa de piedra","Vivienda prefabricada","Material Ecológico",
             "Casa de paja, ramas o caña","Material Adobe Moderno"]

    def __init__(self, master, go_back):
        super().__init__(master, padding=18)
        self.go_back = go_back
        ttk.Label(self, text="Domicilios (CRUD)", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=4, pady=(0,14), sticky="w")

        ttk.Label(self, text="Tipo vivienda").grid(row=1, column=0, sticky="e")
        ttk.Label(self, text="Calle").grid(row=1, column=2, sticky="e")
        ttk.Label(self, text="Número").grid(row=2, column=2, sticky="e")
        ttk.Label(self, text="Colonia").grid(row=2, column=0, sticky="e")

        self.tipo = ttk.Combobox(self, values=self.TIPOS, state="readonly", width=35)
        self.calle = ttk.Entry(self, width=35)
        self.numero = ttk.Entry(self, width=20)
        self.colonia_map = fetch_colonias()
        self.colonia = ttk.Combobox(self, values=[c[1] for c in self.colonia_map], state="readonly", width=35)

        self.tipo.grid(row=1, column=1, padx=6, pady=6, sticky="w")
        self.calle.grid(row=1, column=3, padx=6, pady=6, sticky="w")
        self.numero.grid(row=2, column=3, padx=6, pady=6, sticky="w")
        self.colonia.grid(row=2, column=1, padx=6, pady=6, sticky="w")

        ttk.Button(self, text="Registrar", command=self.registrar).grid(row=3, column=1, padx=6, pady=10, sticky="ew")
        ttk.Button(self, text="Editar", command=self.editar).grid(row=3, column=2, padx=6, pady=10, sticky="ew")
        ttk.Button(self, text="Eliminar", command=self.eliminar).grid(row=3, column=3, padx=6, pady=10, sticky="ew")
        ttk.Separator(self).grid(row=4, column=0, columnspan=4, sticky="ew", pady=10)
        ttk.Button(self, text="Volver al menú", command=self.go_back).grid(row=5, column=0, columnspan=4, pady=6)

        self.model = DomicilioModel()

    def _selected_colonia_id(self):
        i = self.colonia.current()
        return None if i < 0 else self.colonia_map[i][0]

    def registrar(self):
        cid = self._selected_colonia_id()
        if not cid or not self.tipo.get() or not self.calle.get() or not self.numero.get():
            messagebox.showwarning("Validación","Completa todos los campos.")
            return
        ok = self.model.registrar_domicilio(self.tipo.get(), self.calle.get().strip(), self.numero.get().strip(), cid)
        messagebox.showinfo("Domicilio", "Registrado" if ok else "No se registró")
        if ok: bus.emit("domicilio_changed")

    def editar(self):
        cid = self._selected_colonia_id()
        if not cid or not self.calle.get() or not self.numero.get():
            messagebox.showwarning("Validación","Indica colonia, calle y número (registro a editar).")
            return
        ok = self.model.editar_domicilio(self.calle.get().strip(), self.numero.get().strip(), cid,
                                         nuevo_tipo_casa=self.tipo.get() or None)
        messagebox.showinfo("Domicilio", "Actualizado" if ok else "No se actualizó")
        if ok: bus.emit("domicilio_changed")

    def eliminar(self):
        cid = self._selected_colonia_id()
        if not cid or not self.calle.get() or not self.numero.get():
            messagebox.showwarning("Validación","Indica colonia, calle y número (registro a eliminar).")
            return
        ok = self.model.eliminar_domicilio(self.calle.get().strip(), self.numero.get().strip(), cid)
        messagebox.showinfo("Domicilio", "Eliminado" if ok else "No se eliminó")
        if ok: bus.emit("domicilio_changed")
