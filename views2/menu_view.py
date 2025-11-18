import customtkinter as ctk
import config
from views2.login_view import LoginView
from views2.crud_domicilio_habitante_view import MainMenuCRUDHabitantes
from views2.editar_habitante_view import MainMenuEditHabitante
from views2.editar_domicilio_view import MainMenuEditDomicilio
from views2.editar_colonia_view import MainMenuEditColonia
from views2.dashboard_view import DashboardView
from views2.consultas_view import ConsultasView


class MainMenu():
    def __init__(self, user):
        self.user = user
        ctk.set_appearance_mode("light")

        self.root = ctk.CTk()
        self.root.title("Censo INEGI")
        self.root.geometry("400x500")
        self.root.configure(fg_color=config.bg_color)

        frame = ctk.CTkFrame(self.root, corner_radius=12, fg_color=config.frame_color)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        font_title = config.font_title
        font = config.font

        corner_radius = config.corner_radius
        button_color = config.button_color
        button_text_color = config.button_text_color
        pady = config.pady
        padx = config.padx

        for i in range(6):
            frame.grid_rowconfigure(i, pad=pady)
        frame.grid_columnconfigure(0, weight=1)

        width = 300

        ctk.CTkLabel(frame, text=f"Menú Principal - Usuario: {self.user}", font=font_title).grid(row=0, column=0, pady=25, columnspan=2)

        ctk.CTkButton(frame, text="Registro Colonia, Domicilio y Habitantes", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color, command=self.abrir_crud_domiciliohabitante).grid(row=1, column=0, pady=pady, columnspan=2)
        ctk.CTkButton(frame, text="Editar Colonia", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color, command=self.abrir_editar_colonia).grid(row=2, column=0, pady=pady, columnspan=2)
        ctk.CTkButton(frame, text="Editar Domicilio", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color, command=self.abrir_editar_domicilio).grid(row=3, column=0, pady=pady, columnspan=2)
        ctk.CTkButton(frame, text="Editar Habitante", width=width, font=font, corner_radius=corner_radius, fg_color=button_color, text_color=button_text_color, command=self.abrir_editar_habitante).grid(row=4, column=0, pady=pady, columnspan=2)
        ctk.CTkButton( frame,text="Consultas",width=width,font=font, corner_radius=corner_radius, fg_color="#2F6DA8", text_color="white", command=self.abrir_consultas ).grid(row=5, column=0, pady=pady, columnspan=2)
        ctk.CTkButton( frame, text="Dashboard / Reportes", width=width, font=font, corner_radius=corner_radius, fg_color=button_color,  text_color=button_text_color, command=self.abrir_dashboard).grid(row=6, column=0, pady=pady, columnspan=2)

        ctk.CTkLabel(frame, text="", font=font).grid(row=7, column=0, pady=0)

        ctk.CTkButton(frame, text="Cerrar sesión", width=(width/2)-padx, font=font, corner_radius=corner_radius,
                      fg_color=button_color, text_color=button_text_color, command=self.logout).grid(row=8, column=0,padx=padx, pady=pady)

        ctk.CTkButton(frame, text="Salir", width=(width/2)-padx, font=font, corner_radius=corner_radius,
                      fg_color=button_color, text_color=button_text_color, command=self.root.destroy).grid(row=8, column=1,padx=padx, pady=pady)

        self.root.mainloop()

    def abrir_crud_domiciliohabitante(self):
        MainMenuCRUDHabitantes(self.user)

    def abrir_editar_colonia(self):
        MainMenuEditColonia(self.user)

    def abrir_editar_domicilio(self):
        MainMenuEditDomicilio(self.user)

    def abrir_editar_habitante(self):
        MainMenuEditHabitante(self.user)

    def logout(self):
        self.root.destroy()
        LoginView(on_success=lambda username=self.user: MainMenu(username))

    def abrir_dashboard(self):
        DashboardView(self.user)
    
    def abrir_consultas(self):
        ConsultasView(self.user)


