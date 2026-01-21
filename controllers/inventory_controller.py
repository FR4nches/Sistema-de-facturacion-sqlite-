import sqlite3
from tkinter import messagebox
from views.inventory_view import InventoryView


class InventoryController:
    def __init__(self, parent, db_path="pos_system.db"):
        self.parent = parent
        self.db_path = db_path

        self.view = InventoryView(parent)

        # id del producto que se está editando (None = modo crear)
        self.current_product_id = None

        self.connect_events()
        self.load_products()

    # ===========================
    #   DB
    # ===========================
    def db(self):
        return sqlite3.connect(self.db_path)

    # ===========================
    #   EVENTOS
    # ===========================
    def connect_events(self):
        self.view.btn_add.config(command=self.new_product_mode)
        self.view.btn_edit.config(command=self.edit_product_mode)
        self.view.btn_delete.config(command=self.delete_product)
        self.view.btn_save.config(command=self.save_product)

        self.view.table.bind("<<TreeviewSelect>>", self.on_row_select)

    # ===========================
    #   CARGAR PRODUCTOS
    # ===========================
    def load_products(self):
        con = self.db()
        cur = con.cursor()

        # Intentamos con esquema con categorías (category_id) + tabla categories
        try:
            cur.execute("""
                SELECT p.id,
                       p.name,
                       COALESCE(c.name, ''),
                       p.price,
                       p.stock
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                ORDER BY p.id DESC
            """)
        except sqlite3.OperationalError:
            # Plan B: esquema simple con columna category TEXT
            cur.execute("""
                SELECT id, name, category, price, stock
                FROM products
                ORDER BY id DESC
            """)

        rows = cur.fetchall()
        con.close()

        # Limpiar tabla
        self.view.table.delete(*self.view.table.get_children())

        # Llenar tabla
        for row in rows:
            self.view.table.insert("", "end", values=row)

    # ===========================
    #   LIMPIAR FORMULARIO
    # ===========================
    def clear_form(self):
        self.current_product_id = None
        self.view.entry_name.delete(0, "end")
        self.view.entry_category.delete(0, "end")
        self.view.entry_price.delete(0, "end")
        self.view.entry_stock.delete(0, "end")

    # ===========================
    #   MODO NUEVO
    # ===========================
    def new_product_mode(self):
        self.clear_form()
        self.view.entry_name.focus()

    # ===========================
    #   SELECCIONAR FILA
    # ===========================
    def on_row_select(self, event=None):
        selected = self.view.table.selection()
        if not selected:
            return

        values = self.view.table.item(selected[0])["values"]
        # Esperamos: (id, nombre, categoría, precio, stock)
        self.current_product_id = values[0]

        # Cargar datos en el formulario
        self.view.entry_name.delete(0, "end")
        self.view.entry_name.insert(0, values[1])

        self.view.entry_category.delete(0, "end")
        self.view.entry_category.insert(0, values[2])

        self.view.entry_price.delete(0, "end")
        self.view.entry_price.insert(0, str(values[3]))

        if len(values) >= 5:
            self.view.entry_stock.delete(0, "end")
            self.view.entry_stock.insert(0, str(values[4]))

    # ===========================
    #   MODO EDITAR
    # ===========================
    def edit_product_mode(self):
        selected = self.view.table.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Seleccione un producto para editar.")
            return

        # on_row_select ya carga los datos
        self.on_row_select()

    # ===========================
    #   GUARDAR (INSERT / UPDATE)
    # ===========================
    def save_product(self):
        name = self.view.entry_name.get().strip()
        category = self.view.entry_category.get().strip()
        price_str = self.view.entry_price.get().strip()
        stock_str = self.view.entry_stock.get().strip()

        if not name or not price_str:
            messagebox.showerror("Error", "Nombre y precio son obligatorios.")
            return

        try:
            price = float(price_str)
        except ValueError:
            messagebox.showerror("Error", "Precio inválido.")
            return

        try:
            stock = int(stock_str) if stock_str else 0
        except ValueError:
            messagebox.showerror("Error", "Stock inválido.")
            return

        con = self.db()
        cur = con.cursor()

        # Intento de esquema con categories + category_id
        try:
            category_id = None
            if category:
                # Asegurar categoría
                cur.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category,))
                cur.execute("SELECT id FROM categories WHERE name = ?", (category,))
                cat_row = cur.fetchone()
                category_id = cat_row[0] if cat_row else None

            if self.current_product_id is None:
                # INSERT
                cur.execute("""
                    INSERT INTO products (name, category_id, price, stock)
                    VALUES (?, ?, ?, ?)
                """, (name, category_id, price, stock))
            else:
                # UPDATE
                cur.execute("""
                    UPDATE products
                    SET name = ?, category_id = ?, price = ?, stock = ?
                    WHERE id = ?
                """, (name, category_id, price, stock, self.current_product_id))

        except sqlite3.OperationalError:
            # Plan B: tabla products con columna category TEXT
            if self.current_product_id is None:
                cur.execute("""
                    INSERT INTO products (name, category, price, stock)
                    VALUES (?, ?, ?, ?)
                """, (name, category, price, stock))
            else:
                cur.execute("""
                    UPDATE products
                    SET name = ?, category = ?, price = ?, stock = ?
                    WHERE id = ?
                """, (name, category, price, stock, self.current_product_id))

        con.commit()
        con.close()

        messagebox.showinfo("Éxito", "Producto guardado correctamente.")
        self.clear_form()
        self.load_products()

    # ===========================
    #   ELIMINAR PRODUCTO
    # ===========================
    def delete_product(self):
        selected = self.view.table.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Seleccione un producto para eliminar.")
            return

        values = self.view.table.item(selected[0])["values"]
        prod_id = values[0]

        if not messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este producto?"):
            return

        con = self.db()
        cur = con.cursor()

        cur.execute("DELETE FROM products WHERE id = ?", (prod_id,))

        con.commit()
        con.close()

        messagebox.showinfo("Eliminado", "Producto eliminado correctamente.")
        self.clear_form()
        self.load_products()
