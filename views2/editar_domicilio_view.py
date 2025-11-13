import customtkinter as ctk
import config

def limpiar_campos():
    entry_calle.delete(0, "end")
    entry_num.delete(0, "end")

    combobox_ciudad.set("")
    combobox_colonia.set("")
    combobox_t_vivienda.set("")

    nuevo_entry_calle.delete(0, "end")
    nuevo_entry_num.delete(0, "end")

    nuevo_combobox_ciudad.set("")
    nuevo_combobox_colonia.set("")
    nuevo_combobox_t_vivienda.set("")

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

#valores de ciudad y colonia de muestra

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
ctk.CTkLabel(frame, text="Editar Vivienda", font=font_title).grid(row=row, column=0, sticky = "w", padx =padx, pady=10, columnspan=2)

row = 5
ctk.CTkLabel(frame, text="Ciudad (Municipio): ", font=font).grid(row=row, column=0, sticky = "e", padx = padx, pady=pady)
nuevo_combobox_ciudad=ctk.CTkComboBox(frame, values=values_ciudad, width=width, corner_radius=corner_radius)
nuevo_combobox_ciudad.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

ctk.CTkLabel(frame, text="Colonia: ", font=font).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
nuevo_combobox_colonia=ctk.CTkComboBox(frame, values=values_colonia, width=width, corner_radius=corner_radius)
nuevo_combobox_colonia.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)

row = 6
ctk.CTkLabel(frame, text="Domicilio: ", font=font_title).grid(row=row, column=0, sticky = "w", padx = padx, pady=10, columnspan=2)

row = 7
ctk.CTkLabel(frame, text="Tipo Vivienda: ", font=font).grid(row=row, sticky = "e", column=0, padx = padx, pady=pady)
nuevo_combobox_t_vivienda=ctk.CTkComboBox(frame, values=values_t_vivienda, width=width, corner_radius=corner_radius, state="readonly")
nuevo_combobox_t_vivienda.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

ctk.CTkLabel(frame, text="Calle: ", font=font).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
nuevo_entry_calle=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
nuevo_entry_calle.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)

ctk.CTkLabel(frame, text="Numero: ", font=font).grid(row=row, column=4, sticky="e", padx=padx, pady=pady)
nuevo_entry_num = ctk.CTkEntry(frame, width=width, corner_radius=corner_radius, validate="key", validatecommand=(validacion, "%P"))
nuevo_entry_num.grid(row=row, column=5, sticky="w", padx=padx, pady=pady)

row = 8
ctk.CTkLabel(frame, text="", font=font_title).grid(row=row, column=0, sticky = "w", padx = padx, pady=10, columnspan=2)

row = 9
ctk.CTkButton(frame, text="Editar Domicilio", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color).grid(row=row, column=0, padx = padx, pady=pady)
ctk.CTkButton(frame,text="Limpiar campos",width=width,font=font,corner_radius=corner_radius,fg_color=button_color,text_color=button_text_color,command=limpiar_campos).grid(row=row, column=3, padx=padx, pady=pady)


root.mainloop()
