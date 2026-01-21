import os
import sqlite3
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors


def generate_invoice_pdf(db_path: str, sale_id: int, output_dir: str = "invoices") -> str:
    """
    Genera un PDF de la factura indicada por sale_id.
    Devuelve la ruta del archivo PDF generado.
    """

    # ==============================
    #   OBTENER DATOS DE LA BD
    # ==============================
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Encabezado de venta
    cur.execute("""
        SELECT invoice_number, date,
               COALESCE((SELECT name FROM clients WHERE id = sales.client_id), 'Cliente General') AS client_name,
               (SELECT username FROM users WHERE id = sales.cashier_id) AS cashier_name,
               subtotal, tax, total
        FROM sales
        WHERE id = ?
    """, (sale_id,))
    header = cur.fetchone()

    if not header:
        con.close()
        raise ValueError(f"No se encontró la venta con id {sale_id}")

    invoice_number, date_str, client_name, cashier_name, subtotal, tax, total = header

    # Detalle de productos
    cur.execute("""
        SELECT si.quantity, p.name, si.price, si.total
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        WHERE si.sale_id = ?
    """, (sale_id,))
    items = cur.fetchall()

    con.close()

    # ==============================
    #   CONFIGURAR PDF
    # ==============================
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"factura_{invoice_number}.pdf"
    file_path = os.path.join(output_dir, filename)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # Margenes
    margin_left = 20 * mm
    margin_right = width - 20 * mm
    y = height - 30 * mm

    # ==============================
    #   ENCABEZADO COMERCIO
    # ==============================
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin_left, y, "SISTEMA POS FRANCHESCO")
    y -= 8 * mm

    c.setFont("Helvetica", 10)
    c.drawString(margin_left, y, "Dirección: Ejemplo de Calle 123, Costa Rica")
    y -= 5 * mm
    c.drawString(margin_left, y, "Tel: 8888-8888 • Email: ejemplo@correo.com")
    y -= 10 * mm

    # Línea
    c.setStrokeColor(colors.grey)
    c.line(margin_left, y, margin_right, y)
    y -= 10 * mm

    # ==============================
    #   DATOS DE LA FACTURA
    # ==============================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_left, y, f"Factura: {invoice_number}")
    y -= 6 * mm

    c.setFont("Helvetica", 10)
    c.drawString(margin_left, y, f"Fecha: {date_str}")
    y -= 5 * mm
    c.drawString(margin_left, y, f"Cliente: {client_name}")
    y -= 5 * mm
    c.drawString(margin_left, y, f"Cajero: {cashier_name}")
    y -= 10 * mm

    # ==============================
    #   TABLA DE DETALLE
    # ==============================
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin_left, y, "Cant")
    c.drawString(margin_left + 30 * mm, y, "Producto")
    c.drawString(margin_left + 110 * mm, y, "P. Unitario")
    c.drawString(margin_left + 140 * mm, y, "Total")
    y -= 4 * mm

    c.line(margin_left, y, margin_right, y)
    y -= 6 * mm

    c.setFont("Helvetica", 10)

    for qty, name, price, total_item in items:
        if y < 40 * mm:  # Salto de página si se acaba el espacio
            c.showPage()
            y = height - 30 * mm
            c.setFont("Helvetica", 10)

        c.drawString(margin_left, y, str(qty))
        c.drawString(margin_left + 30 * mm, y, name[:40])  # recorte por si es muy largo
        c.drawRightString(margin_left + 135 * mm, y, f"₡ {price:,.2f}")
        c.drawRightString(margin_right, y, f"₡ {total_item:,.2f}")
        y -= 6 * mm

    # ==============================
    #   TOTALES
    # ==============================
    y -= 10 * mm
    c.line(margin_left, y, margin_right, y)
    y -= 6 * mm

    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(margin_right - 40 * mm, y, "Subtotal:")
    c.setFont("Helvetica", 10)
    c.drawRightString(margin_right, y, f"₡ {subtotal:,.2f}")
    y -= 5 * mm

    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(margin_right - 40 * mm, y, "IVA:")
    c.setFont("Helvetica", 10)
    c.drawRightString(margin_right, y, f"₡ {tax:,.2f}")
    y -= 5 * mm

    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(margin_right - 40 * mm, y, "TOTAL:")
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(margin_right, y, f"₡ {total:,.2f}")
    y -= 15 * mm

    # Mensaje final
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(width / 2, y, "¡Gracias por su compra!")

    c.showPage()
    c.save()

    return file_path
