import customtkinter as ctk
import config
from registro.colonias import colonia
from registro.domicilios import domicilio
from registro.habitantes import habitante
import database.get_set_data as gd
from datetime import date
from CTkMessagebox import CTkMessagebox

class MainMenuEditHabitante():
    def __init__(self, user):
        self.user = user
        
        ctk.set_appearance_mode("light")

        self.root = ctk.CTk()
        self.root.title("Censo INEGI")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.root.configure(fg_color=config.bg_color)

        frame = ctk.CTkFrame(self.root, corner_radius=12, fg_color=config.frame_color)
        frame.place(relx=0.01, rely=0.01, anchor="nw")

        font_title = config.font_title
        font = config.font

        corner_radius = config.corner_radius
        button_color = config.button_color
        button_text_color = config.button_text_color
        pady = config.pady
        padx = config.padx

        width = 200

        self.values_ciudad=gd.obtener_municipios()
        self.values_colonia=gd.obtener_colonias("")

        row = 0
        ctk.CTkLabel(frame, text="Introduce un domicilio y un habitante", font=font_title).grid(row=row, column=0, sticky = "w", padx =padx, pady=10, columnspan=2)

        row = 1
        ctk.CTkLabel(frame, text="Municipio / Localidad: ", font=font).grid(row=row, column=0, sticky = "e", padx = padx, pady=pady)
        self.combobox_ciudad=ctk.CTkComboBox(frame, values=self.values_ciudad, width=width, corner_radius=corner_radius, command=lambda value: self.actualizar_colonias())
        self.combobox_ciudad.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)
        self.combobox_ciudad.set("")
        self.combobox_ciudad.bind("<KeyRelease>", self.filtrar_ciudad)

        ctk.CTkLabel(frame, text="Colonia: ", font=font).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
        self.combobox_colonia=ctk.CTkComboBox(frame, values=self.values_colonia, width=width, corner_radius=corner_radius)
        self.combobox_colonia.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)
        self.combobox_colonia.set("")
        self.combobox_colonia.bind("<KeyRelease>", self.filtrar_colonias)

        row = 2
        ctk.CTkLabel(frame, text="Domicilio: ", font=font_title).grid(row=row, column=0, sticky = "w", padx = padx, pady=10, columnspan=2)

        row = 3
        ctk.CTkLabel(frame, text="Calle: ", font=font).grid(row=row, column=0, sticky = "e", padx = padx, pady=pady)
        self.entry_calle=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
        self.entry_calle.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

        def solo_numeros(valor):
            return valor.isdigit() or valor == ""

        validacion = self.root.register(solo_numeros)

        ctk.CTkLabel(frame, text="Numero: ", font=font).grid(row=row, column=2, sticky="e", padx=padx, pady=pady)
        self.entry_num = ctk.CTkEntry(frame, width=width, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
        self.entry_num.grid(row=row, column=3, sticky="w", padx=padx, pady=pady)

        row = 4
        ctk.CTkLabel(frame, text="Habitante: ", font=font_title).grid(row=row, column=0, sticky = "w", padx = padx, pady=10, columnspan=2)

        row = 5
        ctk.CTkLabel(frame, text="Nombre: ", font=font).grid(row=row, sticky = "e", column=0, padx = padx, pady=pady)
        self.entry_nombre=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
        self.entry_nombre.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

        row = 6
        ctk.CTkLabel(frame, text="Editar Habitante: ", font=font_title).grid(row=row, column=0, sticky = "w", padx = padx, pady=10, columnspan=2)

        row = 7
        ctk.CTkLabel(frame, text="Nombre: ", font=font).grid(row=row, sticky = "e", column=0, padx = padx, pady=pady)
        self.n_entry_nombre=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
        self.n_entry_nombre.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

        ctk.CTkLabel(frame, text="Sexo(M/F): ", font=font).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
        self.n_combobox_sexo=ctk.CTkComboBox(frame, values=["M", "F"], width=75,corner_radius=corner_radius, state="readonly")
        self.n_combobox_sexo.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)

        row = 8
        ctk.CTkLabel(frame, text="Fecha Nacimiento:     Año: ", font=font).grid(row=row, column=0, sticky = "e", padx = padx, pady=pady)
        self.n_entry_fec_anno=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
        self.n_entry_fec_anno.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

        ctk.CTkLabel(frame, text="Mes: ", font=font).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
        self.n_entry_fec_mes=ctk.CTkEntry(frame, width=50, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
        self.n_entry_fec_mes.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)

        ctk.CTkLabel(frame, text="Día: ", font=font).grid(row=row, column=4, sticky = "e", padx = padx, pady=pady)
        self.n_entry_fec_dia=ctk.CTkEntry(frame, width=50, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
        self.n_entry_fec_dia.grid(row=row, column=5, sticky = "w", padx = padx, pady=pady)

        row = 9
        ctk.CTkLabel(frame, text="Actividad Económica: ", font=font).grid(row=row, sticky = "e", column=0, padx = padx, pady=pady)
        self.n_entry_act_eco=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
        self.n_entry_act_eco.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

        row = 10
        self.n_checkbox_var = ctk.StringVar(value="si")
        n_checkbox = ctk.CTkCheckBox(frame, text="¿Tiene actividad económica?", variable=self.n_checkbox_var, onvalue="si", offvalue="no", command=self.n_on_checkbox_change)

        n_checkbox.grid(row=row, column=0, padx=padx, pady=pady, sticky="w")

        row = 11
        ctk.CTkLabel(frame, text="", font=font_title).grid(row=row, column=0, sticky = "w", padx = padx, pady=10, columnspan=2)

        row = 12
        ctk.CTkButton(frame, text="Editar Habitante", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color, command= lambda: self.editar_habitante()).grid(row=row, column=0, padx = padx, pady=pady)
        ctk.CTkButton(frame,text="Limpiar campos",width=width,font=font,corner_radius=corner_radius,fg_color=button_color,text_color=button_text_color,command=self.limpiar_campos).grid(row=row, column=3, padx=padx, pady=pady)

        row = 13
        ctk.CTkButton(frame, text="Salir", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color, command=self.root.destroy).grid(row=row, column=3, padx = padx, pady=pady)

        self.root.mainloop()
        
    def editar_habitante(self):
        col = colonia()
        dom = domicilio()
        hab = habitante()

        anno_str = self.n_entry_fec_anno.get().strip()
        mes_str = self.n_entry_fec_mes.get().strip()
        dia_str = self.n_entry_fec_dia.get().strip()

        n_nombre = self.n_entry_nombre.get().strip()
        n_sexo = self.n_combobox_sexo.get().strip()
        n_act_eco = self.n_entry_act_eco.get().strip()

        nombre = self.entry_nombre.get().strip()
        numero = self.entry_num.get().strip()
        calle = self.entry_calle.get().strip()
        col_nom = self.combobox_colonia.get().strip()
        localidad = self.combobox_ciudad.get().strip()

        if not all([localidad, col_nom, calle, numero, nombre]):
            CTkMessagebox(title="Error", message="Debe llenar todos los campos para encontrar el habitante.", icon="warning")
            return

        result_col = col.buscar_colonia(col_nom, localidad)
        if not result_col:
            CTkMessagebox(title="Error", message="Colonia no encontrada.", icon="warning")
            return

        col_id = result_col[0]

        result_dom = dom.buscar_domicilio(calle, numero, col_id)
        if not result_dom:
            CTkMessagebox(title="Error", message="Domicilio no encontrado.", icon="warning")
            return

        dom_id = result_dom[0]

        result_hab = hab.buscar_habitante(nombre, dom_id)
        if not result_hab:
            CTkMessagebox(title="Error", message="Habitante no encontrado.", icon="warning")
            return

        n_fecha_nac = None

        if anno_str or mes_str or dia_str:
            try:
                n_fecha_nac = date(int(anno_str), int(mes_str), int(dia_str))
            except ValueError:
                CTkMessagebox(title="Error", message="Introduce una fecha válida.", icon="warning")
                return

        ok = hab.editar_habitante(nombre, dom_id, nuevo_nombre=n_nombre, nuevo_sexo=n_sexo,nuevo_act_eco=n_act_eco, nuevo_fecha_nac=n_fecha_nac)

        if ok:
            CTkMessagebox(title="Éxito", message="Habitante editado correctamente.", icon="info")
        else:
            CTkMessagebox(title="Aviso", message="No se realizaron cambios.", icon="info")

    def n_on_checkbox_change(self):
        if self.n_checkbox_var.get() == "si":
            self.n_entry_act_eco.configure(state="normal")
            self.n_entry_act_eco.delete(0, "end")
        else:
            self.n_entry_act_eco.configure(state="normal")
            self.n_entry_act_eco.delete(0, "end")
            self.n_entry_act_eco.insert(0, "Ninguna")
            self.n_entry_act_eco.configure(state="disabled")

    def limpiar_campos(self):
        self.entry_calle.delete(0, "end")
        self.entry_num.delete(0, "end")
        self.entry_nombre.delete(0, "end")

        self.combobox_ciudad.set("")
        self.combobox_colonia.set("")

        self.n_entry_nombre.delete(0, "end")
        self.n_entry_fec_anno.delete(0, "end")
        self.n_entry_fec_mes.delete(0, "end")
        self.n_entry_fec_dia.delete(0, "end")
        self.n_entry_act_eco.configure(state="normal")
        self.n_entry_act_eco.delete(0, "end")

        self.n_combobox_sexo.set("")

        self.n_checkbox_var.set("si")
        self.n_on_checkbox_change()
        pass

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