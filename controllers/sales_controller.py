import sqlite3
from tkinter import messagebox, filedialog
from views.sales_view import SalesView
from datetime import datetime

# PDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class SalesController:
    def __init__(self, parent, db_path="pos_system.db"):
        self.parent = parent
        self.db_path = db_path

        self.view = SalesView(parent)

        self.connect_events()
        self.load_sales()

    # -------------------------
    # DB
    # -------------------------
    def db(self):
        return sqlite3.connect(self.db_path)

    # -------------------------
    # Eventos
    # -------------------------
    def connect_events(self):
        self.view.btn_search.config(command=self.search_invoice)
        self.view.btn_show_all.config(command=self.load_sales)
        self.view.btn_details.config(command=self.show_details)
        self.view.btn_pdf.config(command=self.export_pdf)
        self.view.btn_cancel.config(command=self.cancel_sale)

    # -------------------------
    # Cargar ventas
    # -------------------------
    def load_sales(self):
        con = self.db()
        cur = con.cursor()

        cur.execute("""
            SELECT id, invoice_number, date, total, status
            FROM sales
            ORDER BY id DESC
        """)

        rows = cur.fetchall()
        con.close()

        self.view.table.delete(*self.view.table.get_children())

        for row in rows:
            self.view.table.insert("", "end", values=row)

    # -------------------------
    # Buscar factura
    # -------------------------
    def search_invoice(self):
        search_text = self.view.entry_search.get().strip()

        if not search_text:
            return self.load_sales()

        con = self.db()
        cur = con.cursor()

        cur.execute("""
            SELECT id, invoice_number, date, total, status
            FROM sales
            WHERE invoice_number LIKE ?
            ORDER BY id DESC
        """, (f"%{search_text}%",))

        rows = cur.fetchall()
        con.close()

        self.view.table.delete(*self.view.table.get_children())

        for row in rows:
            self.view.table.insert("", "end", values=row)

    # -------------------------
    # Ver detalle de factura
    # -------------------------
    def show_details(self):
        selected = self.view.table.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Seleccione una factura.")
            return

        sale_id = self.view.table.item(selected[0])["values"][0]

        con = self.db()
        cur = con.cursor()

        cur.execute("""
            SELECT p.name, si.quantity, si.price, si.total
            FROM sale_items si
            JOIN products p ON p.id = si.product_id
            WHERE si.sale_id = ?
        """, (sale_id,))
        items = cur.fetchall()

        con.close()

        text = "\n".join([f"{name} x{qty} — ₡{total}" for (name, qty, price, total) in items])

        messagebox.showinfo("Detalle de Venta", text if text else "Factura vacía.")

    # -------------------------
    # Exportar factura a PDF
    # -------------------------
    def export_pdf(self):
        selected = self.view.table.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Seleccione una factura.")
            return

        sale_id = self.view.table.item(selected[0])["values"][0]

        con = self.db()
        cur = con.cursor()

        # Datos generales
        cur.execute("""
            SELECT invoice_number, date, subtotal, tax, total, payment_method
            FROM sales
            WHERE id = ?
        """, (sale_id,))
        sale = cur.fetchone()

        # Items de la venta
        cur.execute("""
            SELECT p.name, si.quantity, si.price, si.total
            FROM sale_items si
            JOIN products p ON p.id = si.product_id
            WHERE si.sale_id = ?
        """, (sale_id,))
        items = cur.fetchall()

        con.close()

        # Seleccionar dónde guardar PDF
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"{sale[0]}.pdf"
        )

        if not filename:
            return

        # Crear PDF
        c = canvas.Canvas(filename, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "Factura Electrónica")
        c.setFont("Helvetica", 12)

        # Encabezado
        y = 720
        c.drawString(50, y, f"Número: {sale[0]}")
        y -= 20
        c.drawString(50, y, f"Fecha: {sale[1]}")
        y -= 20
        c.drawString(50, y, f"Método de pago: {sale[5]}")
        y -= 40

        # Tabla de productos
        c.drawString(50, y, "Producto")
        c.drawString(250, y, "Cant.")
        c.drawString(300, y, "Precio")
        c.drawString(380, y, "Total")
        y -= 20

        for (name, qty, price, total) in items:
            c.drawString(50, y, str(name))
            c.drawString(250, y, str(qty))
            c.drawString(300, y, f"₡{price:.2f}")
            c.drawString(380, y, f"₡{total:.2f}")
            y -= 20

            if y < 80:  # Salto de página
                c.showPage()
                y = 750

        # Totales
        y -= 20
        c.drawString(50, y, f"Subtotal: ₡{sale[2]:.2f}")
        y -= 20
        c.drawString(50, y, f"IVA: ₡{sale[3]:.2f}")
        y -= 20
        c.drawString(50, y, f"TOTAL: ₡{sale[4]:.2f}")

        # Guardar PDF
        c.save()

        messagebox.showinfo("PDF generado", f"Factura exportada como:\n{filename}")

    # -------------------------
    # Anular venta
    # -------------------------
    def cancel_sale(self):
        selected = self.view.table.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Seleccione una factura.")
            return

        sale_id = self.view.table.item(selected[0])["values"][0]

        if not messagebox.askyesno("Confirmar", "¿Seguro que desea ANULAR esta venta?"):
            return

        con = self.db()
        cur = con.cursor()

        cur.execute("""
            UPDATE sales
            SET status = 'anulada'
            WHERE id = ?
        """, (sale_id,))

        con.commit()
        con.close()

        messagebox.showinfo("Anulada", "La venta fue anulada correctamente.")
        self.load_sales()
