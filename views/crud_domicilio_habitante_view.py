import customtkinter as ctk
import config
from registro.colonias import colonia
from registro.domicilios import domicilio
from registro.habitantes import habitante
import database.get_set_data as gd
from datetime import date
from CTkMessagebox import CTkMessagebox

class MainMenuCRUDHabitantes():
    def __init__(self, user):
        self.user = user

        ctk.set_appearance_mode(config.appearance)

        self.root = ctk.CTk()
        self.root.title("Censo INEGI")
        self.root.geometry("1075x550")
        self.root.resizable(False, False)
        self.root.configure(fg_color=config.bg_color)

        frame = ctk.CTkFrame(self.root, corner_radius=12, fg_color=config.frame_color)
        frame.place(anchor="nw")

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
        ctk.CTkLabel(frame, text="Registro de Vivienda y Habitante", font=font_title, text_color=text_color).grid(row=row, column=0, sticky = "w", padx =padx, pady=10, columnspan=2)

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
        ctk.CTkLabel(frame, text="Tipo Vivienda: ", font=font, text_color=text_color).grid(row=row, sticky = "e", column=0, padx = padx, pady=pady)
        self.combobox_t_vivienda=ctk.CTkComboBox(frame, values=values_t_vivienda, width=width, corner_radius=corner_radius, state="readonly")
        self.combobox_t_vivienda.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

        ctk.CTkLabel(frame, text="Calle: ", font=font, text_color=text_color).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
        self.entry_calle=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
        self.entry_calle.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)

        def solo_numeros(valor):
            return valor.isdigit() or valor == ""

        validacion = self.root.register(solo_numeros)

        ctk.CTkLabel(frame, text="Numero: ", font=font, text_color=text_color).grid(row=row, column=4, sticky="e", padx=padx, pady=pady)
        self.entry_num = ctk.CTkEntry(frame, width=width, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
        self.entry_num.grid(row=row, column=5, sticky="w", padx=padx, pady=pady)

        row = 4
        ctk.CTkLabel(frame, text="Habitante: ", font=font_title, text_color=text_color).grid(row=row, column=0, sticky = "w", padx = padx, pady=10, columnspan=2)

        row = 5
        ctk.CTkLabel(frame, text="Nombre: ", font=font, text_color=text_color).grid(row=row, sticky = "e", column=0, padx = padx, pady=pady)
        self.entry_nombre=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
        self.entry_nombre.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

        ctk.CTkLabel(frame, text="Sexo(M/F): ", font=font, text_color=text_color).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
        self.combobox_sexo=ctk.CTkComboBox(frame, values=["M", "F"], width=75,corner_radius=corner_radius, state="readonly")
        self.combobox_sexo.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)

        row = 6
        ctk.CTkLabel(frame, text="Fecha Nacimiento:     Año: ", font=font, text_color=text_color).grid(row=row, column=0, sticky = "e", padx = padx, pady=pady)
        self.entry_fec_anno=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
        self.entry_fec_anno.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

        ctk.CTkLabel(frame, text="Mes: ", font=font, text_color=text_color).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
        self.entry_fec_mes=ctk.CTkEntry(frame, width=50, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
        self.entry_fec_mes.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)

        ctk.CTkLabel(frame, text="Día: ", font=font, text_color=text_color).grid(row=row, column=4, sticky = "e", padx = padx, pady=pady)
        self.entry_fec_dia=ctk.CTkEntry(frame, width=50, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
        self.entry_fec_dia.grid(row=row, column=5, sticky = "w", padx = padx, pady=pady)

        row = 7
        ctk.CTkLabel(frame, text="Actividad Económica: ", font=font, text_color=text_color).grid(row=row, sticky = "e", column=0, padx = padx, pady=pady)
        self.entry_act_eco=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
        self.entry_act_eco.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

        row = 8

        self.checkbox_var = ctk.StringVar(value="si")
        checkbox = ctk.CTkCheckBox(frame,font=font, text_color=text_color, text="¿Tiene actividad económica?", variable=self.checkbox_var, onvalue="si", offvalue="no", command=self.on_checkbox_change)

        checkbox.grid(row=row, column=0, padx=padx, pady=pady, sticky="w")

        row = 9
        ctk.CTkLabel(frame, text="", font=font_title, text_color=text_color).grid(row=row, column=0, sticky = "w", padx = padx, pady=10, columnspan=2)

        row = 10
        ctk.CTkButton(frame, text="Registrar Colonia", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color, command= lambda: self.registrar_col()).grid(row=row, column=0, padx = padx, pady=pady)
        ctk.CTkButton(frame, text="Eliminar Colonia", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color, command= lambda: self.eliminar_col()).grid(row=row, column=1, padx = padx, pady=pady)
        
        row = 11
        ctk.CTkButton(frame, text="Registrar Domicilio", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color, command= lambda: self.registrar_dom()).grid(row=row, column=0, padx = padx, pady=pady)
        ctk.CTkButton(frame, text="Eliminar Domicilio", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color, command= lambda: self.eliminar_dom()).grid(row=row, column=1, padx = padx, pady=pady)
        ctk.CTkButton(frame,text="Limpiar campos",width=width,font=font,corner_radius=corner_radius,fg_color=button_color,text_color=button_text_color,command=self.limpiar_campos).grid(row=row, column=3, padx=padx, pady=pady)

        row = 12
        ctk.CTkButton(frame, text="Registrar Habitante", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color, command= lambda: self.registrar_hab()).grid(row=row, column=0, padx = padx, pady=pady)
        ctk.CTkButton(frame, text="Eliminar Habitante", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color, command= lambda: self.eliminar_hab()).grid(row=row, column=1, padx = padx, pady=pady)
        ctk.CTkButton(frame, text="Salir", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color, command=self.root.destroy).grid(row=row, column=3, padx = padx, pady=pady)

        self.root.mainloop()
        
    def limpiar_campos(self):
        self.entry_calle.delete(0, "end")
        self.entry_num.delete(0, "end")
        self.entry_nombre.delete(0, "end")
        self.entry_fec_anno.delete(0, "end")
        self.entry_fec_mes.delete(0, "end")
        self.entry_fec_dia.delete(0, "end")
        self.entry_act_eco.configure(state="normal")
        self.entry_act_eco.delete(0, "end")

        self.combobox_ciudad.set("")
        self.combobox_colonia.set("")
        self.combobox_t_vivienda.set("")
        self.combobox_sexo.set("")

        self.checkbox_var.set("si")
        self.on_checkbox_change()
        pass

    def on_checkbox_change(self):
        if self.checkbox_var.get() == "si":
            self.entry_act_eco.configure(state="normal")
            self.entry_act_eco.delete(0, "end")
        else:
            self.entry_act_eco.configure(state="normal")
            self.entry_act_eco.delete(0, "end")
            self.entry_act_eco.insert(0, "Ninguna")
            self.entry_act_eco.configure(state="disabled")

    def registrar_col(self):
        col = colonia()

        municipio = self.combobox_ciudad.get().strip()
        col_nom = self.combobox_colonia.get().strip()

        if not municipio or not col_nom:
            CTkMessagebox(title="Error", message="Debe llenar todos los campos.", icon="warning")
            return

        if municipio not in gd.obtener_municipios():
            CTkMessagebox(title="Error", message="Municipio / Localidad no encontrada.", icon="warning")
            return
        
        result_col = col.buscar_colonia(col_nom, municipio)

        if result_col:
            CTkMessagebox(title="Error", message="Colonia ya registrada.", icon="warning")
            return
        
        col.registrar_colonia(col_nom, municipio)
        self.actualizar_colonias()
        self.combobox_colonia.set(col_nom)
        CTkMessagebox(title="", message="Colonia Registrada.", icon="info")

    def eliminar_col(self):
        col = colonia()

        municipio = self.combobox_ciudad.get().strip()
        col_nom = self.combobox_colonia.get().strip()

        if not municipio or not col_nom:
            CTkMessagebox(title="Error", message="Debe llenar todos los campos.", icon="warning")
            return

        if municipio not in gd.obtener_municipios():
            CTkMessagebox(title="Error", message="Municipio / Localidad no encontrada.", icon="warning")
            return
        
        result_col = col.buscar_colonia(col_nom, municipio)

        if not result_col:
            CTkMessagebox(title="Error", message="Colonia no encontrada.", icon="warning")
            return
        
        col.eliminar_colonia(col_nom, municipio)
        self.actualizar_colonias()
        CTkMessagebox(title="", message="Colonia eliminada correctamente!", icon="info")

    def registrar_dom(self):
        col = colonia()
        dom = domicilio()

        numero = int(self.entry_num.get().strip())
        calle = self.entry_calle.get().strip()
        col_nom = self.combobox_colonia.get().strip()
        localidad = self.combobox_ciudad.get().strip()
        tipo_casa = self.combobox_t_vivienda.get().strip()

        if not all([numero, calle, col_nom, localidad, tipo_casa]) :
            CTkMessagebox(title="Error", message="Debe llenar todos los campos de localidad.", icon="warning")
            return

        result = col.buscar_colonia(col_nom, localidad)

        if result:
            col_id = result[0]
            dom_id = dom.buscar_domicilio(calle, numero, col_id)

            if dom_id:
                CTkMessagebox(title="Error", message="Domicilio ya registrado.", icon="warning")
            else:
                dom.registrar_domicilio(tipo_casa, calle, numero, col_id)
                CTkMessagebox(title="Error", message="Domicilio registrado correctamente!", icon="info")
        else:
            CTkMessagebox(title="Error", message="Colonia no reconocida.", icon="warning")

    def registrar_hab(self):
        col = colonia()
        dom = domicilio()
        hab = habitante()

        anno_str = self.entry_fec_anno.get().strip()
        mes_str = self.entry_fec_mes.get().strip()
        dia_str = self.entry_fec_dia.get().strip()

        nombre = self.entry_nombre.get().strip()
        sexo = self.combobox_sexo.get()
        act_eco = self.entry_act_eco.get().strip()

        numero = self.entry_num.get().strip()
        calle = self.entry_calle.get().strip()
        col_nom = self.combobox_colonia.get().strip()
        localidad = self.combobox_ciudad.get().strip()

        if not all([anno_str, mes_str, dia_str, nombre, sexo, act_eco,
                    numero, calle, col_nom, localidad]):
            CTkMessagebox(title="Error", message="Debe llenar todos los campos.", icon="warning")
            return

        anno_nac = int(anno_str)
        mes_nac = int(mes_str)
        dia_nac = int(dia_str)
        numero = int(numero)

        try:
            fecha_nac = date(anno_nac, mes_nac, dia_nac)
        except ValueError:
            CTkMessagebox(title="Error", message="Introduce una fecha válida.", icon="warning")
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

        if result_hab:
            CTkMessagebox(title="Error", message="Habitante ya registrado.", icon="warning")
            return

        hab.registrar_habitante(nombre, fecha_nac, sexo, dom_id, act_eco)
        CTkMessagebox(title="", message="Habitante registrado correctamente!", icon="info")

    def eliminar_dom(self):
        col = colonia()
        dom = domicilio()

        numero_str = self.entry_num.get().strip()
        calle = self.entry_calle.get().strip()
        col_nom = self.combobox_colonia.get().strip()
        localidad = self.combobox_ciudad.get().strip()

        if not all([numero_str, calle, col_nom, localidad]):
            CTkMessagebox(title="Error", message="Debe llenar todos los campos.", icon="warning")
            return

        numero = int(numero_str)

        result_col = col.buscar_colonia(col_nom, localidad)
        if not result_col:
            CTkMessagebox(title="Error", message="Colonia no encontrada.", icon="warning")
            return

        col_id = result_col[0]

        result_dom = dom.buscar_domicilio(calle, numero, col_id)

        if not result_dom:
            CTkMessagebox(title="Error", message="Domicilio no encontrado.", icon="warning")
            return

        dom.eliminar_domicilio(calle, numero, col_id)
        CTkMessagebox(title="", message="Domicilio eliminado correctamente!", icon="info")

    def eliminar_hab(self):
        col = colonia()
        dom = domicilio()
        hab = habitante()

        nombre = self.entry_nombre.get().strip()

        numero_str = self.entry_num.get().strip()
        calle = self.entry_calle.get().strip()
        col_nom = self.combobox_colonia.get().strip()
        localidad = self.combobox_ciudad.get().strip()

        if not all([nombre, numero_str, calle, col_nom, localidad]):
            CTkMessagebox(title="Error", message="Debe llenar todos los campos.", icon="warning")
            return

        numero = int(numero_str)

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

        hab.eliminar_habitante(nombre, dom_id)
        CTkMessagebox(title="", message="Habitante eliminado correctamente!", icon="info")
        
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
        