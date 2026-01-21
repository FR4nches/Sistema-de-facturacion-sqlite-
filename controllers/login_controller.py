import sqlite3
from views.login_view import LoginView
from controllers.app_controller import AppController
import os




class LoginController:
    def __init__(self, app, db_path="pos_system.db"):
        self.app = app
        self.db_path = db_path
        self.view = None
        self.show_login()

    def show_login(self):
        self.clear_root()
        self.view = LoginView(self.app, login_callback=self.process_login)

    def clear_root(self):
        for widget in self.app.winfo_children():
            widget.destroy()

    def process_login(self, username, password):
        print("\n==============================")
        print("RUTA REAL DE LA BASE DE DATOS:")
        print(os.path.abspath(self.db_path))
        print("==============================\n")
        
        if not username or not password:
            self.view.lbl_message.config(text="Debe llenar todos los campos.")
            return

        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(
            "SELECT id, username, password, role FROM users WHERE username = ?",
            (username,)
        )
        

        row = cur.fetchone()
        con.close()

        if not row or row[2] != password:
            self.view.lbl_message.config(text="Usuario o contraseña incorrectos.")
            return

        user_id = row[0]
        username = row[1]
        # Aquí podrías usar el rol si quieres permisos
        role = row[3]

        # Ir al menú principal
        AppController(
            self.app,
            user_id=user_id,
            username=username,
            role=role,
            db_path=self.db_path
        )

