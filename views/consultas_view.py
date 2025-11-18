import customtkinter as ctk
from tkinter import ttk
import config
from database.conn import get_connection
import database.get_set_data as gd


class ConsultasView:
    def __init__(self, user):
        self.user = user

        # listas completas para usar en el filtrado
        self.ciudades_all = []
        self.colonias_all = []

        ctk.set_appearance_mode(config.appearance)

        self.root = ctk.CTk()
        self.root.title("Consultas - Censo INEGI")

        # ventana más pequeña
        self.root.geometry("1250x580")
        self.root.resizable(True, False)
        self.root.configure(fg_color=config.bg_color)

        # refs de widgets que usamos en otros métodos
        self.combobox_ciudad = None
        self.combobox_colonia = None
        self.combobox_t_vivienda = None
        self.entry_calle = None
        self.entry_num = None
        self.entry_act_eco = None
        self.tabla = None

        self.values_ciudad=gd.obtener_municipios()
        self.values_colonia=gd.obtener_colonias("")

        self._build_ui()
        self.root.mainloop()

    # ---------------- BD helper ----------------

    def _query(self, sql, params=None):
        conn = get_connection()
        if conn is None:
            print("Error en la conexión a la base de datos")
            return []

        try:
            cur = conn.cursor()
            cur.execute(sql, params or ())
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print("Error en consulta:", e)
            print("SQL:", sql)
            return []
        finally:
            try:
                cur.close()
                conn.close()
            except:
                pass

    # ---------------- UI ----------------

    def _build_ui(self):
        font_title = config.font_title
        font = config.font
        corner_radius = config.corner_radius
        button_color = config.button_color
        button_text_color = config.button_text_color
        pady = 5
        padx = config.padx
        width = 160
        text_color = config.text_color

        # IMPORTANTE: usamos pack, no place
        frame = ctk.CTkFrame(self.root, corner_radius=12, fg_color=config.frame_color)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # título
        row = 0
        ctk.CTkLabel(
            frame,
            text=f"Consultas de Colonia, Vivienda y Habitante - Usuario: {self.user}",
            font=font_title,
            text_color=text_color
        ).grid(row=row, column=0, sticky="w", padx=padx, pady=10, columnspan=6)

        # ---------------- ciudad / colonia ----------------
        row = 1
        ctk.CTkLabel(frame, text="Municipio / Localidad: ", font=font, text_color=text_color).grid(row=row, column=0, sticky = "e", padx = padx, pady=pady)
        self.combobox_ciudad=ctk.CTkComboBox(frame, values=self.values_ciudad, width=width, corner_radius=corner_radius, command=lambda value: self.actualizar_colonias())
        self.combobox_ciudad.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)
        self.combobox_ciudad.set("")
        self.combobox_ciudad.bind("<KeyRelease>", self.filtrar_ciudad)

        ctk.CTkLabel(frame, text="Colonia: ", font=font, text_color=text_color).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
        self.combobox_colonia=ctk.CTkComboBox(frame, values=self.values_colonia, width=width, corner_radius=corner_radius)
        self.combobox_colonia.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)
        self.combobox_colonia.set("")
        self.combobox_colonia.bind("<KeyRelease>", self.filtrar_colonias)   

        # ---------------- domicilio ----------------
        row = 2
        ctk.CTkLabel(frame, text="Domicilio: ", font=font_title, text_color=text_color).grid(
            row=row, column=0, sticky="w", padx=padx, pady=10, columnspan=2
        )

        row = 3
        ctk.CTkLabel(frame, text="Tipo Vivienda: ", font=font, text_color=text_color).grid(
            row=row, sticky="e", column=0, padx=padx, pady=pady
        )
        values_t_vivienda = [
            "Vivienda de concreto", "Vivienda de adobe(antiguo)", "Vivienda de ladrillo",
            "Vivienda de madera", "Vivienda de cartón", "Casa de piedra",
            "Vivienda prefabricada", "Material Ecológico", "Casa de paja, ramas o caña",
            "Material Adobe Moderno"
        ]
        self.combobox_t_vivienda = ctk.CTkComboBox(
            frame, values=values_t_vivienda, width=width,
            corner_radius=corner_radius, state="readonly"
        )
        self.combobox_t_vivienda.grid(row=row, column=1, sticky="w", padx=padx, pady=pady)

        ctk.CTkLabel(frame, text="Calle: ", font=font, text_color=text_color).grid(
            row=row, column=2, sticky="e", padx=padx, pady=pady
        )
        self.entry_calle = ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
        self.entry_calle.grid(row=row, column=3, sticky="w", padx=padx, pady=pady)

        def solo_numeros(valor):
            return valor.isdigit() or valor == ""

        validacion = self.root.register(solo_numeros)

        ctk.CTkLabel(frame, text="Número: ", font=font, text_color=text_color).grid(
            row=row, column=4, sticky="e", padx=padx, pady=pady
        )
        self.entry_num = ctk.CTkEntry(
            frame, width=width, corner_radius=corner_radius,
            validate="key", validatecommand=(validacion, "%P")
        )
        self.entry_num.grid(row=row, column=5, sticky="w", padx=padx, pady=pady)

        # ---------------- filtros extra (habitante / actividad) ----------------
        row = 4
        ctk.CTkLabel(frame, text="Actividad Económica: ", font=font, text_color=text_color).grid(
            row=row, sticky="e", column=0, padx=padx, pady=pady
        )
        self.entry_act_eco = ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
        self.entry_act_eco.grid(row=row, column=1, sticky="w", padx=padx, pady=pady)

        # ---------------- botones de consulta ----------------
        row = 6
        ctk.CTkLabel(frame, text="Consultas rápidas:", font=font_title, text_color=text_color).grid(
            row=row, column=0, sticky="w", padx=padx, pady=10, columnspan=4
        )

        row = 7
        ctk.CTkButton(frame, text="Casas por colonia", width=width, font=font, corner_radius=corner_radius, fg_color=config.button_color, text_color=config.button_text_color, command=self.buscar_casas_por_colonia).grid(row=row, column=0, padx=padx, pady=pady)

        ctk.CTkButton(frame, text="Habitantes por casa", width=width, font=font, corner_radius=corner_radius, fg_color=config.button_color, text_color=config.button_text_color, command=self.buscar_habitantes_por_casa).grid(row=row, column=1, padx=padx, pady=pady)

        ctk.CTkButton(frame, text="Por actividad económica", width=width, font=font, corner_radius=corner_radius, fg_color=config.button_color, text_color=config.button_text_color, command=self.buscar_por_actividad).grid(row=row, column=2, padx=padx, pady=pady)

        ctk.CTkButton(frame, text="Actividades de una casa", width=width, font=font, corner_radius=corner_radius, fg_color=config.button_color, text_color=config.button_text_color, command=self.ver_actividades_casa).grid(row=row, column=3, padx=padx, pady=pady)

        ctk.CTkButton(frame, text="Limpiar campos", width=width, font=font, corner_radius=corner_radius, fg_color=config.button_color, text_color=config.button_text_color, command=self.limpiar_campos).grid(row=row, column=4, padx=padx, pady=pady)
    
        # 🔹 Ahora el botón Regresar va en otra fila
        row = 8
        ctk.CTkButton(
            frame,
            text="Regresar",
            width=width,
            font=font,
            corner_radius=corner_radius,
            fg_color=config.button_color,
            text_color=config.button_text_color,
            command=self.cerrar
        ).grid(row=row, column=0, padx=padx, pady=pady, sticky="w")

        # ---------------- tabla de resultados ----------------
        row = 9
        tabla_frame = ctk.CTkFrame(frame, fg_color="white", corner_radius=8)
        tabla_frame.grid(row=row, column=0, columnspan=6, padx=padx, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(tabla_frame)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tabla = ttk.Treeview(tabla_frame, columns=("col1", "col2", "col3", "col4"), show="headings", yscrollcommand=scrollbar.set, height=8)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        tabla_frame.grid_rowconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(0, weight=1)
        scrollbar.config(command=self.tabla.yview)

        self._config_tabla(("Columna 1", "Columna 2", "Columna 3", "Columna 4"))

    # ---------------- helpers UI ----------------

    def _config_tabla(self, headers):
        for i in range(4):
            name = f"col{i+1}"
            text = headers[i] if i < len(headers) else ""
            self.tabla.heading(name, text=text)
            self.tabla.column(name, width=180, anchor="w")

    def _llenar_tabla(self, rows):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for r in rows:
            r = list(r)
            if len(r) < 4:
                r += [""] * (4 - len(r))
            self.tabla.insert("", "end", values=r)

    def limpiar_campos(self):
        if self.entry_calle:
            self.entry_calle.delete(0, "end")
        if self.entry_num:
            self.entry_num.delete(0, "end")
        if self.entry_act_eco:
            self.entry_act_eco.delete(0, "end")
        if self.combobox_ciudad:
            self.combobox_ciudad.set("")
        if self.combobox_colonia:
            self.combobox_colonia.set("")
        if self.combobox_t_vivienda:
            self.combobox_t_vivienda.set("")
        self._llenar_tabla([])

    # ---------------- carga catálogos + filtrado ----------------

    # ---------------- obtención ID domicilio ----------------

    def _obtener_id_domicilio(self):
        ciudad = self.combobox_ciudad.get().strip()
        colonia = self.combobox_colonia.get().strip()
        calle = self.entry_calle.get().strip() if self.entry_calle else ""
        numero = self.entry_num.get().strip() if self.entry_num else ""

        if not (ciudad and colonia and calle and numero):
            return None

        sql = """
            SELECT d.id
            FROM domicilios d
            JOIN colonias c ON c.id = d.colonia_id
            WHERE c.localidad = %s
              AND c.nombre = %s
              AND d.calle = %s
              AND d.numero = %s
            LIMIT 1;
        """
        rows = self._query(sql, (ciudad, colonia, calle, numero))
        return rows[0][0] if rows else None

    # ---------------- consultas ----------------

    def buscar_casas_por_colonia(self):
        colonia = self.combobox_colonia.get().strip()
        if not colonia:
            self._llenar_tabla([])
            return

        sql = """
            SELECT 
                d.id,
                c.nombre AS colonia,
                CONCAT(IFNULL(d.calle, ''), ' ', IFNULL(d.numero, '')) AS direccion,
                d.tipo_casa
            FROM domicilios d
            JOIN colonias c ON c.id = d.colonia_id
            WHERE c.nombre = %s
            ORDER BY d.id;
        """
        rows = self._query(sql, (colonia,))
        self._config_tabla(("ID Vivienda", "Colonia", "Dirección", "Tipo vivienda"))
        self._llenar_tabla(rows)

    def buscar_habitantes_por_casa(self):
        id_dom = self._obtener_id_domicilio()
        if id_dom is None:
            self._llenar_tabla([])
            return

        sql = """
            SELECT id, nombre, sexo, act_eco
            FROM habitantes
            WHERE domicilio_id = %s
            ORDER BY id;
        """
        rows = self._query(sql, (id_dom,))
        self._config_tabla(("ID Hab.", "Nombre", "Sexo", "Actividad eco."))
        self._llenar_tabla(rows)

    def buscar_por_actividad(self):
        act = self.entry_act_eco.get().strip()
        if not act:
            self._llenar_tabla([])
            return

        sql = """
            SELECT 
                d.id AS id_vivienda,
                c.nombre AS colonia,
                CONCAT(IFNULL(d.calle, ''), ' ', IFNULL(d.numero, '')) AS direccion,
                GROUP_CONCAT(IFNULL(h.nombre, '') SEPARATOR ', ') AS habitantes
            FROM habitantes h
            JOIN domicilios d ON d.id = h.domicilio_id
            JOIN colonias c ON c.id = d.colonia_id
            WHERE h.act_eco LIKE %s
            GROUP BY d.id, c.nombre, d.calle, d.numero
            ORDER BY d.id;
        """
        rows = self._query(sql, ("%" + act + "%",))
        self._config_tabla(("ID Vivienda", "Colonia", "Dirección", "Habitantes"))
        self._llenar_tabla(rows)

    def ver_actividades_casa(self):
        id_dom = self._obtener_id_domicilio()
        if id_dom is None:
            self._llenar_tabla([])
            return

        sql = """
            SELECT nombre, act_eco
            FROM habitantes
            WHERE domicilio_id = %s
            ORDER BY nombre;
        """
        rows = self._query(sql, (id_dom,))
        rows4 = [(nombre, act, "", "") for nombre, act in rows]
        self._config_tabla(("Habitante", "Actividad eco.", "", ""))
        self._llenar_tabla(rows4)

    def cerrar(self):
        self.root.destroy()
    
    def actualizar_colonias(self):
        ciudad = self.combobox_ciudad.get()
        self.values_colonia = gd.obtener_colonias(ciudad)
        self.combobox_colonia.configure(values=self.values_colonia)
        self.combobox_colonia.set("")

    def filtrar_ciudad(self, event):
        texto = self.combobox_ciudad.get().lower()
        filtradas = [c for c in self.values_ciudad if texto in c.lower()]
        self.combobox_ciudad.configure(values=filtradas)

    def filtrar_colonias(self, event):
        texto = self.combobox_colonia.get().lower()
        filtradas = [c for c in self.values_colonia if texto in c.lower()]
        self.combobox_colonia.configure(values=filtradas)