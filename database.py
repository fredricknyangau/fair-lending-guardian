import sqlite3
import os
from datetime import datetime

DB_PATH = "decisions.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS decisions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  applicant_name TEXT,
                  loan_amount REAL,
                  guardian_score REAL,
                  routing_decision TEXT,
                  officer_assigned TEXT,
                  guard_checks TEXT)''')
                  
    c.execute('''CREATE TABLE IF NOT EXISTS sasra_alerts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  alert_message TEXT,
                  status TEXT)''')
    
    # Seed with 5-8 rows if empty
    c.execute("SELECT COUNT(*) FROM decisions")
    if c.fetchone()[0] == 0:
        seed_data = [
            ("2026-06-01 10:00:00", "Grace Achieng", 28000, 88.0, "Escalate", "Sarah", "Passed"),
            ("2026-06-02 11:30:00", "John Kamau", 5000, 92.0, "Approve", "None", "Passed"),
            ("2026-06-03 09:15:00", "Mary Wanjiku", 12000, 45.0, "Decline", "None", "Passed"),
            ("2026-06-04 14:20:00", "Peter Omondi", 40000, 75.0, "Escalate", "James", "Passed"),
            ("2026-06-05 08:45:00", "Lucy Njoroge", 8000, 60.0, "Decline", "None", "Passed"),
            ("2026-06-06 16:10:00", "David Ochieng", 10000, 85.0, "Escalate", "Sarah", "Passed"),
            ("2026-06-07 12:05:00", "Alice Kinyua", 15000, 0, "Kill Switch", "Supervisor", "Failed: Kill Switch")
        ]
        c.executemany("INSERT INTO decisions (timestamp, applicant_name, loan_amount, guardian_score, routing_decision, officer_assigned, guard_checks) VALUES (?, ?, ?, ?, ?, ?, ?)", seed_data)
        conn.commit()
    conn.close()

def log_decision(name, amount, score, decision, officer, guard):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO decisions (timestamp, applicant_name, loan_amount, guardian_score, routing_decision, officer_assigned, guard_checks) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, amount, score, decision, officer, guard))
    conn.commit()
    conn.close()

def log_sasra_alert(message):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO sasra_alerts (timestamp, alert_message, status) VALUES (?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message, "Simulated Email Sent"))
    conn.commit()
    conn.close()

def get_last_10():
    import pandas as pd
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM decisions ORDER BY id DESC LIMIT 10", conn)
    conn.close()
    return df
