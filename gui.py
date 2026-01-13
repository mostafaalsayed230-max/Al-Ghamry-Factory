import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from database import admin_exists, create_admin, verify_user

class AlGhamryApp(toga.App):

    def startup(self):
        # النافذة الرئيسية
        self.main_window = toga.MainWindow(title="🏭 Al-Ghamry Factory")

        if not admin_exists():
            self.show_create_admin()
        else:
            self.show_login()

    # إنشاء المدير الأول
    def show_create_admin(self):
        box = toga.Box(style=Pack(direction=COLUMN, padding=20))

        username_input = toga.TextInput(placeholder="اسم المستخدم")
        password_input = toga.PasswordInput(placeholder="كلمة المرور")
        button = toga.Button("إنشاء مدير", on_press=lambda w: self.create_admin_action(username_input.value, password_input.value))

        box.add(username_input)
        box.add(password_input)
        box.add(button)

        self.main_window.content = box
        self.main_window.show()

    def create_admin_action(self, username, password):
        if username and password:
            create_admin(username, password)
            self.show_login()

    # شاشة تسجيل الدخول
    def show_login(self):
        box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        username_input = toga.TextInput(placeholder="اسم المستخدم")
        password_input = toga.PasswordInput(placeholder="كلمة المرور")
        button = toga.Button("تسجيل الدخول", on_press=lambda w: self.login_action(username_input.value, password_input.value))
        box.add(username_input)
        box.add(password_input)
        box.add(button)

        self.main_window.content = box
        self.main_window.show()

    def login_action(self, username, password):
        role = verify_user(username, password)
        if role:
            self.show_dashboard(role)
        else:
            self.main_window.info_dialog("خطأ", "اسم المستخدم أو كلمة المرور غير صحيح!")

    # شاشة المدير أو المندوب
    def show_dashboard(self, role):
        box = toga.Box(style=Pack(direction=COLUMN, padding=20))

        box.add(toga.Label(f"مرحبًا بك! الدور: {role}"))

        if role == "admin":
            box.add(toga.Button("إدارة المستخدمين", on_press=self.not_implemented))
            box.add(toga.Button("إدارة المخزون", on_press=self.not_implemented))
        elif role == "agent":
            box.add(toga.Button("فواتير", on_press=self.not_implemented))
            box.add(toga.Button("جرد المنتجات", on_press=self.not_implemented))

        box.add(toga.Button("خروج", on_press=self.main_window.close))

        self.main_window.content = box
        self.main_window.show()

    def not_implemented(self, widget):
        self.main_window.info_dialog("تنبيه", "هذه الخاصية لم تُفعل بعد.")

def start_app():
    return AlGhamryApp('Al-Ghamry Factory', 'com.alghamry.factory').main_loop()
