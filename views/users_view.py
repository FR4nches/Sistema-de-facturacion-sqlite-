import tkinter as tk
from tkinter import ttk as tk_ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class UsersView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        ttk.Label(
            self, text="Gestión de Usuarios",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=10)

        # ============ Tabla ============
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("ID", "Usuario", "Rol", "Creado")
        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            bootstyle=INFO
        )

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center")

        self.table.pack(fill="both", expand=True)

        # ============ Formulario ============

        # Usamos LabelFrame de tkinter.ttk para evitar el error con ttkbootstrap
        form = tk_ttk.LabelFrame(self, text="Crear / Editar Usuario")
        form.pack(fill="x", padx=10, pady=10, ipady=5, ipadx=5)

        # Usuario
        ttk.Label(form, text="Usuario:").grid(row=0, column=0, sticky="w")
        self.entry_username = ttk.Entry(form, width=30)
        self.entry_username.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Contraseña
        ttk.Label(form, text="Contraseña:").grid(row=1, column=0, sticky="w")
        self.entry_password = ttk.Entry(form, width=30, show="*")
        self.entry_password.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Rol
        ttk.Label(form, text="Rol:").grid(row=2, column=0, sticky="w")
        self.combo_role = ttk.Combobox(
            form,
            values=["admin", "cajero"],
            bootstyle=INFO
        )
        self.combo_role.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        form.columnconfigure(1, weight=1)

        # ============ Botones ============
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        self.btn_add = ttk.Button(btn_frame, text="➕ Crear usuario", bootstyle=SUCCESS, width=20)
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_edit = ttk.Button(btn_frame, text="✏ Editar usuario", bootstyle=WARNING, width=20)
        self.btn_edit.grid(row=0, column=1, padx=5)

        self.btn_delete = ttk.Button(btn_frame, text="🗑 Eliminar usuario", bootstyle=DANGER, width=20)
        self.btn_delete.grid(row=0, column=2, padx=5)
