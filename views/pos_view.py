import tkinter as tk
from tkinter import ttk as tk_ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class POSView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        # =======================
        #   COLUMNAS PRINCIPALES
        # =======================
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # =======================
        #   COLUMNA IZQUIERDA
        # =======================
        left_frame = ttk.Frame(self, padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew")

        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)

        # -------- BUSCADOR --------
        search_frame = ttk.Frame(left_frame)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(search_frame, text="Buscar producto:").pack(anchor="w")

        self.entry_search = ttk.Entry(search_frame)
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_add = ttk.Button(search_frame, text="+ Agregar")
        self.btn_add.pack(side="left", padx=5)

        self.btn_clear = ttk.Button(search_frame, text="🗑 Borrar")
        self.btn_clear.pack(side="left")

        # -------- TABLA DE PRODUCTOS --------
        table_frame = ttk.Frame(left_frame)
        table_frame.grid(row=1, column=0, sticky="nsew")

        columns = ("Cantidad", "Producto", "Precio", "Total")
        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15,
            bootstyle=INFO
        )

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center")

        self.table.pack(fill="both", expand=True)

        # -------- RESUMEN DE TOTALES --------
        totals_frame = ttk.Frame(left_frame, padding=10)
        totals_frame.grid(row=2, column=0, sticky="ew", pady=10)

        self.lbl_subtotal = ttk.Label(totals_frame, text="Subtotal: ₡ 0.00", font=("Segoe UI", 11))
        self.lbl_subtotal.pack(anchor="e")

        self.lbl_tax = ttk.Label(totals_frame, text="IVA (13%): ₡ 0.00", font=("Segoe UI", 11))
        self.lbl_tax.pack(anchor="e")

        ttk.Separator(totals_frame, orient="horizontal").pack(fill="x", pady=5)

        self.lbl_total = ttk.Label(totals_frame, text="TOTAL: ₡ 0.00", font=("Segoe UI", 16, "bold"))
        self.lbl_total.pack(anchor="e")

        # =======================
        #   COLUMNA DERECHA
        # =======================
        right_frame = ttk.Frame(self, padding=15)
        right_frame.grid(row=0, column=1, sticky="nsew")

        right_frame.columnconfigure(0, weight=1)

        # -------- RESUMEN RÁPIDO --------
        ttk.Label(right_frame, text="TOTAL A PAGAR", font=("Segoe UI", 14, "bold")).pack()
        self.lbl_total_big = ttk.Label(right_frame, text="₡ 0.00", font=("Segoe UI", 26, "bold"))
        self.lbl_total_big.pack(pady=10)

        self.lbl_items = ttk.Label(right_frame, text="Artículos: 0", font=("Segoe UI", 11))
        self.lbl_items.pack()

        self.lbl_cajero = ttk.Label(right_frame, text="Cajero: ---", font=("Segoe UI", 11))
        self.lbl_cajero.pack(pady=(0, 20))

        # -------- BOTONES DE PAGO --------
        self.payment_method = "efectivo"

        self.btn_cash = ttk.Button(right_frame, text="💵 Efectivo", bootstyle=SUCCESS)
        self.btn_cash.pack(fill="x", pady=5)

        self.btn_card = ttk.Button(right_frame, text="💳 Tarjeta", bootstyle=PRIMARY)
        self.btn_card.pack(fill="x", pady=5)

        self.btn_sinpe = ttk.Button(right_frame, text="📱 SINPE", bootstyle=INFO)
        self.btn_sinpe.pack(fill="x", pady=5)

        self.btn_credit = ttk.Button(right_frame, text="📝 Crédito", bootstyle=WARNING)
        self.btn_credit.pack(fill="x", pady=5)

        # -------- PAGO --------
        ttk.Label(right_frame, text="Monto recibido:", font=("Segoe UI", 11)).pack(anchor="w", pady=(20, 5))
        self.entry_payment = ttk.Entry(right_frame)
        self.entry_payment.pack(fill="x")

        self.lbl_change = ttk.Label(right_frame, text="Cambio: ₡ 0.00", font=("Segoe UI", 11))
        self.lbl_change.pack(anchor="e", pady=10)

        self.btn_finalize = ttk.Button(
            right_frame,
            text="✔ Finalizar venta",
            bootstyle=SUCCESS
        )
        self.btn_finalize.pack(fill="x", pady=10)
