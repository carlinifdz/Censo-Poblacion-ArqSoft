# views/registro_combinado_view.py
from tkinter import ttk, messagebox, simpledialog
from core.event_bus import bus
from database.conn import get_connection
from registro.domicilios import domicilio as DomicilioModel
from registro.habitantes import habitante as HabitanteModel

# ---------- Helpers de BD ----------
def fetch_ciudades():
    """Lista de municipios (colonias.localidad)."""
    conn = get_connection()
    if conn is None:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT localidad FROM colonias ORDER BY localidad")
            return [r[0] for r in cur.fetchall()]
    finally:
        try: conn.close()
        except: pass

def fetch_colonias_by_ciudad(ciudad):
    """[(id, 'Colonia - Ciudad')] filtrado por ciudad/localidad."""
    if not ciudad:
        return []
    conn = get_connection()
    if conn is None:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, nombre, localidad FROM colonias WHERE localidad=%s ORDER BY nombre",
                (ciudad,)
            )
            rows = cur.fetchall()
            return [(r[0], f"{r[1]} - {r[2]}") for r in rows]
    finally:
        try: conn.close()
        except: pass

class RegistroCombinadoView(ttk.Frame):
    TIPOS = ["Vivienda de concreto","Vivienda de adobe(antiguo)","Vivienda de ladrillo","Vivienda de madera",
             "Vivienda de cartón","Casa de piedra","Vivienda prefabricada","Material Ecológico",
             "Casa de paja, ramas o caña","Material Adobe Moderno"]

    def __init__(self, master, go_back):
        super().__init__(master, padding=18)
        self.go_back = go_back
        ttk.Label(self, text="Registro combinado (Domicilio + Habitante)",
                  font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=6, pady=(0,14), sticky="w")

        # ---------- Filtros por Ciudad -> Colonias ----------
        ttk.Label(self, text="Ciudad (municipio)").grid(row=1, column=0, sticky="e")
        self.ciudades = fetch_ciudades()
        self.ciudad = ttk.Combobox(self, values=self.ciudades, state="readonly", width=30)
        self.ciudad.grid(row=1, column=1, padx=6, pady=6, sticky="w")
        self.ciudad.bind("<<ComboboxSelected>>", self._refrescar_colonias)

        ttk.Label(self, text="Colonia").grid(row=1, column=2, sticky="e")
        self.colonia_map = []  # [(id, label)]
        self.colonia = ttk.Combobox(self, values=[], state="readonly", width=35)
        self.colonia.grid(row=1, column=3, padx=6, pady=6, sticky="w")

        ttk.Separator(self).grid(row=2, column=0, columnspan=6, sticky="ew", pady=8)

        # ---------- Sección Domicilio ----------
        ttk.Label(self, text="DOMICILIO", font=("Segoe UI", 12, "bold")).grid(row=3, column=0, sticky="w", pady=(4,0))
        ttk.Label(self, text="Tipo vivienda").grid(row=4, column=0, sticky="e")
        ttk.Label(self, text="Calle").grid(row=4, column=2, sticky="e")
        ttk.Label(self, text="Número").grid(row=4, column=4, sticky="e")

        self.tipo = ttk.Combobox(self, values=self.TIPOS, state="readonly", width=28)
        self.calle = ttk.Entry(self, width=28)
        self.numero = ttk.Entry(self, width=14)

        self.tipo.grid(row=4, column=1, padx=6, pady=6, sticky="w")
        self.calle.grid(row=4, column=3, padx=6, pady=6, sticky="w")
        self.numero.grid(row=4, column=5, padx=6, pady=6, sticky="w")

        # ---------- Sección Habitante ----------
        ttk.Label(self, text="HABITANTE", font=("Segoe UI", 12, "bold")).grid(row=5, column=0, sticky="w", pady=(4,0))
        ttk.Label(self, text="Nombre").grid(row=6, column=0, sticky="e")
        ttk.Label(self, text="Fecha nac. (YYYY-MM-DD)").grid(row=6, column=2, sticky="e")
        ttk.Label(self, text="Sexo (F/M/X)").grid(row=6, column=4, sticky="e")
        ttk.Label(self, text="Actividad económica").grid(row=7, column=0, sticky="e")

        self.nombre = ttk.Entry(self, width=28)
        self.fecha = ttk.Entry(self, width=18)
        self.sexo = ttk.Combobox(self, values=["F","M","X"], state="readonly", width=5)
        self.act = ttk.Entry(self, width=40)

        self.nombre.grid(row=6, column=1, padx=6, pady=6, sticky="w")
        self.fecha.grid(row=6, column=3, padx=6, pady=6, sticky="w")
        self.sexo.grid(row=6, column=5, padx=6, pady=6, sticky="w")
        self.act.grid(row=7, column=1, padx=6, pady=6, sticky="w", columnspan=3)

        # ---------- Botones combinados ----------
        ttk.Button(self, text="Registrar (auto crea domicilio si no existe)", command=self.registrar_combinado)\
            .grid(row=8, column=1, padx=6, pady=10, sticky="ew", columnspan=2)

        ttk.Button(self, text="Editar domicilio", command=self.editar_domicilio)\
            .grid(row=8, column=3, padx=6, pady=10, sticky="ew")

        ttk.Button(self, text="Eliminar domicilio", command=self.eliminar_domicilio)\
            .grid(row=8, column=4, padx=6, pady=10, sticky="ew")

        ttk.Button(self, text="Editar habitante", command=self.editar_habitante)\
            .grid(row=9, column=1, padx=6, pady=4, sticky="ew")

        ttk.Button(self, text="Eliminar habitante", command=self.eliminar_habitante)\
            .grid(row=9, column=2, padx=6, pady=4, sticky="ew")

        ttk.Separator(self).grid(row=10, column=0, columnspan=6, sticky="ew", pady=10)
        ttk.Button(self, text="Volver al menú", command=self.go_back).grid(row=11, column=0, columnspan=6, pady=6)

        # modelos (de tu compañero)
        self.dom_model = DomicilioModel()
        self.hab_model = HabitanteModel()

    # ---------- Utils ----------
    def _refrescar_colonias(self, *_):
        ciudad = self.ciudad.get()
        self.colonia_map = fetch_colonias_by_ciudad(ciudad)
        self.colonia["values"] = [c[1] for c in self.colonia_map]
        self.colonia.set("")

    def _colonia_id_sel(self):
        i = self.colonia.current()
        return None if i < 0 else self.colonia_map[i][0]

    def _dom_id_by_inputs(self):
        """Busca domicilio por (calle, numero, colonia_id)."""
        cid = self._colonia_id_sel()
        if not cid: return None
        res = self.dom_model.buscar_domicilio(self.calle.get().strip(), self.numero.get().strip(), cid)
        if not res: return None
        return res[0] if isinstance(res, tuple) else res.get("id")

    # ---------- Registrar combinado ----------
    def registrar_combinado(self):
        # Validación básica
        if not (self.ciudad.get() and self._colonia_id_sel() and self.calle.get() and self.numero.get() and
                self.tipo.get() and self.nombre.get() and self.sexo.get()):
            messagebox.showwarning("Validación","Completa ciudad, colonia, domicilio y datos del habitante.")
            return

        colonia_id = self._colonia_id_sel()

        # 1) Buscar domicilio
        dom_id = self._dom_id_by_inputs()

        # 2) Si no existe, crear domicilio con el CRUD de tu compañero
        if not dom_id:
            ok_dom = self.dom_model.registrar_domicilio(
                self.tipo.get(), self.calle.get().strip(), self.numero.get().strip(), colonia_id
            )
            if not ok_dom:
                messagebox.showerror("Domicilio","No se pudo registrar el domicilio.")
                return
            # volver a buscar para obtener el id
            dom_id = self._dom_id_by_inputs()
            if not dom_id:
                messagebox.showerror("Domicilio","No se encontró el domicilio recién creado.")
                return
            bus.emit("domicilio_changed")

        # 3) Registrar habitante usando el dom_id
        ok_hab = self.hab_model.registrar_habitante(
            self.nombre.get().strip(),
            self.fecha.get().strip() or None,
            self.sexo.get(),
            dom_id,
            self.act.get().strip() or None
        )
        messagebox.showinfo("Registro", "Combinado registrado" if ok_hab else "No se registró el habitante")
        if ok_hab:
            bus.emit("habitante_changed")

    # ---------- CRUD “rápido” con métodos del compa ----------
    def editar_domicilio(self):
        cid = self._colonia_id_sel()
        if not (cid and self.calle.get() and self.numero.get()):
            messagebox.showwarning("Domicilio","Indica colonia, calle y número.")
            return
        ok = self.dom_model.editar_domicilio(
            self.calle.get().strip(), self.numero.get().strip(), cid, nuevo_tipo_casa=self.tipo.get() or None
        )
        messagebox.showinfo("Domicilio", "Actualizado" if ok else "No se actualizó")
        if ok: bus.emit("domicilio_changed")

    def eliminar_domicilio(self):
        cid = self._colonia_id_sel()
        if not (cid and self.calle.get() and self.numero.get()):
            messagebox.showwarning("Domicilio","Indica colonia, calle y número.")
            return
        if not messagebox.askyesno("Confirmar","¿Eliminar domicilio? (También podría afectar habitantes vinculados)"):
            return
        ok = self.dom_model.eliminar_domicilio(self.calle.get().strip(), self.numero.get().strip(), cid)
        messagebox.showinfo("Domicilio", "Eliminado" if ok else "No se eliminó")
        if ok: bus.emit("domicilio_changed")

    def editar_habitante(self):
        cid = self._colonia_id_sel()
        if not (cid and self.nombre.get()):
            messagebox.showwarning("Habitante","Indica colonia y nombre para localizar.")
            return
        dom_id = self._dom_id_by_inputs()
        if not dom_id:
            messagebox.showerror("Habitante","No se encontró el domicilio actual.")
            return
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

    def eliminar_habitante(self):
        cid = self._colonia_id_sel()
        if not (cid and self.nombre.get()):
            messagebox.showwarning("Habitante","Indica colonia y nombre.")
            return
        dom_id = self._dom_id_by_inputs()
        if not dom_id:
            messagebox.showerror("Habitante","No se encontró el domicilio asociado.")
            return
        ok = self.hab_model.eliminar_habitante(self.nombre.get().strip(), domicilio_id=dom_id)
        messagebox.showinfo("Habitante", "Eliminado" if ok else "No se eliminó")
        if ok: bus.emit("habitante_changed")
