import customtkinter as ctk
import config

import customtkinter as ctk
import config

def limpiar_campos():
    combobox_ciudad.set("")
    entry_colonia.delete(0, "end")
    nuevo_combobox_ciudad.set("")
    nuevo_entry_colonia.delete(0, "end")

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

row = 0
ctk.CTkLabel(frame, text="Registro de Colonias", font=font_title).grid(row=row, column=0, sticky = "w", padx =padx, pady=10, columnspan=2)

row = 1
ctk.CTkLabel(frame, text="Ciudad (Municipio): ", font=font).grid(row=row, column=0, sticky = "e", padx = padx, pady=pady)
combobox_ciudad=ctk.CTkComboBox(frame, values=values_ciudad, width=width, corner_radius=corner_radius)
combobox_ciudad.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

ctk.CTkLabel(frame, text="Nombre: ", font=font).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
entry_colonia=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
entry_colonia.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)

row = 3
ctk.CTkLabel(frame, text="Editar Colonias", font=font_title).grid(row=row, column=0, sticky = "w", padx =padx, pady=10, columnspan=2)

row = 4
ctk.CTkLabel(frame, text="Ciudad (Municipio): ", font=font).grid(row=row, column=0, sticky = "e", padx = padx, pady=pady)
nuevo_combobox_ciudad=ctk.CTkComboBox(frame, values=values_ciudad, width=width, corner_radius=corner_radius)
nuevo_combobox_ciudad.grid(row=row, column=1, sticky = "w", padx = padx, pady=pady)

ctk.CTkLabel(frame, text="Nombre: ", font=font).grid(row=row, column=2, sticky = "e", padx = padx, pady=pady)
nuevo_entry_colonia=ctk.CTkEntry(frame, width=width, corner_radius=corner_radius)
nuevo_entry_colonia.grid(row=row, column=3, sticky = "w", padx = padx, pady=pady)

row = 5
ctk.CTkLabel(frame, text="", font=font).grid(row=row, column=0, sticky = "e", padx = padx, pady=pady)

row = 6
ctk.CTkButton(frame, text="Registrar Colonia", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color).grid(row=row, column=0, padx = padx, pady=pady)
ctk.CTkButton(frame, text="Eliminar Colonia", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color).grid(row=row, column=1, padx = padx, pady=pady)
ctk.CTkButton(frame, text="Editar Colonia", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color).grid(row=row, column=2, padx = padx, pady=pady)
ctk.CTkButton(frame,text="Limpiar campos",width=width,font=font,corner_radius=corner_radius,fg_color=button_color,text_color=button_text_color,command=limpiar_campos).grid(row=row, column=3, padx=padx, pady=pady)

root.mainloop()