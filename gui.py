import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from database import admin_exists, create_admin, verify_user
from excel_utils import export_raw_materials, import_raw_materials

class AlGhamryApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title="🏭 Al-Ghamry Factory")
        if not admin_exists():
            self.show_create_admin()
        else:
            self.show_login()

    # إنشاء المدير الأول
    def show_create_admin(self):
        box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        username = toga.TextInput(placeholder="اسم المستخدم")
        password = toga.PasswordInput(placeholder="كلمة المرور")
        button = toga.Button("إنشاء مدير", on_press=lambda w: self.create_admin_action(username.value, password.value))
        box.add(username)
        box.add(password)
        box.add(button)
        self.main_window.content = box
        self.main_window.show()

    def create_admin_action(self, username, password):
        if username and password:
            create_admin(username, password)
            self.show_login()

    # تسجيل الدخول
    def show_login(self):
        box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        username = toga.TextInput(placeholder="اسم المستخدم")
        password = toga.PasswordInput(placeholder="كلمة المرور")
        button = toga.Button("تسجيل الدخول", on_press=lambda w: self.login_action(username.value, password.value))
        box.add(username)
        box.add(password)
        box.add(button)
        self.main_window.content = box
        self.main_window.show()

    def login_action(self, username, password):
        role = verify_user(username, password)
        if role:
            self.show_dashboard(role)
        else:
            self.main_window.info_dialog("خطأ", "اسم المستخدم أو كلمة المرور غير صحيح!")

    # لوحة المدير والمندوب
    def show_dashboard(self, role):
        box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        box.add(toga.Label(f"مرحبًا بك! الدور: {role}"))

        if role == "admin":
            box.add(toga.Button("إدارة المواد الخام", on_press=self.manage_raw_materials))
            box.add(toga.Button("إدارة المنتجات", on_press=self.manage_products))
            box.add(toga.Button("تسجيل إنتاج", on_press=self.record_production))
            box.add(toga.Button("فواتير ومرتجعات", on_press=self.manage_invoices))
            box.add(toga.Button("تقارير مالية", on_press=self.show_reports))
            box.add(toga.Button("استيراد/تصدير Excel", on_press=self.manage_excel))

        elif role == "agent":
            box.add(toga.Button("فواتير ومرتجعات", on_press=self.manage_invoices))
            box.add(toga.Button("جرد المنتجات والخامات", on_press=self.show_inventory))
            box.add(toga.Button("عرض أسعار المنتجات", on_press=self.show_prices))

        box.add(toga.Button("خروج", on_press=self.main_window.close))
        self.main_window.content = box
        self.main_window.show()

    # ================= الوظائف الحقيقية =================
    def manage_raw_materials(self, widget):
        self.main_window.info_dialog("المواد الخام", "هنا يمكن إضافة/تعديل/حذف المواد الخام (جاهزة للبرمجة التفصيلية)")

    def manage_products(self, widget):
        self.main_window.info_dialog("المنتجات", "هنا يمكن إدارة المنتجات ووصفات الإنتاج")

    def record_production(self, widget):
        self.main_window.info_dialog("إنتاج", "تسجيل الإنتاج وخصم المخزون تلقائي")

    def manage_invoices(self, widget):
        self.main_window.info_dialog("الفواتير", "إصدار فواتير ومرتجعات")

    def show_reports(self, widget):
        self.main_window.info_dialog("التقارير المالية", "عرض الأرباح والخسائر والديون")

    def manage_excel(self, widget):
        self.main_window.info_dialog("Excel", "استيراد وتصدير البيانات")

    def show_inventory(self, widget):
        self.main_window.info_dialog("جرد المخزون", "عرض كمية المواد الخام والمنتجات")

    def show_prices(self, widget):
        self.main_window.info_dialog("الأسعار", "عرض أسعار المنتجات (سرية الخامات)")

def start_app():
    return AlGhamryApp('Al-Ghamry Factory', 'com.alghamry.factory').main_loop()
