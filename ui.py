from database import admin_exists, create_admin, verify_user

def start_ui():
    if not admin_exists():
        print("إنشاء المدير الأول")
        username = input("اسم المستخدم: ")
        password = input("كلمة المرور: ")
        create_admin(username, password)
        print("تم إنشاء المدير بنجاح!")
    else:
        print("تسجيل الدخول")
        username = input("اسم المستخدم: ")
        password = input("كلمة المرور: ")
        role = verify_user(username, password)
        if role:
            print(f"مرحبا بك، أنت {role}")
            if role == "admin":
                print("لوحة المدير: إضافة مستخدم، إدارة مخزون، فواتير، تقارير")
            elif role == "agent":
                print("لوحة المندوب: فواتير، جرد المنتجات، عرض أسعار")
        else:
            print("اسم المستخدم أو كلمة المرور غير صحيح!")
