import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk


class LoginView(ttk.Frame):
    def __init__(self, master, login_callback=None):
        super().__init__(master)
        self.login_callback = login_callback
        self.pack(fill="both", expand=True)

        # ========== CONFIGURACIÓN DE COLUMNAS ==========
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # ========== MARCO CENTRAL ==========
        main_frame = ttk.Frame(self, padding=40)
        main_frame.grid(row=0, column=0, sticky="nsew")

        main_frame.columnconfigure(0, weight=1)

        # ======== TÍTULO ========
        ttk.Label(
            main_frame,
            text="Iniciar Sesión",
            font=("Segoe UI", 20, "bold")
        ).grid(row=0, column=0, pady=(0, 20))

        # ======== USUARIO ========
        ttk.Label(main_frame, text="Usuario:", font=("Segoe UI", 11)).grid(
            row=1, column=0, sticky="w"
        )

        self.entry_user = ttk.Entry(main_frame, bootstyle=INFO)
        self.entry_user.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        # ======== CONTRASEÑA ========
        ttk.Label(main_frame, text="Contraseña:", font=("Segoe UI", 11)).grid(
            row=3, column=0, sticky="w"
        )

        self.entry_pass = ttk.Entry(main_frame, show="*", bootstyle=INFO)
        self.entry_pass.grid(row=4, column=0, sticky="ew", pady=(0, 20))

        # ======== BOTÓN DE LOGIN ========
        self.btn_login = ttk.Button(
            main_frame,
            text="Ingresar",
            bootstyle=PRIMARY,
            command=self.try_login
        )
        self.btn_login.grid(row=5, column=0, sticky="ew", pady=(5, 10))

        # ======== MENSAJE ========
        self.lbl_message = ttk.Label(
            main_frame,
            text="",
            font=("Segoe UI", 10),
            foreground="#D9534F"  # rojo suave para errores
        )
        self.lbl_message.grid(row=6, column=0, pady=5)

    # ============================================
    # FUNCIÓN PARA INTENTAR LOGIN
    # ============================================
    def try_login(self):
        user = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if not user or not password:
            self.lbl_message.config(text="Debe llenar todos los campos.")
            return

        # Llamamos la función (callback) del controlador
        if self.login_callback:
            self.login_callback(user, password)
