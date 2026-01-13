import sqlite3
from datetime import datetime
import hashlib
from database import init_db, admin_exists, create_admin, verify_user
from ui import start_ui

def main():
    init_db()
    start_ui()

if __name__ == "__main__":
    main()
