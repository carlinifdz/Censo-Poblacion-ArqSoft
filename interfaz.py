# ui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import pandas as pd
import mysql.connector

# Importa tus modelos TAL CUAL los tiene tu compañero (no cambies nombres)
from database import get_connection
from domicilio import domicilio as DomicilioModel
from habitante import habitante as HabitanteModel

# ---------- Utilidades de DB ----------
def fetch_colonias():
    """Regresa [(id, 'Nombre - Municipio'), ...] para poblar combos."""
    conn = get_connection()
    if conn is None:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nombre, localidad FROM colonias ORDER BY localidad, nombre")
            rows = cur.fetchall()
            return [(r[0], f"{r[1]} - {r[2]}") for r in rows]
    finally:
        try: conn.close()
        except: pass

def fetch_municipios():
    conn = get_connection()
    if conn is None:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT localidad FROM colonias ORDER BY localidad")
            return [r[0] for r in cur.fetchall()]
    finally:
        try: conn.close()
        except: pass

def try_login(username, password):
    """Intenta validar contra tabla usuarios; si no existe, habilita demo admin/admin."""
    conn = get_connection()
    if conn is None:
        return False, "Sin conexión a BD"

    try:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT username, password FROM usuarios WHERE username=%s", (username,))
                row = cur.fetchone()
                if row:
                    return (password == row[1], None)  # simplificado (sin hash) para demo
                else:
                    return False, "Usuario no encontrado"
            except mysql.connector.Error:
                # No existe la tabla: modo demo
                if username == "admin" and password == "admin":
                    return True, None
                return False, "Credenciales inválidas (o sin tabla usuarios). Demo: admin/admin"
    finally:
        try: conn.close()
        except: pass

# ---------- Ventanas (Frames) ----------
class LoginFrame(ttk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master, padding=20)
        self.on_success = on_success
        ttk.Label(self, text="Censo de Población INEGI – Login", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0,12))
        ttk.Label(self, text="Usuario").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(self, text="Contraseña").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.user = ttk.Entry(self, width=30)
        self.pwd = ttk.Entry(self, width=30, show="*")
        self.user.grid(row=1, column=1, pady=5)
        self.pwd.grid(row=2, column=1, pady=5)
        ttk.Button(self, text="Ingresar", command=self.login).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Label(self, text="Tip (demo): admin / admin", foreground="#666").grid(row=4, column=0, columnspan=2)

    def login(self):
        ok, err = try_login(self.user.get().strip(), self.pwd.get().strip())
        if ok:
            self.on_success()
        else:
            messagebox.showerror("Login", err or "Credenciales inválidas")

class MenuFrame(ttk.Frame):
    def __init__(self, master, go_domicilios, go_habitantes, go_reportes, do_import_colonias, do_logout, do_exit):
        super().__init__(master, padding=20)
        ttk.Label(self, text="Menú principal", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0,12))

        ttk.Button(self, text="CRUD Domicilios", command=go_domicilios).grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        ttk.Button(self, text="CRUD Habitantes", command=go_habitantes).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        ttk.Button(self, text="Reportes y Gráficas", command=go_reportes).grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        ttk.Button(self, text="Importar Colonias (CSV)", command=do_import_colonias).grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        sep = ttk.Separator(self, orient="horizontal")
        sep.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

        ttk.Button(self, text="Cerrar sesión", command=do_logout).grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        ttk.Button(self, text="Salir", command=do_exit).grid(row=4, column=1, sticky="ew", padx=5, pady=5)

class DomiciliosFrame(ttk.Frame):
    TIPOS = ["Vivienda de concreto","Vivienda de adobe(antiguo)","Vivienda de ladrillo","Vivienda de madera",
             "Vivienda de cartón","Casa de piedra","Vivienda prefabricada","Material Ecológico",
             "Casa de paja, ramas o caña","Material Adobe Moderno"]

    def __init__(self, master, go_back):
        super().__init__(master, padding=16)
        self.go_back = go_back
        ttk.Label(self, text="Domicilios (CRUD)", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=(0,12), sticky="w")

        # Formulario
        ttk.Label(self, text="Tipo vivienda").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(self, text="Calle").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        ttk.Label(self, text="Número").grid(row=2, column=2, sticky="e", padx=5, pady=5)
        ttk.Label(self, text="Colonia").grid(row=2, column=0, sticky="e", padx=5, pady=5)

        self.tipo = ttk.Combobox(self, values=self.TIPOS, state="readonly", width=35)
        self.calle = ttk.Entry(self, width=35)
        self.numero = ttk.Entry(self, width=20)
        self.colonia_map = fetch_colonias()
        self.colonia = ttk.Combobox(self, values=[c[1] for c in self.colonia_map], state="readonly", width=35)

        self.tipo.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.calle.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.numero.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        self.colonia.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Botones
        ttk.Button(self, text="Registrar", command=self.registrar).grid(row=3, column=1, padx=5, pady=10, sticky="ew")
        ttk.Button(self, text="Editar", command=self.editar).grid(row=3, column=2, padx=5, pady=10, sticky="ew")
        ttk.Button(self, text="Eliminar", command=self.eliminar).grid(row=3, column=3, padx=5, pady=10, sticky="ew")

        sep = ttk.Separator(self, orient="horizontal")
        sep.grid(row=4, column=0, columnspan=4, sticky="ew", pady=10)
        ttk.Button(self, text="Volver al menú", command=self.go_back).grid(row=5, column=0, columnspan=4, pady=5)

        self.model = DomicilioModel()

    def _selected_colonia_id(self):
        idx = self.colonia.current()
        return None if idx < 0 else self.colonia_map[idx][0]

    def registrar(self):
        cid = self._selected_colonia_id()
        if not cid or not self.tipo.get() or not self.calle.get() or not self.numero.get():
            messagebox.showwarning("Validación","Completa todos los campos.")
            return
        ok = self.model.registrar_domicilio(self.tipo.get(), self.calle.get().strip(), self.numero.get().strip(), cid)
        messagebox.showinfo("Domicilio", "Registrado" if ok else "No se registró")

    def editar(self):
        cid = self._selected_colonia_id()
        if not cid or not self.calle.get() or not self.numero.get():
            messagebox.showwarning("Validación","Indica colonia, calle y número del registro a editar.")
            return
        ok = self.model.editar_domicilio(
            self.calle.get().strip(),
            self.numero.get().strip(),
            cid,
            nuevo_tipo_casa=self.tipo.get() or None
        )
        messagebox.showinfo("Domicilio", "Actualizado" if ok else "No se actualizó")

    def eliminar(self):
        cid = self._selected_colonia_id()
        if not cid or not self.calle.get() or not self.numero.get():
            messagebox.showwarning("Validación","Indica colonia, calle y número del registro a eliminar.")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar domicilio?"):
            return
        ok = self.model.eliminar_domicilio(self.calle.get().strip(), self.numero.get().strip(), cid)
        messagebox.showinfo("Domicilio", "Eliminado" if ok else "No se eliminó")

class HabitantesFrame(ttk.Frame):
    def __init__(self, master, go_back):
        super().__init__(master, padding=16)
        self.go_back = go_back
        ttk.Label(self, text="Habitantes (CRUD)", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=(0,12), sticky="w")

        ttk.Label(self, text="Nombre").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(self, text="Fecha nac. (YYYY-MM-DD)").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        ttk.Label(self, text="Sexo (F/M/X)").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(self, text="Domicilio (Colonia)").grid(row=2, column=2, sticky="e", padx=5, pady=5)
        ttk.Label(self, text="Actividad económica").grid(row=3, column=0, sticky="e", padx=5, pady=5)

        self.nombre = ttk.Entry(self, width=35)
        self.fecha = ttk.Entry(self, width=20)
        self.sexo = ttk.Combobox(self, values=["F","M","X"], state="readonly", width=5)
        self.colonia_map = fetch_colonias()
        self.colonia = ttk.Combobox(self, values=[c[1] for c in self.colonia_map], state="readonly", width=40)
        self.act = ttk.Entry(self, width=40)

        self.nombre.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.fecha.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.sexo.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.colonia.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        self.act.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(self, text="Registrar", command=self.registrar).grid(row=4, column=1, padx=5, pady=10, sticky="ew")
        ttk.Button(self, text="Editar", command=self.editar).grid(row=4, column=2, padx=5, pady=10, sticky="ew")
        ttk.Button(self, text="Eliminar", command=self.eliminar).grid(row=4, column=3, padx=5, pady=10, sticky="ew")

        sep = ttk.Separator(self, orient="horizontal")
        sep.grid(row=5, column=0, columnspan=4, sticky="ew", pady=10)
        ttk.Button(self, text="Volver al menú", command=self.go_back).grid(row=6, column=0, columnspan=4, pady=5)

        self.dom_model = DomicilioModel()
        self.hab_model = HabitanteModel()

    def _domicilio_id_by_calle_numero(self, calle, numero, colonia_id):
        """Busca el domicilio para vincular habitante → domicilio_id."""
        # usa el método existente de tu compañero
        res = self.dom_model.buscar_domicilio(calle, numero, colonia_id)
        if not res:
            return None
        # buscar_domicilio de tu compa devuelve tuple; id está en [0]
        return res[0] if isinstance(res, tuple) else res.get("id")

    def registrar(self):
        if not (self.nombre.get() and self.sexo.get() and self.colonia.current() >= 0):
            messagebox.showwarning("Validación","Completa nombre, sexo y colonia.")
            return
        # pedimos calle/numero para ubicar el domicilio (requisito del modelo de tu compa)
        calle = simple_prompt(self, "Calle del domicilio")
        numero = simple_prompt(self, "Número")
        if not calle or not numero:
            return
        colonia_id = self.colonia_map[self.colonia.current()][0]
        dom_id = self._domicilio_id_by_calle_numero(calle.strip(), numero.strip(), colonia_id)
        if not dom_id:
            messagebox.showerror("Habitante","Primero registra el domicilio.")
            return
        ok = self.hab_model.registrar_habitante(
            self.nombre.get().strip(),
            self.fecha.get().strip() or None,
            self.sexo.get(),
            dom_id,
            self.act.get().strip() or None
        )
        messagebox.showinfo("Habitante", "Registrado" if ok else "No se registró")

    def editar(self):
        if not (self.nombre.get() and self.colonia.current() >= 0):
            messagebox.showwarning("Validación","Indica nombre y colonia (para localizar).")
            return
        calle = simple_prompt(self, "Calle actual del domicilio")
        numero = simple_prompt(self, "Número actual")
        if not calle or not numero:
            return
        colonia_id = self.colonia_map[self.colonia.current()][0]
        ok = self.hab_model.editar_habitante(
            self.nombre.get().strip(),
            domicilio_id=self._domicilio_id_by_calle_numero(calle.strip(), numero.strip(), colonia_id),
            nuevo_nombre=self.nombre.get().strip(),
            nuevo_sexo=self.sexo.get() or None,
            nuevo_act_eco=self.act.get().strip() or None,
            nuevo_fecha_nac=self.fecha.get().strip() or None
        )
        messagebox.showinfo("Habitante", "Actualizado" if ok else "No se actualizó")

    def eliminar(self):
        if not (self.nombre.get() and self.colonia.current() >= 0):
            messagebox.showwarning("Validación","Indica nombre y colonia.")
            return
        calle = simple_prompt(self, "Calle del domicilio")
        numero = simple_prompt(self, "Número")
        if not calle or not numero:
            return
        colonia_id = self.colonia_map[self.colonia.current()][0]
        ok = self.hab_model.eliminar_habitante(self.nombre.get().strip(),
                                               domicilio_id=self._domicilio_id_by_calle_numero(calle.strip(), numero.strip(), colonia_id))
        messagebox.showinfo("Habitante", "Eliminado" if ok else "No se eliminó")

class ReportesFrame(ttk.Frame):
    def __init__(self, master, go_back):
        super().__init__(master, padding=16)
        self.go_back = go_back
        ttk.Label(self, text="Reportes y Gráficas", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=(0,12), sticky="w")

        ttk.Button(self, text="Conteo por tipo de vivienda", command=self.reporte_tipos).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(self, text="Habitantes por municipio", command=self.reporte_municipios).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(self, text="Exportar ambos a CSV", command=self.exportar_csv).grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        sep = ttk.Separator(self, orient="horizontal")
        sep.grid(row=2, column=0, columnspan=3, sticky="ew", pady=10)
        ttk.Button(self, text="Volver al menú", command=self.go_back).grid(row=3, column=0, columnspan=3, pady=5)

        # Embebido Matplotlib
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure
        self.Figure = Figure
        self.FigureCanvasTkAgg = FigureCanvasTkAgg
        self.canvas = None

    def _plot(self, labels, values, title):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        fig = self.Figure(figsize=(6,3), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(labels, values)  # sin estilos, como piden
        ax.set_title(title)
        ax.tick_params(axis='x', rotation=20)
        self.canvas = self.FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=3, pady=10)

    def _query(self, sql, params=None):
        conn = get_connection()
        if conn is None:
            messagebox.showerror("BD","Sin conexión a la base de datos.")
            return []
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params or ())
                return cur.fetchall()
        finally:
            try: conn.close()
            except: pass

    def reporte_tipos(self):
        rows = self._query("""
            SELECT tipo_casa, COUNT(*) as total
            FROM domicilios
            GROUP BY tipo_casa
            ORDER BY total DESC
        """)
        if not rows:
            messagebox.showinfo("Reporte","Sin datos.")
            return
        labels = [r[0] for r in rows]
        values = [r[1] for r in rows]
        self._plot(labels, values, "Viviendas por tipo")

    def reporte_municipios(self):
        rows = self._query("""
            SELECT c.localidad AS municipio, COUNT(h.id) AS total_habitantes
            FROM habitantes h
            JOIN domicilios d ON d.id = h.domicilio_id
            JOIN colonias c ON c.id = d.colonia_id
            GROUP BY c.localidad
            ORDER BY total_habitantes DESC
            LIMIT 12
        """)
        if not rows:
            messagebox.showinfo("Reporte","Sin datos.")
            return
        labels = [r[0] for r in rows]
        values = [r[1] for r in rows]
        self._plot(labels, values, "Habitantes por municipio (Top 12)")

    def exportar_csv(self):
        # Exporta ambos reportes a CSV en carpeta elegida
        folder = filedialog.askdirectory(title="Elige carpeta de exportación")
        if not folder:
            return
        # Tipos vivienda
        tipos = self._query("""
            SELECT tipo_casa, COUNT(*) as total
            FROM domicilios
            GROUP BY tipo_casa
            ORDER BY total DESC
        """)
        df1 = pd.DataFrame(tipos, columns=["tipo_casa","total"])
        df1.to_csv(f"{folder}/reporte_tipos_vivienda.csv", index=False, encoding="utf-8")

        # Habitantes por municipio
        mun = self._query("""
            SELECT c.localidad AS municipio, COUNT(h.id) AS total_habitantes
            FROM habitantes h
            JOIN domicilios d ON d.id = h.domicilio_id
            JOIN colonias c ON c.id = d.colonia_id
            GROUP BY c.localidad
        """)
        df2 = pd.DataFrame(mun, columns=["municipio","total_habitantes"])
        df2.to_csv(f"{folder}/reporte_habitantes_municipio.csv", index=False, encoding="utf-8")
        messagebox.showinfo("Exportación","CSV generados en la carpeta seleccionada.")

class ImportColoniasFrame(ttk.Frame):
    def __init__(self, master, go_back):
        super().__init__(master, padding=16)
        self.go_back = go_back
        ttk.Label(self, text="Importar Colonias (INEGI)", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=(0,12), sticky="w")
        ttk.Label(self, text="Selecciona CSV (NOM_LOC, NOM_MUN, AMBITO, LAT_DECIMAL, LON_DECIMAL)").grid(row=1, column=0, columnspan=3, pady=5)
        ttk.Button(self, text="Elegir CSV…", command=self.pick_csv).grid(row=2, column=0, padx=5, pady=10, sticky="w")
        ttk.Button(self, text="Volver al menú", command=self.go_back).grid(row=3, column=0, columnspan=3, pady=5)

    def pick_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV","*.csv")])
        if not path: return
        try:
            df = pd.read_csv(path, dtype=str).fillna("")
            need = ["NOM_LOC","NOM_MUN","AMBITO","LAT_DECIMAL","LON_DECIMAL"]
            if any(c not in df.columns for c in need):
                messagebox.showerror("CSV","Columnas requeridas faltantes.")
                return
            data = []
            for _, r in df.iterrows():
                data.append((
                    r["NOM_LOC"].strip(), r["NOM_MUN"].strip(), r["AMBITO"].strip(),
                    r["LAT_DECIMAL"] or None, r["LON_DECIMAL"] or None
                ))
            conn = get_connection()
            if conn is None:
                messagebox.showerror("BD","Sin conexión a la base de datos.")
                return
            try:
                with conn:
                    with conn.cursor() as cur:
                        cur.executemany("""
                            INSERT INTO colonias (nombre, localidad, ambito, latitud, longitud)
                            VALUES (%s,%s,%s,%s,%s)
                            ON DUPLICATE KEY UPDATE ambito=VALUES(ambito), latitud=VALUES(latitud), longitud=VALUES(longitud)
                        """, data)
                messagebox.showinfo("Importación", f"Importadas/actualizadas {len(data)} colonias.")
            finally:
                try: conn.close()
                except: pass
        except Exception as e:
            messagebox.showerror("CSV", f"Error al importar: {e}")

# ---------- Helpers UI ----------
def simple_prompt(parent, title):
    win = tk.Toplevel(parent)
    win.title(title)
    win.grab_set()
    entry = ttk.Entry(win, width=30)
    ttk.Label(win, text=title).grid(row=0, column=0, padx=10, pady=8)
    entry.grid(row=1, column=0, padx=10, pady=8)
    res = {"val": None}
    def ok():
        res["val"] = entry.get().strip()
        win.destroy()
    ttk.Button(win, text="OK", command=ok).grid(row=2, column=0, pady=8)
    win.wait_window()
    return res["val"]

# ---------- App ----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Censo de población INEGI – Desktop (MVC)")
        self.geometry("900x520")
        self.style = ttk.Style(self)
        self.style.theme_use("vista" if "vista" in self.style.theme_names() else "clam")
        self._show_login()

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _show_login(self):
        self._clear()
        LoginFrame(self, self._show_menu).pack(fill="both", expand=True)

    def _show_menu(self):
        self._clear()
        MenuFrame(
            self,
            go_domicilios=self._show_domicilios,
            go_habitantes=self._show_habitantes,
            go_reportes=self._show_reportes,
            do_import_colonias=self._show_import_colonias,
            do_logout=self._show_login,
            do_exit=self.destroy
        ).pack(fill="both", expand=True)

    def _show_domicilios(self):
        self._clear()
        DomiciliosFrame(self, go_back=self._show_menu).pack(fill="both", expand=True)

    def _show_habitantes(self):
        self._clear()
        HabitantesFrame(self, go_back=self._show_menu).pack(fill="both", expand=True)

    def _show_reportes(self):
        self._clear()
        ReportesFrame(self, go_back=self._show_menu).pack(fill="both", expand=True)

    def _show_import_colonias(self):
        self._clear()
        ImportColoniasFrame(self, go_back=self._show_menu).pack(fill="both", expand=True)

if __name__ == "__main__":
    App().mainloop()
