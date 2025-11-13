import customtkinter as ctk
from tkinter import ttk
import config

def limpiar_campos():
    entry_calle.delete(0, "end")
    entry_num.delete(0, "end")
    entry_nombre.delete(0, "end")
    entry_fec_anno.delete(0, "end")
    entry_fec_mes.delete(0, "end")
    entry_fec_dia.delete(0, "end")
    entry_act_eco.configure(state="normal")
    entry_act_eco.delete(0, "end")

    combobox_ciudad.set("")
    combobox_colonia.set("")
    combobox_t_vivienda.set("")
    combobox_sexo.set("")

    checkbox_var.set("si")
    on_checkbox_change()

ctk.set_appearance_mode("light")

root = ctk.CTk()
root.title("Censo INEGI")
root.geometry("1200x800")
root.resizable(False, False)
root.configure(fg_color=config.bg_color)

frame = ctk.CTkFrame(root, corner_radius=12, fg_color=config.frame_color)
frame.place(relx=0.01, rely=0.01, anchor="nw")

font_title = config.font_title
font = config.font

corner_radius = config.corner_radius
button_color = config.button_color
button_text_color = config.button_text_color
pady = config.pady
padx = config.padx

width = 200

values_ciudad = ["si", "no"]
values_colonia = ["si", "no"]
values_t_vivienda = [
    "Vivienda de concreto", "Vivienda de adobe(antiguo)", "Vivienda de ladrillo",
    "Vivienda de madera", "Vivienda de cartón", "Casa de piedra",
    "Vivienda prefabricada", "Material Ecológico", "Casa de paja, ramas o caña",
    "Material Adobe Moderno"
]

row = 0
ctk.CTkLabel(frame, text="Consultas de Colonia, Vivienda y Habitante", font=font_title).grid(row=row, column=0, sticky="w", padx=padx, pady=10, columnspan=6)

row = 1
ctk.CTkLabel(frame, text="Ciudad (Municipio): ", font=font).grid(row=row, column=0, sticky = "e", padx = padx, pady=pady)
combobox_ciudad=ctk.CTkComboBox(frame, values=values_ciudad, width=width, corner_radius=corner_radius)
combobox_ciudad.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

ctk.CTkLabel(frame, text="Colonia: ", font=font).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
combobox_colonia=ctk.CTkComboBox(frame, values=values_colonia, width=width, corner_radius=corner_radius)
combobox_colonia.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)

row = 2
ctk.CTkLabel(frame, text="Domicilio: ", font=font_title).grid(row=row, column=0, sticky = "w", padx = padx, pady=10, columnspan=2)

row = 3
ctk.CTkLabel(frame, text="Tipo Vivienda: ", font=font).grid(row=row, sticky = "e", column=0, padx = padx, pady=pady)
combobox_t_vivienda=ctk.CTkComboBox(frame, values=values_t_vivienda, width=width, corner_radius=corner_radius, state="readonly")
combobox_t_vivienda.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

ctk.CTkLabel(frame, text="Calle: ", font=font).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
entry_calle=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
entry_calle.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)

def solo_numeros(valor):
    return valor.isdigit() or valor == ""

validacion = root.register(solo_numeros)

ctk.CTkLabel(frame, text="Numero: ", font=font).grid(row=row, column=4, sticky="e", padx=padx, pady=pady)
entry_num = ctk.CTkEntry(frame, width=width, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
entry_num.grid(row=row, column=5, sticky="w", padx=padx, pady=pady)

row = 4
ctk.CTkLabel(frame, text="Habitante: ", font=font_title).grid(row=row, column=0, sticky = "w", padx = padx, pady=10, columnspan=2)

row = 5
ctk.CTkLabel(frame, text="Nombre: ", font=font).grid(row=row, sticky = "e", column=0, padx = padx, pady=pady)
entry_nombre=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
entry_nombre.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

ctk.CTkLabel(frame, text="Sexo(M/F): ", font=font).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
combobox_sexo=ctk.CTkComboBox(frame, values=["M", "F"], width=75,corner_radius=corner_radius, state="readonly")
combobox_sexo.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)

row = 6

def solo_numeros(valor):
    return valor.isdigit() or valor == ""

validacion = root.register(solo_numeros)

ctk.CTkLabel(frame, text="Fecha Nacimiento:     Año: ", font=font).grid(row=row, column=0, sticky = "e", padx = padx, pady=pady)
entry_fec_anno=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
entry_fec_anno.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

ctk.CTkLabel(frame, text="Mes: ", font=font).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
entry_fec_mes=ctk.CTkEntry(frame, width=50, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
entry_fec_mes.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)

ctk.CTkLabel(frame, text="Día: ", font=font).grid(row=row, column=4, sticky = "e", padx = padx, pady=pady)
entry_fec_dia=ctk.CTkEntry(frame, width=50, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
entry_fec_dia.grid(row=row, column=5, sticky = "w", padx = padx, pady=pady)

row = 7
ctk.CTkLabel(frame, text="Actividad Económica: ", font=font).grid(row=row, sticky = "e", column=0, padx = padx, pady=pady)
entry_act_eco=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
entry_act_eco.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

row = 8
def on_checkbox_change():
    if checkbox_var.get() == "si":
        entry_act_eco.configure(state="normal")
        entry_act_eco.delete(0, "end")
    else:
        entry_act_eco.configure(state="normal")
        entry_act_eco.delete(0, "end")
        entry_act_eco.insert(0, "Ninguna")
        entry_act_eco.configure(state="disabled")

checkbox_var = ctk.StringVar(value="si")
checkbox = ctk.CTkCheckBox(
    frame,
    text="¿Tiene actividad económica?",
    variable=checkbox_var,
    onvalue="si",
    offvalue="no",
    command=on_checkbox_change
)

checkbox.grid(row=row, column=0, padx=padx, pady=pady, sticky="w")

row = 9
ctk.CTkLabel(frame, text="Incluir información: ", font=font_title).grid(row=row, column=0, sticky = "w", padx = padx, pady=10, columnspan=2)

row = 10

var1 = ctk.BooleanVar()
var2 = ctk.BooleanVar()
var3 = ctk.BooleanVar()
var4 = ctk.BooleanVar()

ctk.CTkCheckBox(frame, text="Localidad", variable=var1).grid(row=row, column=0, sticky = "w", padx = padx, pady=10, columnspan=2)
ctk.CTkCheckBox(frame, text="Colonia", variable=var2).grid(row=row, column=1, sticky = "w", padx = padx, pady=10, columnspan=2)
ctk.CTkCheckBox(frame, text="Domicilio", variable=var3).grid(row=row, column=2, sticky = "w", padx = padx, pady=10, columnspan=2)
ctk.CTkCheckBox(frame, text="Habitante", variable=var4).grid(row=row, column=3, sticky = "w", padx = padx, pady=10, columnspan=2)

row = 11
ctk.CTkButton(frame, text="Buscar por Ciudad", width=width, font=font, corner_radius=corner_radius,fg_color=button_color, text_color=button_text_color).grid(row=row, column=0, padx=padx, pady=pady)
ctk.CTkButton(frame, text="Buscar por Colonia", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color).grid(row=row, column=1, padx=padx, pady=pady)
ctk.CTkButton(frame, text="Buscar por Domicilio", width=width, font=font, corner_radius=corner_radius,fg_color=button_color, text_color=button_text_color).grid(row=row, column=2, padx=padx, pady=pady)
ctk.CTkButton(frame,text="Limpiar campos",width=width,font=font,corner_radius=corner_radius,fg_color=button_color,text_color=button_text_color,command=limpiar_campos).grid(row=row, column=3, padx=padx, pady=pady)

# Ejemplo de tabla, reemplaza esto por los resultados de la busqueda
row = 12
tabla_frame = ctk.CTkFrame(frame, fg_color="white", corner_radius=8)
tabla_frame.grid(row=row, column=0, columnspan=6, padx=padx, pady=15, sticky="nsew")

scrollbar = ttk.Scrollbar(tabla_frame)
scrollbar.grid(row=0, column=1, sticky="ns")



tabla = ttk.Treeview(
    tabla_frame,
    columns=("col1", "col2", "col3"),
    show="headings",
    yscrollcommand=scrollbar.set,
    height=10
)
tabla.grid(row=0, column=0, sticky="nsew")

tabla_frame.grid_rowconfigure(0, weight=1)
tabla_frame.grid_columnconfigure(0, weight=1)

scrollbar.config(command=tabla.yview)

tabla.heading("col1", text="ID")
tabla.heading("col2", text="Nombre")
tabla.heading("col3", text="Edad")

tabla.column("col1", width=50, anchor="center")
tabla.column("col2", width=200, anchor="w")
tabla.column("col3", width=100, anchor="center")



datos = [
    (1, "Carla", 25),
    (2, "Luis", 30),
    (3, "Ana", 22),
]
for fila in datos:
    tabla.insert("", "end", values=fila)

root.mainloop()