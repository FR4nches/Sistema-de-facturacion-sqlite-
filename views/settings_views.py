import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class SettingsView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="Configuración del Sistema", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, columnspan=2, pady=15
        )

        # ===========================
        # CAMPOS DE CONFIGURACIÓN
        # ===========================
        fields = [
            ("Nombre del negocio:", "name"),
            ("Teléfono:", "phone"),
            ("Dirección:", "address"),
            ("Correo:", "email"),
            ("Prefijo de factura:", "prefix"),
            ("Símbolo de moneda:", "currency"),
            ("Impuesto (%):", "tax"),
            ("Mensaje del ticket:", "footer"),
        ]

        self.entries = {}

        row = 1
        for label, key in fields:
            ttk.Label(self, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=5)
            entry = ttk.Entry(self, width=40)
            entry.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
            self.entries[key] = entry
            row += 1

        # ===========================
        # LOGO
        # ===========================
        ttk.Label(self, text="Logo del negocio:").grid(row=row, column=0, sticky="w", padx=10, pady=5)
        self.entry_logo = ttk.Entry(self, width=40)
        self.entry_logo.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        row += 1

        self.btn_choose_logo = ttk.Button(self, text="Seleccionar logo", bootstyle=INFO)
        self.btn_choose_logo.grid(row=row, column=1, sticky="w", padx=10, pady=5)
        row += 1

        # ===========================
        # BOTÓN GUARDAR
        # ===========================
        self.btn_save = ttk.Button(self, text="💾 Guardar cambios", bootstyle=SUCCESS, width=25)
        self.btn_save.grid(row=row, column=0, columnspan=2, pady=15)
