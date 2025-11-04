from tkinter import ttk, messagebox
import pandas as pd
from database.conn import get_connection
from core.event_bus import bus

class ReportesView(ttk.Frame):
    def __init__(self, master, go_back):
        super().__init__(master, padding=18)
        self.go_back = go_back
        ttk.Label(self, text="Reportes y Gráficas", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, columnspan=6, pady=(0,14), sticky="w"
        )

        # ---------- Filtros ----------
        ttk.Label(self, text="Ciudad").grid(row=1, column=0, sticky="e")
        ttk.Label(self, text="Colonia").grid(row=1, column=2, sticky="e")
        ttk.Label(self, text="Tipo vivienda").grid(row=1, column=4, sticky="e")

        self.ciudad = ttk.Combobox(self, width=20, state="readonly")
        self.colonia = ttk.Combobox(self, width=20)
        self.tipo = ttk.Combobox(self, width=25)

        self.ciudad.grid(row=1, column=1, padx=6, pady=4, sticky="w")
        self.colonia.grid(row=1, column=3, padx=6, pady=4, sticky="w")
        self.tipo.grid(row=1, column=5, padx=6, pady=4, sticky="w")

        ttk.Button(self, text="Aplicar filtro", command=self.refresh_all).grid(row=2, column=1, padx=6, pady=6, sticky="ew")
        ttk.Button(self, text="Limpiar", command=self._limpiar_filtros).grid(row=2, column=2, padx=6, pady=6, sticky="ew")
        ttk.Button(self, text="Actualizar", command=lambda: self.refresh_all()).grid(row=2, column=3, padx=6, pady=6, sticky="ew")
        ttk.Button(self, text="Volver al menú", command=self.go_back).grid(row=2, column=5, padx=6, pady=6, sticky="e")

        ttk.Separator(self).grid(row=3, column=0, columnspan=6, sticky="ew", pady=10)

        # ---------- Matplotlib embebido ----------
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure
        self.Figure = Figure
        self.FigureCanvasTkAgg = FigureCanvasTkAgg
        self.canvas = None

        # ---------- Tabla de resultados ----------
        cols = ("nombre", "cantidad")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=8)
        self.tabla.heading("nombre", text="Ciudad / Categoría")
        self.tabla.heading("cantidad", text="Cantidad")
        self.tabla.column("nombre", width=220)
        self.tabla.column("cantidad", width=100, anchor="center")
        self.tabla.grid(row=4, column=0, columnspan=6, pady=10, sticky="ew")

        # ---------- Inicialización ----------
        self.colonia_map = []  # [(id, nombre)] cache de colonias filtradas
        self._cargar_opciones()
        bus.subscribe("domicilio_changed", lambda: self.refresh_all())
        bus.subscribe("habitante_changed", lambda: self.refresh_all())

        # Eventos dinámicos
        self.ciudad.bind("<<ComboboxSelected>>", self._refrescar_colonias)
        self.colonia.bind("<KeyRelease>", self._filtrar_colonias)

        self.refresh_all()

    # ---------- Helpers de BD ----------
    def _query(self, sql, params=None):
        conn = get_connection()
        if conn is None:
            messagebox.showerror("BD","Sin conexión a la base de datos.")
            return []
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params or ())
                return cur.fetchall()
        finally:
            try: conn.close()
            except: pass

    def _cargar_opciones(self):
        """Carga valores iniciales en los combobox."""
        ciudades = [r[0] for r in self._query("SELECT DISTINCT localidad FROM colonias ORDER BY localidad")]
        tipos = [r[0] for r in self._query("SELECT DISTINCT tipo_casa FROM domicilios ORDER BY tipo_casa")]
        self.ciudad["values"] = ciudades
        self.tipo["values"] = tipos
        self.colonia["values"] = []  # se llenará dinámicamente

    # ---------- Nuevos métodos de filtrado dinámico ----------
    def _refrescar_colonias(self, *_):
        """Carga las colonias correspondientes a la ciudad seleccionada."""
        ciudad = self.ciudad.get()
        if not ciudad:
            self.colonia_map = []
            self.colonia["values"] = []
            return
        rows = self._query(
            "SELECT id, nombre FROM colonias WHERE localidad=%s ORDER BY nombre",
            (ciudad,)
        )
        self.colonia_map = rows
        self.colonia["values"] = [r[1] for r in rows]
        self.colonia.set("")

    def _filtrar_colonias(self, event):
        """Filtra las colonias a medida que se escribe en el Combobox."""
        texto = self.colonia.get().lower().strip()
        if not texto:
            self.colonia["values"] = [c[1] for c in self.colonia_map]
            return
        filtradas = [c[1] for c in self.colonia_map if texto in c[1].lower()]
        self.colonia["values"] = filtradas

    # ---------- Reportes ----------
    def _plot(self, labels, values, title):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        fig = self.Figure(figsize=(7.5, 4.2), dpi=100)
        ax = fig.add_subplot(111)
        bars = ax.bar(labels, values)
        ax.set_title(title)
        ax.tick_params(axis='x', rotation=30)
        fig.subplots_adjust(bottom=0.25, left=0.1, right=0.95, top=0.9)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.05*max(values), f"{int(height)}",
                    ha='center', va='bottom', fontsize=9)

        self.canvas = self.FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=6, pady=10)

    def _where_filtros(self):
        where = []
        params = []

        if self.ciudad.get():
            where.append("c.localidad = %s")
            params.append(self.ciudad.get())
        if self.colonia.get():
            where.append("c.nombre = %s")
            params.append(self.colonia.get())
        if self.tipo.get():
            where.append("d.tipo_casa = %s")
            params.append(self.tipo.get())

        return ("WHERE " + " AND ".join(where)) if where else "", tuple(params)

    def reporte_tipos(self):
        where, params = self._where_filtros()
        sql = f"""
            SELECT d.tipo_casa, COUNT(*) as total
            FROM domicilios d
            JOIN colonias c ON c.id = d.colonia_id
            {where}
            GROUP BY d.tipo_casa
            ORDER BY total DESC
        """
        rows = self._query(sql, params)
        if not rows:
            return
        labels = [r[0] for r in rows]
        values = [r[1] for r in rows]
        self._plot(labels, values, "Viviendas por tipo (filtradas)")
        self._actualizar_tabla(rows)

    def reporte_municipios(self):
        where, params = self._where_filtros()
        sql = f"""
            SELECT c.localidad AS municipio, COUNT(h.id) AS total_habitantes
            FROM habitantes h
            JOIN domicilios d ON d.id = h.domicilio_id
            JOIN colonias c ON c.id = d.colonia_id
            {where}
            GROUP BY c.localidad
            ORDER BY total_habitantes DESC
            LIMIT 12
        """
        rows = self._query(sql, params)
        if not rows:
            return
        labels = [r[0] for r in rows]
        values = [r[1] for r in rows]
        self._plot(labels, values, "Habitantes por municipio (Top 12 / filtrado)")
        self._actualizar_tabla(rows)

    def _actualizar_tabla(self, rows):
        # Limpiar tabla previa
        for i in self.tabla.get_children():
            self.tabla.delete(i)

        total = 0
        for nombre, cantidad in rows:
            self.tabla.insert("", "end", values=(nombre, cantidad))
            total += cantidad or 0

        # Fila de total
        if rows:
            self.tabla.insert("", "end", values=("TOTAL", total))

    def _limpiar_filtros(self):
        self.ciudad.set("")
        self.colonia.set("")
        self.tipo.set("")
        self.colonia_map = []
        self.colonia["values"] = []
        self.refresh_all()

    def refresh_all(self):
        self.reporte_municipios()
