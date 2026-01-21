import tkinter as tk
from tkinter import ttk as tk_ttk   # Para usar LabelFrame que SÍ funciona
from ttkbootstrap import Style
import ttkbootstrap as ttk          # Para usar Entry, Button, Treeview con estilo
from ttkbootstrap.constants import *




class InventoryView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        # ============================
        #   CONFIGURACIÓN GENERAL
        # ============================
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # ============================
        #   TÍTULO
        # ============================
        title = ttk.Label(
            self, text="Gestión de Inventario",
            font=("Segoe UI", 18, "bold")
        )
        title.grid(row=0, column=0, pady=10)

        # ============================
        #   BUSCADOR
        # ============================
        search_frame = ttk.Frame(self, padding=10)
        search_frame.grid(row=1, column=0, sticky="ew")

        search_frame.columnconfigure(0, weight=1)

        self.entry_search = ttk.Entry(
            search_frame, width=50, bootstyle=INFO
        )
        self.entry_search.grid(row=0, column=0, sticky="ew", padx=5)

        # 🔎 Buscar
        self.btn_search = ttk.Button(
            search_frame, text="🔍 Buscar", bootstyle=PRIMARY
        )
        self.btn_search.grid(row=0, column=1, padx=5)

        # Mostrar todo
        self.btn_show_all = ttk.Button(
            search_frame, text="Mostrar todo", bootstyle=SECONDARY
        )
        self.btn_show_all.grid(row=0, column=2, padx=5)

        # ============================
        #   TABLA DE PRODUCTOS
        # ============================
        table_frame = ttk.Frame(self, padding=10)
        table_frame.grid(row=2, column=0, sticky="nsew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        columns = ("ID", "Producto", "Categoría", "Precio", "Stock")

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            bootstyle=INFO
        )

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center")

        # Scrollbar vertical
        scroll_y = ttk.Scrollbar(
            table_frame, orient="vertical",
            command=self.table.yview
        )
        self.table.configure(yscrollcommand=scroll_y.set)

        self.table.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")

        # ============================
        #   BOTONES CRUD
        # ============================
        crud_frame = ttk.Frame(self, padding=10)
        crud_frame.grid(row=3, column=0, pady=5)

        # ➕ Agregar
        self.btn_add = ttk.Button(
            crud_frame, text="➕ Agregar producto",
            bootstyle=SUCCESS, width=20
        )
        self.btn_add.grid(row=0, column=0, padx=5)

        # ✏ Editar
        self.btn_edit = ttk.Button(
            crud_frame, text="✏ Editar producto",
            bootstyle=WARNING, width=20
        )
        self.btn_edit.grid(row=0, column=1, padx=5)

        # 🗑 Eliminar
        self.btn_delete = ttk.Button(
            crud_frame, text="🗑 Eliminar producto",
            bootstyle=DANGER, width=20
        )
        self.btn_delete.grid(row=0, column=2, padx=5)

        # ============================
        #   FORMULARIO PARA AGREGAR/EDITAR
        # ============================
        form_frame = tk_ttk.LabelFrame(self, text="Registrar / Editar Producto")

        form_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=10)

        form_frame.columnconfigure(1, weight=1)

        # NOMBRE
        ttk.Label(form_frame, text="Nombre:", font=("Segoe UI", 11)).grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.entry_name = ttk.Entry(form_frame, bootstyle=INFO)
        self.entry_name.grid(row=0, column=1, sticky="ew")

        # CATEGORÍA
        ttk.Label(form_frame, text="Categoría:", font=("Segoe UI", 11)).grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.entry_category = ttk.Entry(form_frame, bootstyle=INFO)
        self.entry_category.grid(row=1, column=1, sticky="ew")

        # PRECIO
        ttk.Label(form_frame, text="Precio:", font=("Segoe UI", 11)).grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.entry_price = ttk.Entry(form_frame, bootstyle=INFO)
        self.entry_price.grid(row=2, column=1, sticky="ew")

        # STOCK
        ttk.Label(form_frame, text="Stock:", font=("Segoe UI", 11)).grid(
            row=3, column=0, sticky="w", pady=5
        )
        self.entry_stock = ttk.Entry(form_frame, bootstyle=INFO)
        self.entry_stock.grid(row=3, column=1, sticky="ew")

        # BOTÓN GUARDAR
        self.btn_save = ttk.Button(
            form_frame, text="💾 Guardar",
            bootstyle=SUCCESS, width=18
        )
        self.btn_save.grid(row=4, column=1, pady=10, sticky="e")
