import customtkinter as ctk
import config
from registro.colonias import colonia
from registro.domicilios import domicilio
from registro.habitantes import habitante
import database.get_set_data as gd
from CTkMessagebox import CTkMessagebox


class MainMenuEditDomicilio():
        
    def __init__(self, user):
        self.user = user

        ctk.set_appearance_mode(config.appearance)

        self.root = ctk.CTk()
        self.root.title("Censo INEGI")
        self.root.geometry("1200x375")
        self.root.resizable(False, False)
        self.root.configure(fg_color=config.bg_color)

        frame = ctk.CTkFrame(self.root, corner_radius=12, fg_color=config.frame_color)
        frame.place(relx=0.01, rely=0.01, anchor="nw")

        font_title = config.font_title
        font = config.font
        text_color = config.text_color

        corner_radius = config.corner_radius
        button_color = config.button_color
        button_text_color = config.button_text_color
        pady = config.pady
        padx = config.padx

        width = 200

        self.values_ciudad=gd.obtener_municipios()
        self.values_colonia=gd.obtener_colonias("")
        values_t_vivienda=["Vivienda de concreto","Vivienda de adobe(antiguo)","Vivienda de ladrillo","Vivienda de madera","Vivienda de cartón",
                "Casa de piedra","Vivienda prefabricada","Material Ecológico","Casa de paja, ramas o caña","Material Adobe Moderno"]

        row = 0
        ctk.CTkLabel(frame, text="Introduce un domicilio", font=font_title, text_color=text_color).grid(row=row, column=0, sticky = "w", padx =padx, pady=10, columnspan=2)

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

        row = 2
        ctk.CTkLabel(frame, text="Domicilio: ", font=font_title, text_color=text_color).grid(row=row, column=0, sticky = "w", padx = padx, pady=10, columnspan=2)

        row = 3
        ctk.CTkLabel(frame, text="Calle: ", font=font, text_color=text_color).grid(row=row, column=0, sticky = "e", padx = padx, pady=pady)
        self.entry_calle=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
        self.entry_calle.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

        def solo_numeros(valor):
            return valor.isdigit() or valor == ""

        validacion = self.root.register(solo_numeros)

        ctk.CTkLabel(frame, text="Numero: ", font=font, text_color=text_color).grid(row=row, column=2, sticky="e", padx=padx, pady=pady)
        self.entry_num = ctk.CTkEntry(frame, width=width, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
        self.entry_num.grid(row=row, column=3, sticky="w", padx=padx, pady=pady)

        row = 4
        ctk.CTkLabel(frame, text="Editar Vivienda", font=font_title, text_color=text_color).grid(row=row, column=0, sticky = "w", padx =padx, pady=10, columnspan=2)

        row = 6
        ctk.CTkLabel(frame, text="Tipo Vivienda: ", font=font, text_color=text_color).grid(row=row, sticky = "e", column=0, padx = padx, pady=pady)
        self.n_combobox_t_vivienda=ctk.CTkComboBox(frame, values=values_t_vivienda, width=width, corner_radius=corner_radius, state="readonly")
        self.n_combobox_t_vivienda.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

        ctk.CTkLabel(frame, text="Calle: ", font=font, text_color=text_color).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
        self.n_entry_calle=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
        self.n_entry_calle.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)

        ctk.CTkLabel(frame, text="Numero: ", font=font, text_color=text_color).grid(row=row, column=4, sticky="e", padx=padx, pady=pady)
        self.n_entry_num = ctk.CTkEntry(frame, width=width, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
        self.n_entry_num.grid(row=row, column=5, sticky="w", padx=padx, pady=pady)

        row = 7
        ctk.CTkLabel(frame, text="", font=font_title, text_color=text_color).grid(row=row, column=0, sticky = "w", padx = padx, pady=10, columnspan=2)

        row = 8
        ctk.CTkButton(frame, text="Editar Domicilio", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color, command= lambda: self.editar_domicilio()).grid(row=row, column=0, padx = padx, pady=pady)
        ctk.CTkButton(frame,text="Limpiar campos",width=width,font=font,corner_radius=corner_radius,fg_color=button_color,text_color=button_text_color,command=self.limpiar_campos).grid(row=row, column=2, padx=padx, pady=pady)
        ctk.CTkButton(frame, text="Salir", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color, command=self.root.destroy).grid(row=row, column=3, padx = padx, pady=pady)

        self.root.mainloop()

    def editar_domicilio(self):
        col = colonia()
        dom = domicilio()
        
        numero = self.entry_num.get().strip()
        calle = self.entry_calle.get().strip()
        col_nom = self.combobox_colonia.get().strip()
        localidad = self.combobox_ciudad.get().strip()

        n_numero = self.n_entry_num.get().strip()
        n_calle = self.n_entry_calle.get().strip()
        n_t_vivienda = self.n_combobox_t_vivienda.get()

        if not all([localidad, col_nom, calle, numero]):
            CTkMessagebox(title="Error",message="Debe llenar todos los campos para encontrar el domicilio.",icon="warning")
            return

        result_col = col.buscar_colonia(col_nom, localidad)
        if not result_col:
            CTkMessagebox(title="Error", message="Colonia no encontrada.", icon="warning")
            return

        col_id = result_col[0]

        try:
            numero_int = int(numero)
        except ValueError:
            CTkMessagebox(title="Error", message="El número original no es válido.", icon="warning")
            return

        if n_numero:
            try:
                n_numero_int = int(n_numero)
            except ValueError:
                CTkMessagebox(title="Error", message="El nuevo número no es válido.", icon="warning")
                return
        else:
            n_numero_int = None

        ok = dom.editar_domicilio(calle, numero_int,col_id, nuevo_calle=n_calle if n_calle else None, nuevo_numero=n_numero_int, nuevo_tipo_casa=n_t_vivienda)

        if ok:
            CTkMessagebox(title="Éxito", message="Domicilio editado correctamente.", icon="info")
        else:
            CTkMessagebox(title="Aviso", message="No se realizaron cambios.", icon="info")


    def limpiar_campos(self):
        self.entry_calle.delete(0, "end")
        self.entry_num.delete(0, "end")

        self.combobox_ciudad.set("")
        self.combobox_colonia.set("")

        self.n_entry_calle.delete(0, "end")
        self.n_entry_num.delete(0, "end")

        self.n_combobox_t_vivienda.set("")

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