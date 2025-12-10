import sqlite3
import os
import csv
import io

class Database:
    def __init__(self, db_name="data/finance.db"):
        self.db_name = db_name
        os.makedirs(os.path.dirname(db_name), exist_ok=True)
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT,
                amount REAL,
                category TEXT,
                description TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.commit()

    def add_transaction(self, user_id, t_type, amount, category, description=""):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO transactions (user_id, type, amount, category, description)
            VALUES (?, ?, ?, ?, ?)
            """, (user_id, t_type, amount, category, description))
            conn.commit()

    def delete_last_transaction(self, user_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM transactions WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))
            row = cursor.fetchone()
            if row:
                cursor.execute("DELETE FROM transactions WHERE id = ?", (row[0],))
                conn.commit()
                return True
            return False

    # --- NUEVO: BORRADO TOTAL ---
    def delete_all_user_data(self, user_id):
        """Borra todo el historial de un usuario"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount

    def get_balance(self, user_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT 
                SUM(CASE WHEN type='income' THEN amount ELSE 0 END) as total_income,
                SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) as total_expense
            FROM transactions WHERE user_id = ?
            """, (user_id,))
            return cursor.fetchone()

    def get_daily_total(self, user_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT SUM(amount) FROM transactions 
            WHERE user_id = ? AND type='expense' 
            AND date(date) = date('now')
            """, (user_id,))
            result = cursor.fetchone()[0]
            return result if result else 0.0

    def get_categories_summary(self, user_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT category, SUM(amount) 
            FROM transactions 
            WHERE user_id = ? AND type='expense'
            GROUP BY category
            ORDER BY SUM(amount) DESC
            """, (user_id,))
            return cursor.fetchall()

    def export_to_csv(self, user_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT date, type, amount, category, description FROM transactions WHERE user_id = ?", (user_id,))
            rows = cursor.fetchall()
            
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['Fecha', 'Tipo', 'Monto', 'Categoría', 'Descripción'])
            writer.writerows(rows)
            output.seek(0)
            return output