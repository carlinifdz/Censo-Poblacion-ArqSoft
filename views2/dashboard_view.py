import customtkinter as ctk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from database.conn import get_connection
import config


class DashboardView:
    def __init__(self, user):
        self.user = user
        ctk.set_appearance_mode("light")

        self.root = ctk.CTk()
        self.root.title("Dashboard - Censo INEGI Coahuila")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)
        self.root.configure(fg_color=config.bg_color)

        # guardar referencias a los canvas para poder actualizarlos
        self.canvas_municipios = None
        self.canvas_tipos = None

        self._build_ui()
        self._load_data()

        self.root.mainloop()

    # ------------------------ DB helper ------------------------

    def _query(self, sql, params=None):
        conn = get_connection()
        if conn is None:
            print("Error en la conexión a la base de datos")
            return []

        try:
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print("Error en consulta:", e)
            return []
        finally:
            try:
                cursor.close()
                conn.close()
            except:
                pass

    # ------------------------ UI ------------------------

    def _build_ui(self):
        font_title = config.font_title
        font = config.font
        corner_radius = config.corner_radius
        button_color = config.button_color
        button_text_color = config.button_text_color
        pady = config.pady
        padx = config.padx

        # Frame principal
        main_frame = ctk.CTkFrame(self.root, fg_color=config.frame_color, corner_radius=corner_radius)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        ctk.CTkLabel(
            main_frame,
            text=f"Dashboard – Censo de Población INEGI (Usuario: {self.user})",
            font=font_title,
        ).grid(row=0, column=0, columnspan=3, pady=(0, 15), sticky="w")

        # ---------- KPIs ----------
        kpi_frame = ctk.CTkFrame(main_frame, fg_color=config.bg_color, corner_radius=corner_radius)
        kpi_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=padx, pady=pady)
        kpi_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.lbl_total_habitantes = ctk.CTkLabel(kpi_frame, text="Habitantes: --", font=font)
        self.lbl_total_viviendas = ctk.CTkLabel(kpi_frame, text="Viviendas: --", font=font)
        self.lbl_municipios = ctk.CTkLabel(kpi_frame, text="Municipios (localidad): --", font=font)
        self.lbl_colonias = ctk.CTkLabel(kpi_frame, text="Colonias: --", font=font)

        self.lbl_total_habitantes.grid(row=0, column=0, padx=padx, pady=pady, sticky="w")
        self.lbl_total_viviendas.grid(row=0, column=1, padx=padx, pady=pady, sticky="w")
        self.lbl_municipios.grid(row=0, column=2, padx=padx, pady=pady, sticky="w")
        self.lbl_colonias.grid(row=0, column=3, padx=padx, pady=pady, sticky="w")

        # ---------- Gráficas ----------
        charts_frame = ctk.CTkFrame(main_frame, fg_color=config.bg_color, corner_radius=corner_radius)
        charts_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=padx, pady=pady)
        charts_frame.grid_columnconfigure((0, 1), weight=1)
        charts_frame.grid_rowconfigure(0, weight=1)

        # Frame para grafica de municipios
        self.frame_municipios = ctk.CTkFrame(charts_frame, fg_color=config.frame_color, corner_radius=corner_radius)
        self.frame_municipios.grid(row=0, column=0, padx=padx, pady=pady, sticky="nsew")

        ctk.CTkLabel(self.frame_municipios, text="Habitantes por municipio (Top 10)", font=font).pack(
            anchor="w", padx=10, pady=5
        )

        # Frame para grafica de tipos de vivienda
        self.frame_tipos = ctk.CTkFrame(charts_frame, fg_color=config.frame_color, corner_radius=corner_radius)
        self.frame_tipos.grid(row=0, column=1, padx=padx, pady=pady, sticky="nsew")

        ctk.CTkLabel(self.frame_tipos, text="Viviendas por tipo", font=font).pack(
            anchor="w", padx=10, pady=5
        )

        # ---------- Tabla por municipio/localidad ----------
        table_frame = ctk.CTkFrame(main_frame, fg_color=config.bg_color, corner_radius=corner_radius)
        table_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=padx, pady=(pady, 0))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            table_frame,
            text="Quiénes y cuántos viven por vivienda",
            font=font,
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(5, 0))

        inner = ctk.CTkFrame(table_frame, fg_color="white", corner_radius=8)
        inner.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        scrollbar = ttk.Scrollbar(inner)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tabla = ttk.Treeview(
            inner,
            columns=("vivienda", "colonia", "direccion", "total", "habitantes", "actividades"),
            show="headings",
            yscrollcommand=scrollbar.set,
        )
        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=self.tabla.yview)

        inner.grid_rowconfigure(0, weight=1)
        inner.grid_columnconfigure(0, weight=1)

        self.tabla.heading("vivienda", text="ID Vivienda")
        self.tabla.heading("colonia", text="Colonia")
        self.tabla.heading("direccion", text="Dirección")
        self.tabla.heading("total", text="Total hab.")
        self.tabla.heading("habitantes", text="Quiénes viven")
        self.tabla.heading("actividades", text="Actividades económicas")

        self.tabla.column("vivienda", width=80, anchor="center")
        self.tabla.column("colonia", width=120, anchor="w")
        self.tabla.column("direccion", width=180, anchor="w")
        self.tabla.column("total", width=80, anchor="center")
        self.tabla.column("habitantes", width=220, anchor="w")
        self.tabla.column("actividades", width=220, anchor="w")


        # Botón actualizar
        btn_frame = ctk.CTkFrame(main_frame, fg_color=config.frame_color, corner_radius=corner_radius)
        btn_frame.grid(row=4, column=0, columnspan=3, sticky="ew", padx=padx, pady=(10, 0))
        btn_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            btn_frame,
            text="Regresar",
            font=font,
            corner_radius=corner_radius,
            fg_color="#888888",
            text_color=button_text_color,
            command=self.cerrar_dashboard,
        ).grid(row=0, column=0, pady=10, padx=10, sticky="w")

        ctk.CTkButton(
            btn_frame,
            text="Actualizar dashboard",
            font=font,
            corner_radius=corner_radius,
            fg_color=button_color,
            text_color=button_text_color,
            command=self._load_data,
        ).grid(row=0, column=1, pady=10, padx=10, sticky="e")


    # ------------------------ Lógica de datos ------------------------

    def _load_data(self):
        # KPIs
        total_h = self._query("SELECT COUNT(*) FROM habitantes")
        total_v = self._query("SELECT COUNT(*) FROM domicilios")
        total_m = self._query("SELECT COUNT(DISTINCT localidad) FROM colonias")
        total_c = self._query("SELECT COUNT(*) FROM colonias")

        th = total_h[0][0] if total_h else 0
        tv = total_v[0][0] if total_v else 0
        tm = total_m[0][0] if total_m else 0
        tc = total_c[0][0] if total_c else 0

        self.lbl_total_habitantes.configure(text=f"Habitantes: {th}")
        self.lbl_total_viviendas.configure(text=f"Viviendas: {tv}")
        self.lbl_municipios.configure(text=f"Municipios (localidad): {tm}")
        self.lbl_colonias.configure(text=f"Colonias: {tc}")

        # Gráfica habitantes por municipio
        sql_mun = """
            SELECT c.localidad AS municipio, COUNT(h.id) AS total_habitantes
            FROM habitantes h
            JOIN domicilios d ON d.id = h.domicilio_id
            JOIN colonias c ON c.id = d.colonia_id
            GROUP BY c.localidad
            ORDER BY total_habitantes DESC
            LIMIT 10
        """
        rows_mun = self._query(sql_mun)
        labels_mun = [r[0] for r in rows_mun]
        values_mun = [r[1] for r in rows_mun]

        self._plot_bar(
            parent=self.frame_municipios,
            labels=labels_mun,
            values=values_mun,
            title="Habitantes por municipio (Top 10)",
            canvas_attr="canvas_municipios",
        )

        # Gráfica viviendas por tipo
        sql_tip = """
            SELECT d.tipo_casa, COUNT(*) AS total
            FROM domicilios d
            GROUP BY d.tipo_casa
            ORDER BY total DESC
        """
        rows_tip = self._query(sql_tip)
        labels_tip = [r[0] for r in rows_tip]
        values_tip = [r[1] for r in rows_tip]

        self._plot_bar(
            parent=self.frame_tipos,
            labels=labels_tip,
            values=values_tip,
            title="Viviendas por tipo de casa",
            canvas_attr="canvas_tipos",
        )

                # -------- Tabla: quiénes y cuántos viven por vivienda --------
        # -------- Tabla: quiénes y cuántos viven + actividades eco por vivienda --------
        sql_tabla = """
            SELECT 
                d.id AS id_vivienda,
                c.nombre AS colonia,
                CONCAT(IFNULL(d.calle, ''), ' ', IFNULL(d.numero, '')) AS direccion,
                COUNT(h.id) AS total_habitantes,
                GROUP_CONCAT(
                    IFNULL(h.nombre, '')
                    SEPARATOR ', '
                ) AS habitantes,
                GROUP_CONCAT(
                    DISTINCT IFNULL(h.act_eco, '')
                    SEPARATOR ', '
                ) AS actividades
            FROM domicilios d
            LEFT JOIN colonias c ON c.id = d.colonia_id
            LEFT JOIN habitantes h ON h.domicilio_id = d.id
            GROUP BY 
                d.id,
                c.nombre,
                d.calle,
                d.numero
            ORDER BY total_habitantes DESC, c.nombre;
        """
        rows_tabla = self._query(sql_tabla)
        self._fill_table(rows_tabla)




    # ------------------------ Helpers de UI ------------------------

    def _plot_bar(self, parent, labels, values, title, canvas_attr):
        # destruir canvas previo
        old_canvas = getattr(self, canvas_attr, None)
        if old_canvas is not None:
            old_canvas.get_tk_widget().destroy()

        if not labels:
            return

        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(labels, values)
        ax.set_title(title)
        ax.tick_params(axis="x", rotation=45, labelsize=8)
        ax.tick_params(axis="y", labelsize=8)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        setattr(self, canvas_attr, canvas)

    def _fill_table(self, rows):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for id_viv, colonia, direccion, total, habitantes, actividades in rows:
            self.tabla.insert(
                "",
                "end",
                values=(
                    id_viv,
                    colonia,
                    direccion,
                    total,
                    habitantes if habitantes else "-",
                    actividades if actividades else "-"
                )
            )


    def cerrar_dashboard(self):
        # Cierra la ventana del dashboard
        self.root.destroy()

