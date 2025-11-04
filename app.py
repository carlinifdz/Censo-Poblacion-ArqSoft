import tkinter as tk
from tkinter import ttk

from core.session import session
from core.event_bus import bus

from views.login_view import LoginView
from views.menu_view import MenuView
from views.domicilios_view import DomiciliosView
from views.habitantes_view import HabitantesView
from views.reportes_view import ReportesView
from views.registro_combinado_view import RegistroCombinadoView

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Censo de población INEGI – Desktop (MVC)")
        self.geometry("980x800")
        self.style = ttk.Style(self)
        self.style.theme_use("vista" if "vista" in self.style.theme_names() else "clam")

        # una sola instancia de Reportes + dirty flag (para Observer)
        self.reportes_frame = None
        self.reports_dirty = False

        # subscripciones globales a cambios de datos
        bus.subscribe("domicilio_changed", self._on_data_changed)
        bus.subscribe("habitante_changed", self._on_data_changed)

        self._show_login()

    # -- Observer handler --
    def _on_data_changed(self, *a, **kw):
        if self.reportes_frame and self.reportes_frame.winfo_ismapped():
            self.after(0, self.reportes_frame.refresh_all)
        else:
            self.reports_dirty = True

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    # -- rutas --
    def _show_login(self):
        self._clear()
        LoginView(self, on_success=self._show_menu).pack(fill="both", expand=True)

    def _show_menu(self):
        self._clear()
        MenuView(
            self,
            username=session.user or "—",
            go_domicilios=self._show_domicilios,
            go_habitantes=self._show_habitantes,
            go_reportes=self._show_reportes,
            go_registro=self._show_registro_combinado,
            do_logout=self._logout,
            do_exit=self.destroy
        ).pack(fill="both", expand=True)

    def _logout(self):
        session.logout()
        self._show_login()

    def _show_domicilios(self):
        self._clear()
        DomiciliosView(self, go_back=self._show_menu).pack(fill="both", expand=True)

    def _show_habitantes(self):
        self._clear()
        HabitantesView(self, go_back=self._show_menu).pack(fill="both", expand=True)

    def _show_reportes(self):
        self._clear()
        if self.reportes_frame is None:
            self.reportes_frame = ReportesView(self, go_back=self._show_menu)
        self.reportes_frame.pack(fill="both", expand=True)
        if self.reports_dirty:
            self.reportes_frame.refresh_all()
            self.reports_dirty = False

    def _show_registro_combinado(self):
        self._clear()
        RegistroCombinadoView(self, go_back=self._show_menu).pack(fill="both", expand=True)
if __name__ == "__main__":
    App().mainloop()
