# views/habitantes_view.py
from tkinter import ttk, messagebox, simpledialog
from core.event_bus import bus
from database.conn import get_connection
from registro.domicilios import domicilio as DomicilioModel
from registro.habitantes import habitante as HabitanteModel

def fetch_colonias_combo():
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

class HabitantesView(ttk.Frame):
    def __init__(self, master, go_back):
        super().__init__(master, padding=18)
        self.go_back = go_back
        ttk.Label(self, text="Habitantes (CRUD)", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=4, pady=(0,14), sticky="w")

        ttk.Label(self, text="Nombre").grid(row=1, column=0, sticky="e")
        ttk.Label(self, text="Fecha nac. (YYYY-MM-DD)").grid(row=1, column=2, sticky="e")
        ttk.Label(self, text="Sexo (F/M/X)").grid(row=2, column=0, sticky="e")
        ttk.Label(self, text="Colonia").grid(row=2, column=2, sticky="e")
        ttk.Label(self, text="Actividad económica").grid(row=3, column=0, sticky="e")

        self.nombre = ttk.Entry(self, width=35)
        self.fecha = ttk.Entry(self, width=20)
        self.sexo = ttk.Combobox(self, values=["F","M","X"], state="readonly", width=5)
        self.colonia_map = fetch_colonias_combo()
        self.colonia = ttk.Combobox(self, values=[c[1] for c in self.colonia_map], state="readonly", width=40)
        self.act = ttk.Entry(self, width=40)

        self.nombre.grid(row=1, column=1, padx=6, pady=6, sticky="w")
        self.fecha.grid(row=1, column=3, padx=6, pady=6, sticky="w")
        self.sexo.grid(row=2, column=1, padx=6, pady=6, sticky="w")
        self.colonia.grid(row=2, column=3, padx=6, pady=6, sticky="w")
        self.act.grid(row=3, column=1, padx=6, pady=6, sticky="w")

        ttk.Button(self, text="Registrar", command=self.registrar).grid(row=4, column=1, padx=6, pady=10, sticky="ew")
        ttk.Button(self, text="Editar", command=self.editar).grid(row=4, column=2, padx=6, pady=10, sticky="ew")
        ttk.Button(self, text="Eliminar", command=self.eliminar).grid(row=4, column=3, padx=6, pady=10, sticky="ew")
        ttk.Separator(self).grid(row=5, column=0, columnspan=4, sticky="ew", pady=10)
        ttk.Button(self, text="Volver al menú", command=self.go_back).grid(row=6, column=0, columnspan=4, pady=6)

        self.dom_model = DomicilioModel()
        self.hab_model = HabitanteModel()

    def _domicilio_id(self, calle, numero, colonia_id):
        res = self.dom_model.buscar_domicilio(calle, numero, colonia_id)
        if not res: return None
        return res[0] if isinstance(res, tuple) else res.get("id")

    def _ask_dom(self, titulo):
        calle = simpledialog.askstring("Domicilio", f"Calle ({titulo})", parent=self)
        numero = simpledialog.askstring("Domicilio", f"Número ({titulo})", parent=self)
        if not calle or not numero: return None, None, None
        if self.colonia.current() < 0: return None, None, None
        colonia_id = self.colonia_map[self.colonia.current()][0]
        return calle.strip(), numero.strip(), colonia_id

    def registrar(self):
        if not (self.nombre.get() and self.sexo.get() and self.colonia.current() >= 0):
            messagebox.showwarning("Validación","Completa nombre, sexo y colonia.")
            return
        calle, numero, colonia_id = self._ask_dom("para asociar")
        if not calle: return
        dom_id = self._domicilio_id(calle, numero, colonia_id)
        if not dom_id:
            messagebox.showerror("Habitante","Primero registra ese domicilio.")
            return
        ok = self.hab_model.registrar_habitante(
            self.nombre.get().strip(),
            self.fecha.get().strip() or None,
            self.sexo.get(),
            dom_id,
            self.act.get().strip() or None
        )
        messagebox.showinfo("Habitante", "Registrado" if ok else "No se registró")
        if ok: bus.emit("habitante_changed")

    def editar(self):
        if not (self.nombre.get() and self.colonia.current() >= 0):
            messagebox.showwarning("Validación","Indica nombre y colonia.")
            return
        calle, numero, colonia_id = self._ask_dom("actual")
        if not calle: return
        dom_id = self._domicilio_id(calle, numero, colonia_id)
        ok = self.hab_model.editar_habitante(
            self.nombre.get().strip(),
            domicilio_id=dom_id,
            nuevo_nombre=self.nombre.get().strip(),
            nuevo_sexo=self.sexo.get() or None,
            nuevo_act_eco=self.act.get().strip() or None,
            nuevo_fecha_nac=self.fecha.get().strip() or None
        )
        messagebox.showinfo("Habitante", "Actualizado" if ok else "No se actualizó")
        if ok: bus.emit("habitante_changed")

    def eliminar(self):
        if not (self.nombre.get() and self.colonia.current() >= 0):
            messagebox.showwarning("Validación","Indica nombre y colonia.")
            return
        calle, numero, colonia_id = self._ask_dom("del registro")
        if not calle: return
        dom_id = self._domicilio_id(calle, numero, colonia_id)
        ok = self.hab_model.eliminar_habitante(self.nombre.get().strip(), domicilio_id=dom_id)
        messagebox.showinfo("Habitante", "Eliminado" if ok else "No se eliminó")
        if ok: bus.emit("habitante_changed")
