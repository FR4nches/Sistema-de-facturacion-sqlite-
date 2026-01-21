import tkinter as tk
from tkinter import ttk as tk_ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class SalesView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # --- Título ---
        title = ttk.Label(
            self, text="Historial de Ventas",
            font=("Segoe UI", 18, "bold")
        )
        title.grid(row=0, column=0, pady=10)

        # --- Buscador ---
        search_frame = ttk.Frame(self)
        search_frame.grid(row=1, column=0, sticky="ew", padx=10)

        ttk.Label(search_frame, text="Buscar factura:").grid(row=0, column=0)
        self.entry_search = ttk.Entry(search_frame, width=40)
        self.entry_search.grid(row=0, column=1, padx=5)

        self.btn_search = ttk.Button(search_frame, text="Buscar", bootstyle=PRIMARY)
        self.btn_search.grid(row=0, column=2, padx=5)

        self.btn_show_all = ttk.Button(search_frame, text="Mostrar todo", bootstyle=SECONDARY)
        self.btn_show_all.grid(row=0, column=3, padx=5)

        # --- Tabla ---
        table_frame = ttk.Frame(self)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = ("ID", "Factura", "Fecha", "Total", "Estado")
        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            bootstyle=INFO
        )

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center")

        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scroll_y.set)

        self.table.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")

        # --- Botones de acción ---
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=3, column=0, pady=10)

        self.btn_details = ttk.Button(btn_frame, text="Ver Detalle", bootstyle=INFO)
        self.btn_details.grid(row=0, column=0, padx=5)

        self.btn_pdf = ttk.Button(btn_frame, text="Exportar PDF", bootstyle=SUCCESS)
        self.btn_pdf.grid(row=0, column=1, padx=5)

        self.btn_cancel = ttk.Button(btn_frame, text="Anular Venta", bootstyle=DANGER)
        self.btn_cancel.grid(row=0, column=2, padx=5)
