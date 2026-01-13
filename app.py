from database import init_db
from gui import start_app

def main():
    init_db()
    start_app()  # يبدأ التطبيق بالواجهة الرسومية

if __name__ == "__main__":
    main()
