import customtkinter as ctk
import config
from registro.colonias import colonia
import database.get_set_data as gd
from CTkMessagebox import CTkMessagebox

class MainMenuEditColonia():        
    def __init__(self, user):
        self.user = user

        ctk.set_appearance_mode("light")

        self.root = ctk.CTk()
        self.root.title("Censo INEGI")
        self.root.geometry("900x250")
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
        ctk.CTkLabel(frame, text="Introduce una colonia", font=font_title).grid(row=row, column=0, sticky = "w", padx =padx, pady=10, columnspan=2)

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
        ctk.CTkLabel(frame, text="Editar colonia: ", font=font_title).grid(row=row, column=0, sticky = "w", padx = padx, pady=pady, columnspan=2)
        
        row = 3
        ctk.CTkLabel(frame, text="Colonia: ", font=font).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
        self.entry_colonia=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
        self.entry_colonia.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)

        row = 4
        ctk.CTkLabel(frame, text="", font=font).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)

        row = 5
        ctk.CTkButton(frame, text="Editar Colonia", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color, command= lambda: self.editar_colonia()).grid(row=row, column=0, padx = padx, pady=pady)
        ctk.CTkButton(frame,text="Limpiar campos",width=width,font=font,corner_radius=corner_radius,fg_color=button_color,text_color=button_text_color,command=self.limpiar_campos).grid(row=row, column=2, padx=padx, pady=pady)
        ctk.CTkButton(frame, text="Salir", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color, command=self.root.destroy).grid(row=row, column=3, padx = padx, pady=pady)
        
        self.root.mainloop()

    def editar_colonia(self):
        col = colonia()
        
        col_nom = self.combobox_colonia.get().strip()
        localidad = self.combobox_ciudad.get().strip()
        n_col_nom = self.entry_colonia.get().strip()

        if not all([localidad, col_nom, n_col_nom]):
            CTkMessagebox(title="Error", message="Debe llenar todos los campos.", icon="warning")
            return

        result_col = col.buscar_colonia(col_nom, localidad)
        if not result_col:
            CTkMessagebox(title="Error", message="Colonia no encontrada.", icon="warning")
            return

        ok = col.editar_colonia(col_nom, localidad, nuevo_nombre=n_col_nom)

        if ok:
            self.actualizar_colonias()
            CTkMessagebox(title="Éxito", message="Colonia editada correctamente.", icon="info")
        else:
            CTkMessagebox(title="Aviso", message="No se realizaron cambios.", icon="info")


    def limpiar_campos(self):
        self.combobox_ciudad.set("")
        self.combobox_colonia.set("")

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