
# views/reportes_view.py
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from database.conn import get_connection
from core.event_bus import bus

class ReportesView(ttk.Frame):
    def __init__(self, master, go_back):
        super().__init__(master, padding=18)
        self.go_back = go_back
        ttk.Label(self, text="Reportes y Gráficas", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=(0,14), sticky="w")

        ttk.Button(self, text="Conteo por tipo de vivienda", command=self.reporte_tipos).grid(row=1, column=0, padx=6, pady=6, sticky="ew")
        ttk.Button(self, text="Habitantes por municipio", command=self.reporte_municipios).grid(row=1, column=1, padx=6, pady=6, sticky="ew")
        ttk.Button(self, text="Exportar a CSV", command=self.exportar_csv).grid(row=1, column=2, padx=6, pady=6, sticky="ew")
        ttk.Button(self, text="Actualizar", command=lambda: self.refresh_all()).grid(row=1, column=3, padx=6, pady=6, sticky="ew")

        ttk.Separator(self).grid(row=2, column=0, columnspan=4, sticky="ew", pady=10)
        ttk.Button(self, text="Volver al menú", command=self.go_back).grid(row=3, column=0, columnspan=4, pady=6)

        # Matplotlib embebido
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure
        self.Figure = Figure
        self.FigureCanvasTkAgg = FigureCanvasTkAgg
        self.canvas = None

        # Suscripción (por si está abierta la vista)
        bus.subscribe("domicilio_changed", lambda: self.reporte_tipos())
        bus.subscribe("habitante_changed", lambda: self.reporte_municipios())

        self.refresh_all()

    def _plot(self, labels, values, title):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        fig = self.Figure(figsize=(6.5,3.2), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(labels, values)
        ax.set_title(title)
        ax.tick_params(axis='x', rotation=20)
        self.canvas = self.FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=4, pady=10)

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

    def reporte_tipos(self):
        rows = self._query("""
            SELECT tipo_casa, COUNT(*) as total
            FROM domicilios
            GROUP BY tipo_casa
            ORDER BY total DESC
        """)
        if not rows:
            return
        labels = [r[0] for r in rows]
        values = [r[1] for r in rows]
        self._plot(labels, values, "Viviendas por tipo")

    def reporte_municipios(self):
        rows = self._query("""
            SELECT c.localidad AS municipio, COUNT(h.id) AS total_habitantes
            FROM habitantes h
            JOIN domicilios d ON d.id = h.domicilio_id
            JOIN colonias c ON c.id = d.colonia_id
            GROUP BY c.localidad
            ORDER BY total_habitantes DESC
            LIMIT 12
        """)
        if not rows:
            return
        labels = [r[0] for r in rows]
        values = [r[1] for r in rows]
        self._plot(labels, values, "Habitantes por municipio (Top 12)")

    def exportar_csv(self):
        folder = filedialog.askdirectory(title="Carpeta de exportación")
        if not folder: return
        tipos = self._query("""
            SELECT tipo_casa, COUNT(*) as total
            FROM domicilios
            GROUP BY tipo_casa
            ORDER BY total DESC
        """)
        df1 = pd.DataFrame(tipos, columns=["tipo_casa","total"])
        df1.to_csv(f"{folder}/reporte_tipos_vivienda.csv", index=False, encoding="utf-8")

        mun = self._query("""
            SELECT c.localidad AS municipio, COUNT(h.id) AS total_habitantes
            FROM habitantes h
            JOIN domicilios d ON d.id = h.domicilio_id
            JOIN colonias c ON c.id = d.colonia_id
            GROUP BY c.localidad
        """)
        df2 = pd.DataFrame(mun, columns=["municipio","total_habitantes"])
        df2.to_csv(f"{folder}/reporte_habitantes_municipio.csv", index=False, encoding="utf-8")

    def refresh_all(self):
        self.reporte_tipos()
        self.reporte_municipios()
