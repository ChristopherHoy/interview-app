import sqlite3

from fastapi import FastAPI
import uvicorn
from routes import router


app = FastAPI()
app.include_router(router)


def init_db():
    conn = sqlite3.connect('payments.db')
    tables = [
        """
            CREATE TABLE IF NOT EXISTS payment_status_tracking (
                id STRING PRIMARY KEY,
                reference TEXT NOT NULL,
                status_name TEXT NOT NULL,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """,
        """
            CREATE TABLE IF NOT EXISTS payment_audit_log (
                id INTEGER PRIMARY KEY,
                reference TEXT NOT NULL,
                amount INTEGER NOT NULL,
                currency INTEGER DEFAULT 'ZAR',
                payment_method TEXT DEFAULT 'CREDIT_CARD',
                product_code INTEGER,
                gateway_name TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """    
    ]

    cursor = conn.cursor()
    for sql in tables:
        cursor.execute(sql)
        
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)