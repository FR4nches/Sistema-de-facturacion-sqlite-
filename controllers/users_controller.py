import sqlite3
from tkinter import messagebox
from views.users_view import UsersView
from core.security import hash_password


class UsersController:
    def __init__(self, parent, db_path="pos_system.db"):
        self.parent = parent
        self.db_path = db_path

        self.view = UsersView(parent)
        self.selected_user_id = None

        self.load_users()
        self.connect_events()

    # DB
    def db(self):
        return sqlite3.connect(self.db_path)

    # Eventos
    def connect_events(self):
        self.view.btn_add.config(command=self.add_user)
        self.view.btn_edit.config(command=self.edit_user)
        self.view.btn_delete.config(command=self.delete_user)

        self.view.table.bind("<<TreeviewSelect>>", self.on_row_selected)

    # =========================
    #   Cargar usuarios
    # =========================
    def load_users(self):
        con = self.db()
        cur = con.cursor()

        cur.execute("SELECT id, username, role, created_at FROM users")
        rows = cur.fetchall()

        con.close()

        self.view.table.delete(*self.view.table.get_children())
        for row in rows:
            self.view.table.insert("", "end", values=row)

    # =========================
    #   Seleccionar usuario
    # =========================
    def on_row_selected(self, event):
        selected = self.view.table.selection()
        if not selected:
            self.selected_user_id = None
            return

        values = self.view.table.item(selected[0])["values"]
        self.selected_user_id = values[0]

        # Cargar en formulario para edición
        self.view.entry_username.delete(0, "end")
        self.view.entry_username.insert(0, values[1])

        self.view.combo_role.set(values[2])

        # No mostramos contraseña por seguridad

    # =========================
    #   Crear usuario
    # =========================
    def add_user(self):
        username = self.view.entry_username.get().strip()
        password = self.view.entry_password.get().strip()
        role = self.view.combo_role.get().strip()

        if not username or not password or not role:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        hashed_pw = hash_password(password)

        con = self.db()
        cur = con.cursor()

        try:
            cur.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, hashed_pw, role)
            )
            con.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El usuario ya existe.")
            con.close()
            return

        con.close()
        messagebox.showinfo("Éxito", "Usuario creado correctamente.")
        self.clear_form()
        self.load_users()

    # =========================
    #   Editar usuario
    # =========================
    def edit_user(self):
        if not self.selected_user_id:
            messagebox.showwarning("Aviso", "Seleccione un usuario para editar.")
            return

        username = self.view.entry_username.get().strip()
        password = self.view.entry_password.get().strip()
        role = self.view.combo_role.get().strip()

        if not username or not role:
            messagebox.showerror("Error", "Usuario y rol son obligatorios.")
            return

        con = self.db()
        cur = con.cursor()

        # Si se dio nueva contraseña
        if password:
            hashed_pw = hash_password(password)
            cur.execute("""
                UPDATE users SET username=?, password=?, role=?
                WHERE id=?
            """, (username, hashed_pw, role, self.selected_user_id))
        else:
            cur.execute("""
                UPDATE users SET username=?, role=?
                WHERE id=?
            """, (username, role, self.selected_user_id))

        con.commit()
        con.close()

        messagebox.showinfo("Actualizado", "Usuario modificado correctamente.")
        self.clear_form()
        self.load_users()

    # =========================
    #   Eliminar usuario
    # =========================
    def delete_user(self):
        if not self.selected_user_id:
            messagebox.showwarning("Aviso", "Seleccione un usuario para eliminar.")
            return

        if self.selected_user_id == 1:
            messagebox.showerror("Error", "No podés eliminar al administrador principal.")
            return

        con = self.db()
        cur = con.cursor()

        cur.execute("DELETE FROM users WHERE id=?", (self.selected_user_id,))

        con.commit()
        con.close()

        messagebox.showinfo("Eliminado", "Usuario eliminado correctamente.")
        self.clear_form()
        self.load_users()

    # =========================
    #   Limpiar form
    # =========================
    def clear_form(self):
        self.view.entry_username.delete(0, "end")
        self.view.entry_password.delete(0, "end")
        self.view.combo_role.set("")
        self.selected_user_id = None
