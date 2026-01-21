import sqlite3
from tkinter import filedialog, messagebox
from views.settings_views import SettingsView


class SettingsController:
    def __init__(self, parent, db_path="pos_system.db"):
        self.parent = parent
        self.db_path = db_path

        self.view = SettingsView(parent)

        self.load_settings()
        self.connect_events()

    # DB connection
    def db(self):
        return sqlite3.connect(self.db_path)

    # Cargar valores desde la BD
    def load_settings(self):
        con = self.db()
        cur = con.cursor()
        cur.execute("SELECT * FROM settings WHERE id = 1")
        row = cur.fetchone()
        con.close()

        if not row:
            return

        (_, business_name, phone, address, email, prefix, currency, tax_rate, footer, logo) = row

        self.view.entries["name"].insert(0, business_name)
        self.view.entries["phone"].insert(0, phone)
        self.view.entries["address"].insert(0, address)
        self.view.entries["email"].insert(0, email)
        self.view.entries["prefix"].insert(0, prefix)
        self.view.entries["currency"].insert(0, currency)
        self.view.entries["tax"].insert(0, str(tax_rate * 100))  # Mostrar en %
        self.view.entries["footer"].insert(0, footer)

        if logo:
            self.view.entry_logo.insert(0, logo)

    def connect_events(self):
        self.view.btn_save.config(command=self.save_settings)
        self.view.btn_choose_logo.config(command=self.choose_logo)

    # Seleccionar imagen de logo
    def choose_logo(self):
        path = filedialog.askopenfilename(
            title="Seleccionar logo",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")]
        )
        if path:
            self.view.entry_logo.delete(0, "end")
            self.view.entry_logo.insert(0, path)

    # Guardar en BD
    def save_settings(self):
        try:
            name = self.view.entries["name"].get().strip()
            phone = self.view.entries["phone"].get().strip()
            address = self.view.entries["address"].get().strip()
            email = self.view.entries["email"].get().strip()
            prefix = self.view.entries["prefix"].get().strip()
            currency = self.view.entries["currency"].get().strip()
            tax_percent = float(self.view.entries["tax"].get().strip()) / 100
            footer = self.view.entries["footer"].get().strip()
            logo = self.view.entry_logo.get().strip()

        except:
            messagebox.showerror("Error", "Hay valores inválidos.")
            return

        con = self.db()
        cur = con.cursor()

        cur.execute("""
            UPDATE settings SET
                business_name = ?,
                business_phone = ?,
                business_address = ?,
                business_email = ?,
                invoice_prefix = ?,
                currency_symbol = ?,
                tax_rate = ?,
                footer_message = ?,
                logo_path = ?
            WHERE id = 1
        """, (name, phone, address, email, prefix, currency, tax_percent, footer, logo))

        con.commit()
        con.close()

        messagebox.showinfo("Guardado", "Configuración actualizada correctamente.")
