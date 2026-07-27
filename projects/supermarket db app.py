import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
from fpdf import FPDF
import jdatetime
import os
import arabic_reshaper
from bidi.algorithm import get_display


#  تنظیمات اولیه دیتابیس
conn = sqlite3.connect('shop.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand TEXT,
    price REAL NOT NULL,
    category TEXT,
    stock INTEGER DEFAULT 0
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    brand TEXT,
    price REAL NOT NULL,
    qty INTEGER NOT NULL,
    FOREIGN KEY(product_id) REFERENCES products(id)
)
''')

conn.commit()
conn.close()

#-------------------------------------------------------------------------------------------------------------

def add_product():
    name = simpledialog.askstring("افزودن کالا", "نام کالا:")
    if not name:
        return

    brand = simpledialog.askstring("افزودن کالا", "برند کالا:")

    if brand is None:
        brand = ""

    price = simpledialog.askfloat("افزودن کالا", "قیمت کالا:")
    if price is None:

        return

    category = simpledialog.askstring("افزودن کالا", "نوع کالا:")
    if category is None:
        category = ""

    stock = simpledialog.askinteger("افزودن کالا", "موجودی (تعداد):", minvalue=0)
    if stock is None:
        return

    # ذخیر
    with sqlite3.connect('shop.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, brand, price, category, stock) VALUES (?, ?, ?, ?, ?)",
            (name, brand, float(price), category, int(stock))
        )
        conn.commit()
    messagebox.showinfo("موفق", "کالا ثبت شد.")

#-------------------------------------------------------------------------------------------------------------

def show_products():
    with sqlite3.connect('shop.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, brand, price, category, stock FROM products")
        rows = cursor.fetchall()

    if not rows:
        messagebox.showinfo("نمایش کالاها", "هیچ کالایی ثبت نشده است.")
        return

    result_lines = ["لیست کالاها:\n"]
    for r in rows:
        # r = (id, name, brand, price, category, stock)
        result_lines.append(f"شناسه: {r[0]} | نام: {r[1]} | برند: {r[2]} | قیمت: {r[3]} | نوع: {r[4]} | موجودی: {r[5]}")

    messagebox.showinfo("نمایش کالاها", "\n".join(result_lines))


#-------------------------------------------------------------------------------------------------------------

def add_to_cart():
    name = simpledialog.askstring("سبد خرید", "نام کالا:")
    if not name:
        return

    # جستجو در محصولات
    with sqlite3.connect('shop.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, brand, price, category, stock FROM products WHERE name LIKE ?", ('%' + name + '%',))
        results = cursor.fetchall()

    if not results:
        messagebox.showinfo("جستجو", "کالایی یافت نشد.")
        return

    # انتخاب محصول اگر یک نتیجه بود
    if len(results) == 1:
        selected = results[0]
    else:
        options = ""
        for r in results:
            options += f"{r[0]} - {r[1]} | {r[2]} | {r[3]} تومان | موجودی: {r[5]}\n"
        pid = simpledialog.askinteger("انتخاب کالا", f"چند مورد یافت شد:\n{options}\nشناسه مورد نظر را وارد کنید:")
        selected = next((r for r in results if r[0] == pid), None)

    if not selected:
        return

    prod_id = selected[0]

    # singel connect ....
    with sqlite3.connect('shop.db') as conn:
        cursor = conn.cursor()

        # دوباره موجودی میگیریم برای عدم باگ

        cursor.execute("SELECT stock FROM products WHERE id=?", (prod_id,))
        row = cursor.fetchone()
        if not row:
            messagebox.showwarning("خطا", "محصول پیدا نشد.")
            return
        current_stock = row[0]

        if current_stock <= 0:
            messagebox.showwarning("موجودی", "موجودی این کالا صفر است.")
            return

        qty = simpledialog.askinteger("تعداد", f"تعداد مورد نظر را وارد کنید (موجودی: {current_stock}):")
        if not qty:
            return

        if qty > current_stock:
            messagebox.showwarning("محدودیت موجودی", f"تنها {current_stock} عدد موجود است.")
            return

        # بررسی اینکه آیا این محصول از قبل در cart هست
        cursor.execute("SELECT id, qty FROM cart WHERE product_id=?", (prod_id,))
        existing = cursor.fetchone()

        if existing:
            cart_id, cart_qty = existing
            new_qty = cart_qty + qty
            cursor.execute("UPDATE cart SET qty=? WHERE id=?", (new_qty, cart_id))
        else:

            cursor.execute(
                "INSERT INTO cart (product_id, name, brand, price, qty) VALUES (?, ?, ?, ?, ?)",
                (selected[0], selected[1], selected[2], selected[3], qty)
            )

        # کاهش موجودی در جدول products به اندازهٔ مقدار اضافه‌شده

        cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (qty, prod_id))


        conn.commit()

    messagebox.showinfo("موفق", "کالا به سبد خرید اضافه شد.")

#-------------------------------------------------------------------------------------------------------------

def edit_product():
    pid = simpledialog.askinteger("ویرایش کالا", "شناسه کالا را وارد کنید:")
    if not pid:
        return
    with sqlite3.connect('shop.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id=?", (pid,))
        product = cursor.fetchone()
        if not product:

            messagebox.showwarning("خطا", "کالایی با این شناسه یافت نشد.")
            return
        new_name = simpledialog.askstring("ویرایش کالا", f"نام جدید (فعلی: {product[1]}):", initialvalue=product[1])
        new_brand = simpledialog.askstring("ویرایش کالا", f"برند جدید (فعلی: {product[2]}):", initialvalue=product[2])
        new_price = simpledialog.askfloat("ویرایش کالا", f"قیمت جدید (فعلی: {product[3]}):", initialvalue=product[3])
        new_stock = simpledialog.askstring("ویرایش کالا", f"استوک جدید (فعلی: {product[5]}):", initialvalue=product[5])
        if new_brand and new_price is not None:
            cursor.execute("UPDATE products SET name=?, brand=?, price=?,stock=? WHERE id=?", (new_name,new_brand, new_price, new_stock,pid))
            conn.commit()
            messagebox.showinfo("موفق", "کالا با موفقیت ویرایش شد.")

#------------------------------------------------------------------------------------------------------------------

def delete_product():
    pid = simpledialog.askinteger("حذف کالا", "شناسه کالا را وارد کنید:")
    if not pid:
        return
    with sqlite3.connect('shop.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id=?", (pid,))
        product = cursor.fetchone()
        if not product:
            messagebox.showwarning("خطا", "کالایی با این شناسه یافت نشد.")
            return
        confirm = messagebox.askyesno("تأیید حذف", f"آیا مطمئن هستید که می‌خواهید {product[1]} را حذف کنید؟")
        if confirm:
            cursor.execute("DELETE FROM products WHERE id=?", (pid,))
            conn.commit()
            messagebox.showinfo("موفق", "کالا با موفقیت حذف شد.")

#------------------------------------------------------------------------------------------------------------------

def reset_product_ids():

    confirm = messagebox.askyesno("ریست شناسه کالاها",
                                  "آیا مطمئن هستید که می‌خواهید شماره کالاها را از ۱ شروع کنید؟\n"
                                  " این عملیات فقط در صورت خالی بودن جدول محصولات انجام می‌شود.")
    if not confirm:
        return

    with sqlite3.connect('shop.db') as conn:
        cursor = conn.cursor()

        # بررسی اینکه جدول خالی هست یا نه
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]

        if count > 0:
            messagebox.showwarning("ناموفق", "ابتدا باید همه کالاها را حذف کنید.")
            return

        # اگر جدول خالی بود، شمارنده ID ریست می‌شود
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='products'")
        conn.commit()

    messagebox.showinfo("موفق", "id ریست شد")

#-------------------------------------------------------------------------------------------------------------

def show_cart():
    with sqlite3.connect('shop.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, brand, price, qty FROM cart")
        items = cursor.fetchall()

    if not items:
        messagebox.showinfo("سبد خرید", "سبد خرید خالی است.")
        return

    result = " محتوای سبد خرید:\n\n"
    total = 0
    for i, item in enumerate(items, start=1):
        name, brand, price, qty = item
        subtotal = float(qty) * float(price)
        total += subtotal
        result += f"{i}. {name} ({brand}) - {qty} عدد - {price} تومان = {subtotal} تومان\n"

    result += f"\nمبلغ کل: {total} تومان"
    messagebox.showinfo("سبد خرید", result)

#-------------------------------------------------------------------------------------------------------------

def remove_from_cart():
    with sqlite3.connect('shop.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, brand, qty FROM cart")
        items = cursor.fetchall()

    if not items:
        messagebox.showinfo("سبد خرید", "سبد خرید خالی است.")
        return

    options = ""
    for i, item in enumerate(items, start=1):
        options += f"{i}. {item[1]} ({item[2]}) - {item[3]} عدد\n"

    index = simpledialog.askinteger("حذف از سبد", f"آیتم مورد نظر را انتخاب کنید:\n\n{options}")
    if not index or index < 1 or index > len(items):
        return


    item_id, name, brand, qty = items[index - 1]
    with sqlite3.connect('shop.db') as conn:
        cursor = conn.cursor()
        # برگرداندن موجودی کالا
        cursor.execute("SELECT product_id FROM cart WHERE id=?", (item_id,))
        pid = cursor.fetchone()[0]
        cursor.execute("UPDATE products SET stock = stock + ? WHERE id=?", (qty, pid))
        # حذف از سبد خرید
        cursor.execute("DELETE FROM cart WHERE id=?", (item_id,))
        conn.commit()

    messagebox.showinfo("حذف شد", f"{name} از سبد خرید حذف شد و موجودی بازگردانده شد.")

#-------------------------------------------------------------------------------------------------------------

def clear_cart():
    with sqlite3.connect('shop.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, qty FROM cart")
        items = cursor.fetchall()
        for pid, qty in items:
            cursor.execute("UPDATE products SET stock = stock + ? WHERE id=?", (qty, pid))
        cursor.execute("DELETE FROM cart")
        conn.commit()
    messagebox.showinfo("سبد خرید", "سبد خرید خالی شد و موجودی‌ها بازگردانده شدند.")


#-------------------------------------------------------------------------------------------------------------

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        font_path = os.path.join(os.path.dirname(__file__), "font", "Bnazanin.ttf")
        self.add_font("Bnazanin", "", font_path )
        self.set_font("Bnazanin", size=14)


def reshape(text):
    return get_display(arabic_reshaper.reshape(text))

#-------------------------------------------------------------------------------------------------------------

def issue_invoice():

        with sqlite3.connect('shop.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, brand, price, qty FROM cart")
            items = cursor.fetchall()

        if not items:
            messagebox.showwarning("خطا", "سبد خرید خالی است!")
            return

        phone = simpledialog.askstring("مشتری", "شماره تماس مشتری:")
        name = simpledialog.askstring("مشتری", "نام مشتری:")
        if not phone or not name:
            return

        with sqlite3.connect('shop.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone))
            conn.commit()

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Bnazanin", size=12)

        now = datetime.datetime.now()
        j_now = jdatetime.datetime.fromgregorian(datetime=now)
        raw_text = f"ساعت {j_now.hour:02}:{j_now.minute:02}  تاریخ {j_now.year}/{j_now.month:02}/{j_now.day:02}"
        bidi_text = get_display(arabic_reshaper.reshape(raw_text))
        from fpdf.enums import XPos, YPos
        pdf.cell(0, 10, text=bidi_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        pdf.cell(200, 10, text=reshape("فروشگاه افق کوروش"), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.cell(200, 10, text=reshape("فاکتور خرید"), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.cell(200, 10, text=reshape(f"نام: {name} | شماره: {phone}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

        total = 0
        for item in items:
            n, b, p, q = item
            subtotal = float(q) * float(p)
            total += subtotal
            line = f"{n} ({b}) - {int(q)} عدد × {p:.2f} تومان = {subtotal:.2f} تومان"
            pdf.cell(0, 10, text=reshape(line), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.ln(10)
        pdf.cell(0, 10, text=reshape(f"مبلغ کل: {total:.2f} تومان"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        filename = f"invoice_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(filename)

        with sqlite3.connect('shop.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cart")
            conn.commit()

        messagebox.showinfo("فاکتور", f"فاکتور با نام {filename} ذخیره شد.")


#-------------------------------------------------------------------------------------------------------------


# --- رابط گرافیکی ---

# تنظیمات کلی پنجره
root = tk.Tk()
root.title("مدیریت فروشگاه افق کوروش")
root.geometry("400x600")
root.configure(bg="#f7f7f7")  #رنگ پس‌زمینه

# عنوان
title_label = tk.Label(root, text="صندوق فروشگاه",bg="#f7f7f7", fg="#2b2b2b")
title_label.pack(pady=15)

# متن راهنما
lbl = tk.Label(root, text="لطفاً یک گزینه را انتخاب کنید:",bg="#f7f7f7", fg="#333333")
lbl.pack(pady=5)

#   مدیریت کالا
tk.Label(root, text="مدیریت کالاها", bg="#f7f7f7", fg="#0078D7").pack(pady=(10, 2))
tk.Button(root, text="➕ افزودن کالا جدید", width=25, command=add_product).pack(pady=3)
tk.Button(root, text="✏️ ویرایش کالا", width=25, command=edit_product).pack(pady=3)
tk.Button(root, text="🗑️ حذف کالا", width=25, command=delete_product).pack(pady=3)
tk.Button(root, text="📦 نمایش کالاها", width=25, command=show_products).pack(pady=3)
tk.Button(root, text="🔁 ریست شماره کالاها", width=25, command=reset_product_ids).pack(pady=5)

#   سبد خرید
tk.Label(root, text="سبد خرید", bg="#f7f7f7", fg="#0078D7").pack(pady=(15, 2))
tk.Button(root, text="🛒 افزودن به سبد خرید", width=25, command=add_to_cart).pack(pady=3)
tk.Button(root, text="📋 نمایش سبد خرید", width=25, command=show_cart).pack(pady=3)
tk.Button(root, text="❌ حذف از سبد خرید", width=25, command=remove_from_cart).pack(pady=3)
tk.Button(root, text="🧹 خالی کردن سبد خرید", width=25, command=clear_cart).pack(pady=3)

#   صدور فاکتور
tk.Label(root, text="صدور فاکتور", bg="#f7f7f7", fg="#0078D7").pack(pady=(15, 2))
tk.Button(root, text="🧾 صدور فاکتور خرید", width=25, command=issue_invoice).pack(pady=8)

#  خروج
tk.Button(root, text="خروج", width=15, bg="#cc0000", fg="white",command=root.destroy).pack(pady=20)
root.mainloop()