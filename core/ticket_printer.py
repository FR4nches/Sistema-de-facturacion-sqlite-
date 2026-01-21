import os
import sqlite3
from datetime import datetime

from escpos.printer import Usb      # Para USB
from escpos.printer import Serial   # Para Serial COM
from escpos.printer import Network  # Para impresoras LAN


class TicketPrinter:
    def __init__(self, db_path="pos_system.db"):
        self.db_path = db_path

        # Cambiar VID y PID según tu impresora
        # Para Xprinter común:
        #   VID = 0x0416
        #   PID = 0x5011
        #
        # Puedes ver tu VID y PID aquí:
        # Panel de Control > Administrador de Dispositivos > Impresoras > Propiedades > Detalles > Id. de hardware
        #
        self.VID = 0x0416
        self.PID = 0x5011

    # ========================================
    # CONEXIÓN
    # ========================================
    def connect_usb(self):
        try:
            return Usb(self.VID, self.PID, timeout=0, in_ep=0x81, out_ep=0x03)
        except Exception as e:
            raise Exception(f"No se pudo conectar a la impresora USB: {e}")

    # ========================================
    # CARGAR DATOS DE FACTURA
    # ========================================
    def load_sale(self, sale_id):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()

        # Venta
        cur.execute("""
            SELECT invoice_number, date, subtotal, tax, total,
                   COALESCE((SELECT name FROM clients WHERE id=sales.client_id), 'Cliente General')
            FROM sales WHERE id=?
        """, (sale_id,))
        sale = cur.fetchone()

        if not sale:
            con.close()
            raise Exception("Factura no encontrada.")

        invoice_number, date, subtotal, tax, total, client = sale

        # Items
        cur.execute("""
            SELECT si.quantity, p.name, si.price, si.total
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            WHERE si.sale_id = ?
        """, (sale_id,))
        items = cur.fetchall()

        con.close()

        return {
            "invoice": invoice_number,
            "date": date,
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
            "client": client,
            "items": items
        }

    # ========================================
    # IMPRIMIR TICKET ESTÁNDAR 58MM
    # ========================================
    def print_ticket(self, sale_id):
        p = self.connect_usb()
        data = self.load_sale(sale_id)

        p.set(align='center', bold=True, width=2, height=2)
        p.text("TIENDA FRANCHESCO\n")
        p.set(align='center', bold=False, width=1, height=1)
        p.text("Tel: 8888-8888\n")
        p.text("Gracias por su compra!\n")
        p.text("--------------------------\n")

        # Datos de factura
        p.set(align='left')
        p.text(f"Factura: {data['invoice']}\n")
        p.text(f"Fecha: {data['date']}\n")
        p.text(f"Cliente: {data['client']}\n")
        p.text("--------------------------\n")

        # Productos
        for qty, name, price, total in data["items"]:
            p.text(f"{qty} x {name[:20]}\n")
            p.text(f"    ₡{price:.2f}   →   ₡{total:.2f}\n")

        p.text("--------------------------\n")

        # Totales
        p.text(f"SUBTOTAL:   ₡{data['subtotal']:.2f}\n")
        p.text(f"IVA:        ₡{data['tax']:.2f}\n")
        p.set(bold=True)
        p.text(f"TOTAL:      ₡{data['total']:.2f}\n")
        p.set(bold=False)

        p.text("--------------------------\n")
        p.text("¡Vuelva pronto!\n")
        p.text("\n\n")

        p.cut()
