import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from controllers.dashboard_controller import DashboardController
from controllers.pos_controller import POSController
from controllers.sales_controller import SalesController
from controllers.inventory_controller import InventoryController


class AppController:
    def __init__(self, root, user_id, username, role, db_path="pos_system.db"):
        self.root = root
        self.user_id = user_id
        self.username = username
        self.role = role
        self.db_path = db_path

        # Limpiar ventana (por si venimos del login)
        for widget in self.root.winfo_children():
            widget.destroy()

        # ======================
        #   LAYOUT PRINCIPAL
        # ======================
        main = ttk.Frame(self.root)
        main.pack(fill="both", expand=True)

        main.columnconfigure(0, weight=0)   # sidebar
        main.columnconfigure(1, weight=1)   # contenido
        main.rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ttk.Frame(main, padding=10)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Contenido central
        self.content = ttk.Frame(main, padding=10)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)

        # ======================
        #   BOTONES DEL MENÚ
        # ======================
        ttk.Label(
            self.sidebar,
            text=f"👤 {self.username}",
            font=("Segoe UI", 11, "bold")
        ).pack(pady=(0, 10))

        ttk.Button(
            self.sidebar,
            text="🏠 Dashboard",
            bootstyle=PRIMARY,
            command=self.show_dashboard
        ).pack(fill="x", pady=5)

        ttk.Button(
            self.sidebar,
            text="🛒 Punto de venta",
            bootstyle=INFO,
            command=self.show_pos
        ).pack(fill="x", pady=5)

        ttk.Button(
            self.sidebar,
            text="📦 Inventario",
            bootstyle=SECONDARY,
            command=self.show_inventory
        ).pack(fill="x", pady=5)

        ttk.Button(
            self.sidebar,
            text="🧾 Ventas / Facturas",
            bootstyle=SUCCESS,
            command=self.show_sales
        ).pack(fill="x", pady=5)

        # BOTÓN CONFIGURACIÓN (para todos los usuarios)
        ttk.Button(
            self.sidebar,
            text="⚙ Configuración",
            bootstyle=SECONDARY,
            command=self.show_settings
        ).pack(fill="x", pady=5)

        # SI EL USUARIO ES ADMIN, MOSTRAR "Usuarios"
        if self.role == "admin":
            ttk.Button(
                self.sidebar,
                text="👥 Usuarios",
                bootstyle=INFO,
                command=self.show_users
            ).pack(fill="x", pady=5)

        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", pady=10)

        ttk.Button(
            self.sidebar,
            text="🚪 Cerrar sesión",
            bootstyle=DANGER,
            command=self.logout
        ).pack(fill="x", pady=5)

        # Mostrar vista inicial
        self.current_controller = None
        self.show_dashboard()

    # ==========================
    #   UTILIDAD
    # ==========================
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self.current_controller = None

    # ==========================
    #   VISTAS
    # ==========================
    def show_dashboard(self):
        self.clear_content()
        self.current_controller = DashboardController(self.content, db_path=self.db_path)

    def show_pos(self):
        self.clear_content()
        self.current_controller = POSController(
            self.content,
            db_path=self.db_path,
            cashier_name=self.username,
            cashier_id=self.user_id
        )

    def show_inventory(self):
        self.clear_content()
        self.current_controller = InventoryController(self.content, db_path=self.db_path)

    def show_sales(self):
        self.clear_content()
        self.current_controller = SalesController(self.content, db_path=self.db_path)

    def show_users(self):
        from controllers.users_controller import UsersController
        self.clear_content()
        self.current_controller = UsersController(self.content, db_path=self.db_path)

    def show_settings(self):
        from controllers.settings_controller import SettingsController
        self.clear_content()
        self.current_controller = SettingsController(self.content, db_path=self.db_path)

    # ==========================
    #   CERRAR SESIÓN
    # ==========================
    def logout(self):
        from controllers.login_controller import LoginController
        LoginController(self.root, db_path=self.db_path)
