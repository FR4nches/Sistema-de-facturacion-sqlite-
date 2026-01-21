import sqlite3
from datetime import datetime, timedelta
from views.dashboard_view import DashboardView


class DashboardController:
    def __init__(self, parent, db_path="pos_system.db"):
        self.parent = parent
        self.db_path = db_path
        self.view = DashboardView(parent)

        self.load_data()

    # ------------------------------
    #   CONEXIÓN DB
    # ------------------------------
    def db(self):
        return sqlite3.connect(self.db_path)

    # ------------------------------
    #   CARGAR DATOS AL DASHBOARD
    # ------------------------------
    def load_data(self):
        con = self.db()
        cur = con.cursor()

        # ------------------ VENTAS HOY ------------------
        cur.execute("""
            SELECT COUNT(*), COALESCE(SUM(total), 0)
            FROM sales
            WHERE DATE(date) = DATE('now')
        """)
        ventas_hoy, ingresos_hoy = cur.fetchone()

        # ------------------ VENTAS DEL MES ------------------
        cur.execute("""
            SELECT COUNT(*)
            FROM sales
            WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        """)
        ventas_mes = cur.fetchone()[0]

        # ------------------ ÚLTIMOS 7 DÍAS ------------------
        labels = []
        valores = []

        for i in range(6, -1, -1):
            dia = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            labels.append(dia[5:])  # Muestra solo "MM-DD"

            cur.execute("""
                SELECT COALESCE(SUM(total), 0)
                FROM sales
                WHERE DATE(date) = DATE(?)
            """, (dia,))
            valores.append(cur.fetchone()[0])

        con.close()

        # Actualizar tarjetas
        self.view.update_cards(
            ventas_hoy,
            ingresos_hoy,
            ventas_mes
        )

        # Actualizar gráfica
        self.view.update_chart(labels, valores)
