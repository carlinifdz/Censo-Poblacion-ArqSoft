import customtkinter as ctk
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


    nuevo_entry_nombre.delete(0, "end")
    nuevo_entry_fec_anno.delete(0, "end")
    nuevo_entry_fec_mes.delete(0, "end")
    nuevo_entry_fec_dia.delete(0, "end")
    nuevo_entry_act_eco.configure(state="normal")
    nuevo_entry_act_eco.delete(0, "end")

    nuevo_combobox_sexo.set("")

    n_checkbox_var.set("si")
    n_on_checkbox_change()

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

values_ciudad=["si","no"]
values_colonia=["si","no"]
values_t_vivienda=["Vivienda de concreto","Vivienda de adobe(antiguo)","Vivienda de ladrillo","Vivienda de madera","Vivienda de cartón",
        "Casa de piedra","Vivienda prefabricada","Material Ecológico","Casa de paja, ramas o caña","Material Adobe Moderno"]

row = 0
ctk.CTkLabel(frame, text="Registro de Vivienda y Habitante", font=font_title).grid(row=row, column=0, sticky = "w", padx =padx, pady=10, columnspan=2)

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
ctk.CTkLabel(frame, text="Editar Habitante: ", font=font_title).grid(row=row, column=0, sticky = "w", padx = padx, pady=10, columnspan=2)

row = 10
ctk.CTkLabel(frame, text="Nombre: ", font=font).grid(row=row, sticky = "e", column=0, padx = padx, pady=pady)
nuevo_entry_nombre=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
nuevo_entry_nombre.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

ctk.CTkLabel(frame, text="Sexo(M/F): ", font=font).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
nuevo_combobox_sexo=ctk.CTkComboBox(frame, values=["M", "F"], width=75,corner_radius=corner_radius, state="readonly")
nuevo_combobox_sexo.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)

row = 11
ctk.CTkLabel(frame, text="Fecha Nacimiento:     Año: ", font=font).grid(row=row, column=0, sticky = "e", padx = padx, pady=pady)
nuevo_entry_fec_anno=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
nuevo_entry_fec_anno.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

ctk.CTkLabel(frame, text="Mes: ", font=font).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
nuevo_entry_fec_mes=ctk.CTkEntry(frame, width=50, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
nuevo_entry_fec_mes.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)

ctk.CTkLabel(frame, text="Día: ", font=font).grid(row=row, column=4, sticky = "e", padx = padx, pady=pady)
nuevo_entry_fec_dia=ctk.CTkEntry(frame, width=50, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
nuevo_entry_fec_dia.grid(row=row, column=5, sticky = "w", padx = padx, pady=pady)

row = 12
ctk.CTkLabel(frame, text="Actividad Económica: ", font=font).grid(row=row, sticky = "e", column=0, padx = padx, pady=pady)
nuevo_entry_act_eco=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
nuevo_entry_act_eco.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

row = 13
def n_on_checkbox_change():
    if n_checkbox_var.get() == "si":
        nuevo_entry_act_eco.configure(state="normal")
        nuevo_entry_act_eco.delete(0, "end")
    else:
        nuevo_entry_act_eco.configure(state="normal")
        nuevo_entry_act_eco.delete(0, "end")
        nuevo_entry_act_eco.insert(0, "Ninguna")
        nuevo_entry_act_eco.configure(state="disabled")

n_checkbox_var = ctk.StringVar(value="si")
n_checkbox = ctk.CTkCheckBox(
    frame,
    text="¿Tiene actividad económica?",
    variable=n_checkbox_var,
    onvalue="si",
    offvalue="no",
    command=n_on_checkbox_change
)

n_checkbox.grid(row=row, column=0, padx=padx, pady=pady, sticky="w")

row = 15
ctk.CTkLabel(frame, text="", font=font_title).grid(row=row, column=0, sticky = "w", padx = padx, pady=10, columnspan=2)

row = 16
ctk.CTkButton(frame, text="Editar Habitante", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color).grid(row=row, column=0, padx = padx, pady=pady)
ctk.CTkButton(frame,text="Limpiar campos",width=width,font=font,corner_radius=corner_radius,fg_color=button_color,text_color=button_text_color,command=limpiar_campos).grid(row=row, column=3, padx=padx, pady=pady)

root.mainloop()