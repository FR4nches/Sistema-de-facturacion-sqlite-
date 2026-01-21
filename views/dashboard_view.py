import tkinter as tk
from tkinter import ttk as tk_ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class DashboardView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # ---------- TÍTULO ----------
        title = ttk.Label(
            self, 
            text="Dashboard de Ventas",
            font=("Segoe UI", 20, "bold")
        )
        title.grid(row=0, column=0, pady=20)

        # ---------- CONTENEDOR PRINCIPAL ----------
        main_frame = ttk.Frame(self)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        # 3 columnas para las tarjetas
        main_frame.columnconfigure((0, 1, 2), weight=1)

        # ---------- TARJETAS DE ESTADÍSTICAS ----------
        self.card_sales = ttk.Label(main_frame, text="Ventas Hoy: 0", font=("Segoe UI", 14))
        self.card_sales.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.card_income = ttk.Label(main_frame, text="Ingresos Hoy: ₡0.00", font=("Segoe UI", 14))
        self.card_income.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        self.card_month = ttk.Label(main_frame, text="Ventas del Mes: 0", font=("Segoe UI", 14))
        self.card_month.grid(row=0, column=2, sticky="ew", padx=10, pady=10)

        # ---------- GRÁFICA DE VENTAS ----------
        chart_frame = tk_ttk.LabelFrame(main_frame, text="Ventas últimos 7 días")
        chart_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.chart_canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------- ACTUALIZAR LAS CARTAS ----------
    def update_cards(self, ventas_hoy, ingresos_hoy, ventas_mes):
        self.card_sales.config(text=f"Ventas Hoy: {ventas_hoy}")
        self.card_income.config(text=f"Ingresos Hoy: ₡{ingresos_hoy:.2f}")
        self.card_month.config(text=f"Ventas del Mes: {ventas_mes}")

    # ---------- ACTUALIZAR GRÁFICA ----------
    def update_chart(self, labels, valores):
        self.ax.clear()
        self.ax.plot(labels, valores, marker="o")
        self.ax.set_title("Ventas últimos 7 días")
        self.ax.set_ylabel("Monto (₡)")
        self.ax.grid(True)
        self.chart_canvas.draw()
