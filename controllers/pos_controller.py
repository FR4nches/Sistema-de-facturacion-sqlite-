import sqlite3
from datetime import datetime
from tkinter import messagebox
from views.pos_view import POSView
from core.config import TAX_RATE


class POSController:
    def __init__(self, parent, db_path="pos_system.db", cashier_name="Admin", cashier_id=1):
        self.parent = parent
        self.db_path = db_path
        self.cashier_name = cashier_name
        self.cashier_id = cashier_id

        self.view = POSView(parent)
        self.items = []  # Carrito

        self.payment_method = "efectivo"

        self.connect_events()
        self.update_totals()

    # ========== DB ==========
    def db(self):
        return sqlite3.connect(self.db_path)

    # ========== EVENTOS ==========
    def connect_events(self):
        self.view.btn_add.config(command=self.add_product)
        self.view.btn_clear.config(command=self.clear_sale)
        self.view.btn_finalize.config(command=self.finalize_sale)

        self.view.entry_search.bind("<Return>", lambda e: self.add_product())
        self.view.entry_payment.bind("<KeyRelease>", lambda e: self.update_change())

        # Métodos de pago
        self.view.btn_cash.config(command=lambda: self.set_payment("efectivo"))
        self.view.btn_card.config(command=lambda: self.set_payment("tarjeta"))
        self.view.btn_sinpe.config(command=lambda: self.set_payment("sinpe"))
        self.view.btn_credit.config(command=lambda: self.set_payment("credito"))

        # Mostrar cajero
        self.view.lbl_cajero.config(text=f"Cajero: {self.cashier_name}")

    # ========== MÉTODO DE PAGO ==========
    def set_payment(self, method):
        self.payment_method = method
        messagebox.showinfo("Método de pago", f"Seleccionaste: {method.capitalize()}")

    # ========== AGREGAR PRODUCTO ==========
    def add_product(self):
        name = self.view.entry_search.get().strip()
        if not name:
            return

        con = self.db()
        cur = con.cursor()
        cur.execute("""
            SELECT id, name, price, stock 
            FROM products
            WHERE name LIKE ?
        """, (f"%{name}%",))
        product = cur.fetchone()
        con.close()

        if not product:
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        prod_id, prod_name, prod_price, prod_stock = product

        if prod_stock <= 0:
            messagebox.showerror("Sin stock", "No hay inventario disponible.")
            return

        # Si ya está en el carrito, aumentar cantidad
        for item in self.items:
            if item["id"] == prod_id:
                item["quantity"] += 1
                item["total"] = item["quantity"] * item["price"]
                break
        else:
            # Nuevo producto al carrito
            self.items.append({
                "id": prod_id,
                "name": prod_name,
                "price": prod_price,
                "quantity": 1,
                "total": prod_price
            })

        self.load_table()
        self.update_totals()
        self.view.entry_search.delete(0, "end")

    # ========== CARGAR TABLA ==========
    def load_table(self):
        self.view.table.delete(*self.view.table.get_children())

        for item in self.items:
            self.view.table.insert(
                "",
                "end",
                values=(item["quantity"], item["name"], f"₡{item['price']:.2f}", f"₡{item['total']:.2f}")
            )

        self.view.lbl_items.config(text=f"Artículos: {len(self.items)}")

    # ========== TOTALES ==========
    def update_totals(self):
        subtotal = sum(item["total"] for item in self.items)
        tax = subtotal * TAX_RATE
        total = subtotal + tax

        self.view.lbl_subtotal.config(text=f"Subtotal: ₡{subtotal:.2f}")
        self.view.lbl_tax.config(text=f"IVA (13%): ₡{tax:.2f}")
        self.view.lbl_total.config(text=f"TOTAL: ₡{total:.2f}")
        self.view.lbl_total_big.config(text=f"₡{total:.2f}")

        self.total = total

    # ========== CAMBIO ==========
    def update_change(self):
        try:
            amount = float(self.view.entry_payment.get())
            change = amount - self.total
            if change < 0:
                change = 0
        except:
            change = 0

        self.view.lbl_change.config(text=f"Cambio: ₡{change:.2f}")

    # ========== LIMPIAR ==========
    def clear_sale(self):
        self.items = []
        self.load_table()
        self.update_totals()
        self.view.entry_payment.delete(0, "end")
        self.view.lbl_change.config(text="Cambio: ₡ 0.00")

    # ========== FINALIZAR VENTA ==========
    def finalize_sale(self):
        if not self.items:
            messagebox.showerror("Error", "No hay productos en la venta.")
            return

        # Validar pago
        try:
            amount_received = float(self.view.entry_payment.get().strip())
        except:
            messagebox.showerror("Error", "Monto recibido inválido.")
            return

        if amount_received < self.total:
            messagebox.showerror("Error", "El pago no cubre el total.")
            return

        # Registrar venta
        con = self.db()
        cur = con.cursor()

        invoice_number = f"F-{int(datetime.now().timestamp())}"

        cur.execute("""
            INSERT INTO sales (invoice_number, client_id, cashier_id, subtotal, tax, total, payment_method, status)
            VALUES (?, NULL, ?, ?, ?, ?, ?, 'pagada')
        """, (
            invoice_number,
            self.cashier_id,
            self.total / (1 + TAX_RATE),
            self.total - (self.total / (1 + TAX_RATE)),
            self.total,
            self.payment_method
        ))

        sale_id = cur.lastrowid

        # Registrar items y descontar stock
        for item in self.items:
            cur.execute("""
                INSERT INTO sale_items (sale_id, product_id, quantity, price, total)
                VALUES (?, ?, ?, ?, ?)
            """, (
                sale_id,
                item["id"],
                item["quantity"],
                item["price"],
                item["total"]
            ))

            cur.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (item["quantity"], item["id"]))

            cur.execute("""
                INSERT INTO stock_movements (product_id, change, reason)
                VALUES (?, ?, 'venta')
            """, (item["id"], -item["quantity"]))

        con.commit()
        con.close()

        messagebox.showinfo("Venta registrada", f"Factura {invoice_number} generada correctamente.")
        self.clear_sale()
