from mailbox import mbox
from tkinter import *
import sqlite3
from tkinter import messagebox, Menu
from tkinter.ttk import Treeview
from tkinter import ttk, messagebox 
from connect import *
from config import *

""" FRONT END """
def create_window():
    root = Tk()
    root.title("Back office : Be Lune")
    root.geometry("1194x834")
    root.configure(bg=cl_white)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    return root
def create_layout(root):
    fm_main = Frame(root,bg=cl_white,padx=24,pady=24)
    fm_main.grid_rowconfigure(0, weight=1)
    fm_main.grid_columnconfigure(0, weight=1)
    fm_main.grid(row=0, column=0, sticky=NSEW)
    return fm_main

#Menu Bar
def bar_login():
    menu_bar = Menu(root, tearoff=0) 
    menu_bar.add_command(label='login', command=login) 
    menu_bar.add_command(label='exit', command=lambda: exit(0))  
    root.configure(menu=menu_bar)

def bar_home(user):
    
    if user[7] == "admin" :
        menu_bar = Menu(root, tearoff=0)
        menu_bar.add_command(label='dashboard', command=lambda: dashboard(user))  # <- แก้ตรงนี้
        menu_bar.add_command(label='books', command=lambda: stock(user))
        menu_bar.add_command(label='catagory', command=lambda: profile(user))
        menu_bar.add_command(label='shelves', command=lambda: profile(user))
        menu_bar.add_command(label='userManagement', command=lambda: profile(user))
        menu_bar.add_command(label='profile', command=lambda: profileUser(user))
        menu_bar.add_command(label='log out', command=login) 
        root.configure(menu=menu_bar)

    elif user[7] == "librarian" :
        menu_bar = Menu(root, tearoff=0)
        borrow_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_command(label='dashboard', command=lambda: dashboard(user))  # <- แก้ตรงนี้
        borrow_menu.add_command(label='borrowing', command=lambda: stock(user)) 
        menu_bar.add_cascade(label='borrow', menu=borrow_menu)
        menu_bar.add_command(label='history', command=lambda: stock(user))
        menu_bar.add_command(label='books', command=lambda: profile(user))
        menu_bar.add_command(label='category', command=lambda: profile(user))
        menu_bar.add_command(label='shelves', command=lambda: profile(user))
        menu_bar.add_command(label='profile', command=lambda: profileUser(user))
        menu_bar.add_command(label='log out', command=login) 
        root.configure(menu=menu_bar)


#login page   
def login():
    
    # - Layout Frame -
    # frame outside
    fm = Frame(fm_main, bg=cl_white, padx=295, pady=172)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure((0,1,2), weight=1)
    fm.grid_columnconfigure((0,1), weight=1)
    
    # frame inside
    top = Frame(fm,bg=cl_white)
    top.rowconfigure(0,weight=1)
    top.columnconfigure(0,weight=1)
    top.grid(row=0,columnspan=2,sticky=NSEW)
    
    mid = Frame(fm,bg=cl_white)
    mid.rowconfigure((0,1),weight=1)
    mid.columnconfigure((0,1),weight=1)
    mid.grid(row=1,columnspan=2,sticky=NSEW)
    
    bot = Frame(fm,bg=cl_white)
    bot.rowconfigure(0,weight=1)
    bot.columnconfigure(0,weight=1)
    bot.grid(row=2,columnspan=2,sticky=NSEW)
    
    #global veriable
    global username_login_entry, password_login_entry
    username_info = StringVar()
    password_info = StringVar()
    
    #set scale of component
    
    # - component inside -
    #menubar
    bar_login()

    # top frame 
    Label(top,image=logo_img,bg=cl_white).grid(row=0,column=0,sticky='news') 
    
    # mid frame 
    Label(mid,text="username : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=0,column=0,sticky='e')
    username_login_entry = Entry(mid,bg=cl_white_gray, textvariable=username_info)
    username_login_entry.grid(row=0,column=1,sticky='w', ipady=high_entry, ipadx=long_entry, padx=spacing_comp)
    
    Label(mid,text="password  : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=1,column=0,sticky='e')
    password_login_entry = Entry(mid,bg=cl_white_gray,show='*', textvariable=password_info)
    password_login_entry.grid(row=1, column=1, sticky='w', ipady=high_entry, ipadx=long_entry, padx=spacing_comp)

    # bot frame 
    button_login = Button(bot,text="login",bg=cl_red,fg=cl_white,font=font_h3_bold, command=lambda: login_click(username_info.get(),password_info.get()))
    button_login.grid(row=0,column=0, ipadx=50, ipady=5)
        

# ...existing code...
# ...existing code...
def dashboard(user):
    """
    Dashboard สรุปการยืมหนังสือสำหรับบรรณารักษ์
    ใช้ตาราง: borrowings, books, category, student, user
    """
    # พยายาม import matplotlib ถ้าไม่มีให้ข้ามกราฟไป
    try:
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import matplotlib
        import matplotlib.pyplot as plt
        # ฟอนต์ไทย (Windows มี Tahoma อยู่แล้ว)
        matplotlib.rcParams['font.family'] = 'Tahoma'
    except Exception:
        FigureCanvasTkAgg = None
        plt = None

    # ล้างหน้าจอเก่าออกจาก fm_main
    for w in fm_main.winfo_children():
        w.destroy()

    # เฟรมหลักของหน้า dashboard
    fm = Frame(fm_main, bg=cl_white)
    fm.grid(row=0, column=0, sticky=NSEW)
    fm.grid_rowconfigure(0, weight=0)  # title
    fm.grid_rowconfigure(1, weight=0)  # KPI cards
    fm.grid_rowconfigure(2, weight=1)  # content (กราฟ + รายการ)
    fm.grid_columnconfigure(0, weight=1)

    # เมนูด้านบน
    bar_home(user)

    # ฟอนต์ที่ใช้เฉพาะในหน้านี้
    card_title_font = ("Tahoma", 11, "bold")     # หัวข้อการ์ด / หัวข้อ box
    card_value_font = ("Tahoma", 16, "bold")     # ตัวเลขใหญ่
    card_sub_font   = ("Tahoma", 9)              # คำอธิบายย่อย

    # หัวข้อใหญ่
    Label(
        fm,
        text="Dashboard",
        bg=cl_white,
        fg="black",
        font=font_h3_bold
    ).grid(row=0, column=0, sticky=W, padx=spacing_comp, pady=(8, 0))

    #  ฟังก์ชันดึงข้อมูลจาก DB 
    def safe_query(sql, params=()):
        try:
            conn_q, cur_q = db_connection()
            cur_q.execute(sql, params)
            rows = cur_q.fetchall()
            conn_q.close()
            return rows
        except Exception as e:
            print("DB query error:", e, "| SQL:", sql)
            return []


    #   ดึงสถิติจากฐานข้อมูล

    # 1) หมวดหมู่ที่ถูกยืมเยอะที่สุด
    top_cat_name = "-"
    top_cat_total = 0
    r = safe_query("""
        SELECT c.ctgName, COUNT(*) AS total
        FROM borrowings b
        JOIN books bk ON b.bookID = bk.bookID
        JOIN category c ON bk.ctgID = c.ctgID
        GROUP BY c.ctgID, c.ctgName
        ORDER BY total DESC
        LIMIT 1;
    """)
    if r:
        top_cat_name, top_cat_total = r[0]

    # 2) จำนวนคนที่เคยยืม
    r = safe_query("SELECT COUNT(DISTINCT stdID) FROM borrowings;")
    borrower_count = r[0][0] if r and r[0][0] is not None else 0

    # 3) จำนวนครั้งที่ยืมทั้งหมด
    r = safe_query("SELECT COUNT(*) FROM borrowings;")
    total_borrow_count = r[0][0] if r and r[0][0] is not None else 0

    # 4) ยอดยืมเดือนปัจจุบัน
    r = safe_query("""
        SELECT COUNT(*)
        FROM borrowings
        WHERE strftime('%Y-%m', borrowDate) = strftime('%Y-%m', 'now');
    """)
    borrow_this_month = r[0][0] if r and r[0][0] is not None else 0

    # 5) จำนวนหนังสือทั้งหมด
    r = safe_query("SELECT COUNT(*) FROM books;")
    total_books = r[0][0] if r and r[0][0] is not None else 0

    # 6) จำนวนหมวดหมู่
    r = safe_query("SELECT COUNT(*) FROM category;")
    total_categories = r[0][0] if r and r[0][0] is not None else 0

    # 7) จำนวนนักศึกษา
    r = safe_query("SELECT COUNT(*) FROM student;")
    total_students = r[0][0] if r and r[0][0] is not None else 0


    # ยอดยืมรายเดือน (ไว้ทำกราฟ)
    monthly_rows = safe_query("""
        SELECT strftime('%Y-%m', borrowDate) AS mon,
               COUNT(*) AS total
        FROM borrowings
        GROUP BY mon
        ORDER BY mon;
    """)
    monthly_rows = [row for row in monthly_rows if row[0] is not None]

    # Top 5 หนังสือที่ถูกยืมมากที่สุด
    top5_books = safe_query("""
        SELECT bk.title, COUNT(*) AS total
        FROM borrowings b
        JOIN books bk ON b.bookID = bk.bookID
        GROUP BY bk.bookID, bk.title
        ORDER BY total DESC
        LIMIT 5;
    """)

    # จำนวนหนังสือในแต่ละหมวดหมู่
    category_book_counts = safe_query("""
        SELECT c.ctgName, COUNT(b.bookID) AS total
        FROM category c
        LEFT JOIN books b ON c.ctgID = b.ctgID
        GROUP BY c.ctgID, c.ctgName
        ORDER BY total DESC;
    """)

    #   แถวการ์ด KPI ด้านบน (2 แถว × 4 ใบ)
    
    kpi = Frame(fm, bg=cl_white)
    kpi.grid(row=1, column=0, sticky=EW,
             padx=spacing_comp, pady=(spacing_comp, 0))
    for c in range(4):
        kpi.columnconfigure(c, weight=1)

    def kpi_card(parent, row, col, title, value, subtitle=""):
        box = Frame(parent, bg=cl_white, bd=1, relief=SOLID, padx=14, pady=10)
    
        # ถ้าเป็นคอลัมน์แรก (ซ้ายสุด) ไม่ต้องมี padding ด้านซ้าย
        # เพื่อให้ขอบซ้ายของการ์ดตรงกับกราฟด้านล่าง
        if col == 0:
            box.grid(row=row, column=col, padx=(0, 8), pady=6, sticky="nsew")
        else:
            box.grid(row=row, column=col, padx=8, pady=6, sticky="nsew")
    
        Label(
            box,
            text=title,
            bg=cl_white,
            fg="black",
            font=card_title_font
        ).pack(anchor=W)
    
        Label(
            box,
            text=str(value),
            bg=cl_white,
            fg="black",
            font=card_value_font
        ).pack(anchor=W, pady=(2, 0))
    
        if subtitle:
            Label(
                box,
                text=subtitle,
                bg=cl_white,
                fg=cl_gray,
                font=card_sub_font
            ).pack(anchor=W, pady=(2, 0))

    # แถวที่ 1
    kpi_card(
        kpi, 0, 0,
        "หมวดหมู่ที่ยืมเยอะที่สุด",
        top_cat_name,
        f"{top_cat_total} ครั้ง"
    )
    kpi_card(
        kpi, 0, 1,
        "จำนวนผู้ยืม",
        borrower_count,
        "คนที่เคยยืมหนังสือ"
    )
    kpi_card(
        kpi, 0, 2,
        "จำนวนครั้งที่ยืมทั้งหมด",
        total_borrow_count,
        "ตั้งแต่เริ่มใช้ระบบ"
    )
    kpi_card(
        kpi, 0, 3,
        "ยอดยืมเดือนนี้",
        borrow_this_month,
        "ครั้งในเดือนปัจจุบัน"
    )

    # แถวที่ 2
    kpi_card(
        kpi, 1, 0,
        "จำนวนหนังสือทั้งหมด",
        total_books,
        "เล่มในระบบ"
    )
    kpi_card(
        kpi, 1, 1,
        "จำนวนหมวดหมู่",
        total_categories,
        "หมวดหมู่"
    )
    kpi_card(
        kpi, 1, 2,
        "จำนวนนักศึกษา",
        total_students,
        "คนในฐานข้อมูล"
    )
      
    #   พื้นที่หลักด้านล่าง (กราฟ + รายการ)

    content = Frame(fm, bg=cl_white)
    content.grid(row=2, column=0, sticky=NSEW,
                 padx=spacing_comp, pady=spacing_comp)
    content.columnconfigure(0, weight=3)  # ซ้าย
    content.columnconfigure(1, weight=2)  # ขวา
    content.rowconfigure(0, weight=1)

    # ด้านซ้าย : กราฟ + Top 5 
    left = Frame(content, bg=cl_white)
    left.grid(row=0, column=0, sticky=NSEW, padx=(0, 8))
    left.rowconfigure(0, weight=2)  # กราฟ
    left.rowconfigure(1, weight=0)  # Top 5
    left.columnconfigure(0, weight=1)

    # กราฟ
    chart_card = Frame(left, bg=cl_white, bd=1, relief=SOLID, padx=10, pady=10)
    chart_card.grid(row=0, column=0, sticky=NSEW)
    Label(
        chart_card,
        text="ยอดยืมรายเดือน (3 เดือนล่าสุด)",
        bg=cl_white,
        fg="black",
        font=card_title_font
    ).pack(anchor=W)

    # เดือนที่เป็นภาษาไทย
    thai_months = {
        "01": "ม.ค.", "02": "ก.พ.", "03": "มี.ค.", "04": "เม.ย.",
        "05": "พ.ค.", "06": "มิ.ย.", "07": "ก.ค.", "08": "ส.ค.",
        "09": "ก.ย.", "10": "ต.ค.", "11": "พ.ย.", "12": "ธ.ค."
    }

    if monthly_rows and plt and FigureCanvasTkAgg:
        # เอาแค่ 3 เดือนล่าสุด
        monthly_rows_sorted = sorted(monthly_rows, key=lambda r: r[0])
        last_rows = monthly_rows_sorted[-3:]

        month_labels = []
        totals = []
        for ym, total in last_rows:
            year, mon = ym.split("-")
            label_th = f"{thai_months.get(mon, mon)} {year}"
            month_labels.append(label_th)
            totals.append(total)

        x = list(range(len(month_labels)))

        fig, ax = plt.subplots(figsize=(5.5, 2.4))

        # ----- แท่ง (bar) ด้านหลัง -----
        bar_width = 0.6
        ax.bar(
            x,
            totals,
            width=bar_width,
            color="#e1efff",          
            edgecolor="#c0d4f5",
            linewidth=1
        )

        
        ax.plot(
            x,
            totals,
            color="#ff6b6b",          
            marker="o",
            markersize=5,
            linewidth=2
        )

        # เส้นgridแกน Y ช่องๆ
        ax.grid(True, axis="y", linestyle="--", alpha=0.3)

        #ปิดขอบบนขวา
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.set_xticks(x)
        ax.set_xticklabels(month_labels, rotation=45)
        ax.set_xlabel("เดือน")
        ax.set_ylabel("จำนวนครั้งที่ยืม")

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    else:
        Label(chart_card, text="No monthly data",
              bg=cl_white, fg="black").pack(anchor=W, pady=8)

    # Top 5 หนังสือ
    top_box = Frame(left, bg=cl_white, bd=1, relief=SOLID, padx=10, pady=10)
    top_box.grid(row=1, column=0, sticky=EW, pady=(8, 0))
    Label(
        top_box,
        text="Top 5 หนังสือที่ถูกยืมมากที่สุด",
        bg=cl_white,
        fg="black",
        font=card_title_font
    ).pack(anchor=W)

    if top5_books:
        for title, total in top5_books:
            Label(
                top_box,
                text=f"{title} — {total} ครั้ง",
                bg=cl_white,
                anchor="w",
                font=card_sub_font
            ).pack(fill="x")
    else:
        Label(top_box, text="No data", bg=cl_white,
              font=card_sub_font).pack(anchor=W, pady=4)

    #  ด้านขวา  จำนวนหนังสือในแต่ละหมวด 
    right = Frame(content, bg=cl_white)
    right.grid(row=0, column=1, sticky=NSEW, padx=(8, 0))
    right.rowconfigure(0, weight=0)
    right.columnconfigure(0, weight=1)

    category_card = Frame(right, bg=cl_white, bd=1, relief=SOLID, padx=10, pady=10)
    category_card.grid(row=0, column=0, sticky=NSEW)
    Label(
        category_card,
        text="จำนวนหนังสือในแต่ละหมวดหมู่",
        bg=cl_white,
        fg="black",
        font=card_title_font
    ).pack(anchor=W)

    if category_book_counts:
        for name, total in category_book_counts:
            Label(
                category_card,
                text=f"{name} — {total} เล่ม",
                bg=cl_white,
                anchor="w",
                font=card_sub_font
            ).pack(fill="x")
    else:
        Label(
            category_card,
            text="No category data",
            bg=cl_white,
            font=card_sub_font
        ).pack(anchor=W, pady=4)


def books(user):
    fm = Frame(fm_main, bg=cl_white)
    fm.grid(row=0, column=0, sticky=NSEW)
    for widget in fm.winfo_children():
        widget.destroy()
        
    fm.grid_rowconfigure(0, weight=0) # แถว Search ไม่ต้องขยาย
    fm.grid_rowconfigure(1, weight=1) # แถวตาราง ขยายเต็มที่
    fm.grid_rowconfigure(2, weight=0) # แถวปุ่ม ไม่ต้องขยาย
    fm.grid_columnconfigure(0, weight=1)
    bar_home(user)

def catagory(user):
    fm = Frame(fm_main, bg=cl_white)
    fm.grid(row=0, column=0, sticky=NSEW)
    for widget in fm.winfo_children():
        widget.destroy()
        
    fm.grid_rowconfigure(0, weight=0) # แถว Search ไม่ต้องขยาย
    fm.grid_rowconfigure(1, weight=1) # แถวตาราง ขยายเต็มที่
    fm.grid_rowconfigure(2, weight=0) # แถวปุ่ม ไม่ต้องขยาย
    fm.grid_columnconfigure(0, weight=1)
    bar_home(user)

def shelves(user):
    fm = Frame(fm_main, bg=cl_white)
    fm.grid(row=0, column=0, sticky=NSEW)
    for widget in fm.winfo_children():
        widget.destroy()
        
    fm.grid_rowconfigure(0, weight=0) # แถว Search ไม่ต้องขยาย
    fm.grid_rowconfigure(1, weight=1) # แถวตาราง ขยายเต็มที่
    fm.grid_rowconfigure(2, weight=0) # แถวปุ่ม ไม่ต้องขยาย
    fm.grid_columnconfigure(0, weight=1)
    bar_home(user)

def history(user):
    fm = Frame(fm_main, bg=cl_white)
    fm.grid(row=0, column=0, sticky=NSEW)
    for widget in fm.winfo_children():
        widget.destroy()
        
    fm.grid_rowconfigure(0, weight=0) # แถว Search ไม่ต้องขยาย
    fm.grid_rowconfigure(1, weight=1) # แถวตาราง ขยายเต็มที่
    fm.grid_rowconfigure(2, weight=0) # แถวปุ่ม ไม่ต้องขยาย
    fm.grid_columnconfigure(0, weight=1)
    bar_home(user)

def profileUser(user):
    fm = Frame(fm_main, bg=cl_white)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    for widget in fm.winfo_children():
        widget.destroy()
        
    fm.grid_rowconfigure(0, weight=0)
    fm.grid_rowconfigure(1, weight=1)
    fm.grid_rowconfigure(2, weight=0)
    fm.grid_columnconfigure(0, weight=1)
    
    bar_home(user)

    # 1. แกะข้อมูล User ปัจจุบัน (เพื่อเอาไปใส่ในช่องกรอก)
    current_id = user[0]
    
    # สร้างตัวแปร StringVar สำหรับ Tkinter เพื่อรอรับค่าที่แก้ไข
    v_username = StringVar(value=user[1])
    v_password = StringVar(value=user[2])
    v_firstname = StringVar(value=user[3])
    v_lastname = StringVar(value=user[4])
    v_email = StringVar(value=user[5])
    v_tel = StringVar(value=user[6]) 
    v_role = StringVar(value=user[7])

    # --- ฟังก์ชันบันทึกข้อมูลลง Database ---
    def save_profile():
        try:
            conn, cursor = db_connection()
            sql = """
                UPDATE user 
                SET username=?, password=?, firstName=?, lastName=?, email=?, tel=?
                WHERE userID=?
            """
            params = (
                v_username.get(),
                v_password.get(),
                v_firstname.get().strip(), # strip() เพื่อลบช่องว่างท้ายคำถ้ามี
                v_lastname.get().strip(),
                v_email.get(),
                v_tel.get(),
                current_id # ใช้ ID เดิมเป็นตัวอ้างอิง (WHERE)
            )
            
            cursor.execute(sql, params)
            conn.commit()
            
            messagebox.showinfo("Success", "บันทึกข้อมูลเรียบร้อยแล้ว!")
            
            # (Optional) ถ้าอยากให้หน้าจอรีเฟรชข้อมูลใหม่ทันที อาจต้องมีการเรียก query ข้อมูลใหม่อีกรอบ
            # หรือส่งค่าใหม่กลับไปที่ฟังก์ชัน profileUser(new_data_tuple)
        except Exception as e:
            messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {e}")

    def cancel_edit():
        # คืนค่าในช่องกรอก ให้กลับไปเป็นค่าเริ่มต้นจากตัวแปร user
        v_username.set(user[1])
        v_password.set(user[2])
        v_firstname.set(user[3])
        v_lastname.set(user[4])
        v_email.set(user[5])
        v_tel.set(user[6])
        # (ไม่ต้องแจ้งเตือนก็ได้ หรือจะแจ้งก็ได้ครับ)
        # messagebox.showinfo("Cancelled", "คืนค่าข้อมูลเดิมเรียบร้อยแล้ว")

    # --- สร้าง Layout ---
    content_box = Frame(fm, bg=cl_white, padx=20, pady=20)
    content_box.grid(row=1, column=0)

    Label(content_box, text="Edit Profile", font=('Arial', 24, 'bold'), bg=cl_white, fg="#333333").pack(pady=(0, 20))

    # Helper Function สร้างช่องกรอก
    def create_input(label_text, text_var, is_password=False, is_readonly=False):
        row_frame = Frame(content_box, bg=cl_white)
        row_frame.pack(fill='x', pady=5)
        
        Label(row_frame, text=label_text, font=('Arial', 12, 'bold'), width=12, anchor='w', bg=cl_white).pack(side=LEFT)
        
        if is_readonly:
            # ถ้าแก้ไขไม่ได้ ให้ใช้ Entry แต่ disable ไว้ หรือใช้ Label เหมือนเดิมก็ได้
            ent = Entry(row_frame, textvariable=text_var, font=('Arial', 12), state='disabled', disabledbackground="#f0f0f0", disabledforeground="#555")
        else:
            # ถ้าแก้ไขได้
            show_char = '*' if is_password else None
            ent = Entry(row_frame, textvariable=text_var, font=('Arial', 12), show=show_char, bg="#f9f9f9", bd=1, relief=SOLID)
            
        ent.pack(side=LEFT, fill='x', expand=True, ipady=3)

    # แสดงผลช่องต่างๆ
    create_input("User ID :", StringVar(value=current_id), is_readonly=True) # แก้ไม่ได้
    create_input("Role :", v_role, is_readonly=True)    # แก้ไม่ได้ (ปกติ User ไม่ควรแก้ Role เองได้)
    
    Frame(content_box, height=2, bd=1, relief=SUNKEN).pack(fill='x', pady=10) # เส้นคั่น

    create_input("Username :", v_username)
    create_input("Password :", v_password, is_password=False) # ใส่ True ถ้าอยากให้เป็น ****
    create_input("First Name :", v_firstname)
    create_input("Last Name :", v_lastname)
    create_input("Email :", v_email)
    create_input("Tel :", v_tel)

    btn_frame = Frame(content_box, bg=cl_white)
    btn_frame.pack(pady=20)

    # ปุ่ม Save (สีเขียว)
    btn_save = Button(content_box, text="Save", command=save_profile, 
                  font=('Arial', 12, 'bold'), bg="#2ecc71", fg="white", 
                  cursor="hand2", padx=20, pady=5, bd=0)
    btn_save.pack(pady=(20, 5)) # เพิ่มระยะห่างด้านบน 20px, ด้านล่าง 5px

    # ปุ่ม Cancel (สีแดง)
    btn_cancel = Button(content_box, text="Cancel", command=cancel_edit, 
                    font=('Arial', 12), bg="#e74c3c", fg="white", 
                    cursor="hand2", padx=15, pady=5, bd=0)
    btn_cancel.pack(pady=(5, 0)) # เพิ่มระยะห่างด้านบน 5px, ด้านล่าง 0px

def userManagement(user):
    fm = Frame(fm_main, bg=cl_white)
    fm.grid(row=0, column=0, sticky=NSEW)
    for widget in fm.winfo_children():
        widget.destroy()
        
    fm.grid_rowconfigure(0, weight=0) # แถว Search ไม่ต้องขยาย
    fm.grid_rowconfigure(1, weight=1) # แถวตาราง ขยายเต็มที่
    fm.grid_rowconfigure(2, weight=0) # แถวปุ่ม ไม่ต้องขยาย
    fm.grid_columnconfigure(0, weight=1)
    bar_home(user)
    # ==========================================
    # 1. ส่วนค้นหา (Search & Filter)
    # ==========================================
    search_frame = Frame(fm, bg='white')
    search_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

    Label(search_frame, text="ค้นหาจาก:", bg='white').pack(side=LEFT, padx=5)

    # ตัวเลือกคอลัมน์ที่จะค้นหา (Map ชื่อที่โชว์ -> ชื่อใน DB)
    search_options = {
        "Username": "username",
        "First Name": "firstName",
        "Last Name": "lastName",
        "Role": "role"
    }
    
    combo_search = ttk.Combobox(search_frame, values=list(search_options.keys()), state="readonly", width=15)
    combo_search.current(0) # เลือกค่าแรกเป็น Default
    combo_search.pack(side=LEFT, padx=5)

    entry_search = Entry(search_frame, width=20)
    entry_search.pack(side=LEFT, padx=5)

    def search_data():
        selected_display = combo_search.get()
        col_name = search_options[selected_display] # แปลงเป็นชื่อ Column ใน DB
        keyword = entry_search.get()

        # Query ข้อมูลตามเงื่อนไข
        sql = f"SELECT * FROM user WHERE {col_name} LIKE ?"
        cursor.execute(sql, ('%' + keyword + '%',))
        rows = cursor.fetchall()
        update_table(rows)

    btn_search = Button(search_frame, text="ค้นหา", command=search_data, bg='#2196F3', fg='white')
    btn_search.pack(side=LEFT, padx=5)

    btn_reset = Button(search_frame, text="ล้างค่า", command=lambda: load_all_data(), bg='gray', fg='white')
    btn_reset.pack(side=LEFT, padx=5)

    # ==========================================
    # 2. ส่วนตาราง (Treeview)
    # ==========================================
    columns = ('userID', 'username', 'password', 'firstName', 'lastName', 'email', 'tal', 'role')
    tree = ttk.Treeview(fm, columns=columns, show='headings', height=10)
    
    # กำหนดหัวตาราง (Config เหมือนเดิมของคุณ)
    headers = ['User ID', 'Username', 'Password', 'First Name', 'Last Name', 'Email', 'Tel', 'Role']
    for col, head in zip(columns, headers):
        tree.heading(col, text=head)
        tree.column(col, width=100) # ปรับ width ตามชอบ

    tree.grid(row=1, column=0, sticky='nsew', padx=10)

    # Scrollbar
    scrollbar = ttk.Scrollbar(fm, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=1, column=1, sticky='ns')

    # ฟังก์ชันอัปเดตข้อมูลในตาราง
    def update_table(rows):
        tree.delete(*tree.get_children()) # ลบข้อมูลเก่าในตารางออกให้หมด
        for row in rows:
            tree.insert('', 'end', values=row)

    # ฟังก์ชันโหลดข้อมูลทั้งหมด (ตอนเปิดครั้งแรก)
    def load_all_data():
        cursor.execute("SELECT * FROM user")
        rows = cursor.fetchall()
        update_table(rows)
        entry_search.delete(0, END) # ล้างช่องค้นหา

    load_all_data() # เรียกทำงานทันที

    # ==========================================
    # 3. ส่วนปุ่ม Action (Add, Edit, Delete)
    # ==========================================
    btn_frame = Frame(fm, bg='white')
    btn_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)

    # --- ฟังก์ชันสำหรับปุ่มต่างๆ ---
    
    def open_popup(mode, data=None):
        # สร้างหน้าต่างเด้งขึ้นมา (Toplevel)
        popup = Toplevel()
        popup.title(f"{mode} User")
        popup.geometry("400x400")
        
        # สร้างตัวแปรรับค่า
        vars_dict = {}
        fields = ['userID', 'username', 'password', 'firstName', 'lastName', 'email', 'tal', 'role']
        
        for i, field in enumerate(fields):
            Label(popup, text=field).grid(row=i, column=0, padx=10, pady=5, sticky='e')
            entry = Entry(popup)
            entry.grid(row=i, column=1, padx=10, pady=5)
            vars_dict[field] = entry
            
            # ถ้าเป็นโหมด Edit ให้ใส่ข้อมูลเดิมเข้าไป
            if mode == "Edit" and data:
                entry.insert(0, data[i])
                if field == 'userID': # ห้ามแก้ ID
                    entry.config(state='readonly')

        def save_data():
            # ดึงค่าจาก Entry
            values = [vars_dict[f].get() for f in fields]
            cursor = conn.cursor()
            
            if mode == "Add":
                try:
                    cursor.execute("INSERT INTO user VALUES (?,?,?,?,?,?,?,?)", values)
                    conn.commit()
                    messagebox.showinfo("Success", "เพิ่มข้อมูลสำเร็จ")
                    popup.destroy()
                    load_all_data() # รีเฟรชตาราง
                except Exception as e:
                    messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {e}")
            
            elif mode == "Edit":
                try:
                    # Update โดยอ้างอิงจาก userID (ค่าแรกใน values)
                    sql = """UPDATE user SET username=?, password=?, firstName=?, lastName=?, 
                             email=?, tal=?, role=? WHERE userID=?"""
                    # values[1:] คือเอาตั้งแต่ username ถึงตัวสุดท้าย, values[0] คือ ID
                    cursor.execute(sql, (*values[1:], values[0]))
                    conn.commit()
                    messagebox.showinfo("Success", "แก้ไขข้อมูลสำเร็จ")
                    popup.destroy()
                    load_all_data()
                except Exception as e:
                    messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {e}")
            conn.close()

        Button(popup, text="Save", command=save_data, bg='green', fg='white').grid(row=len(fields), column=1, pady=20)

    def add_user():
        open_popup("Add")

    def edit_user():
        selected = tree.selection() # ดูว่า user เลือกแถวไหน
        if not selected:
            messagebox.showwarning("Warning", "กรุณาเลือกรายการที่จะแก้ไข")
            return
        item = tree.item(selected)
        data = item['values'] # ได้ข้อมูลเป็น list
        open_popup("Edit", data)

    def delete_user():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "กรุณาเลือกรายการที่จะลบ")
            return
        
        confirm = messagebox.askyesno("Confirm", "ต้องการลบข้อมูลนี้ใช่หรือไม่?")
        if confirm:
            item = tree.item(selected)
            user_id = item['values'][0] # สมมติว่า ID อยู่คอลัมน์แรก
            cursor.execute("DELETE FROM user WHERE userID = ?", (user_id,))
            conn.commit()
            load_all_data() # รีเฟรชตาราง

    # วางปุ่ม
    Button(btn_frame, text="เพิ่มข้อมูล (Add)", command=add_user, bg='green', fg='white', width=15).pack(side=LEFT, padx=5)
    Button(btn_frame, text="แก้ไข (Edit)", command=edit_user, bg='orange', fg='white', width=15).pack(side=LEFT, padx=5)
    Button(btn_frame, text="ลบ (Delete)", command=delete_user, bg='red', fg='white', width=15).pack(side=LEFT, padx=5)
    

def order(user,order=None):
    # - Layout Frame -
    # frame outside
    fm = Frame(fm_main, bg=cl_white)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure(0, weight=1)
    fm.grid_columnconfigure((0), weight=1)
    fm.grid_rowconfigure(1, weight=10)
    
    # variable
    global  tree_order
    search_var = StringVar()
    # find product
    if order is None:
        order = retrieve_order(user[0])
    # table product
    columns = ("id", "quantity", "total price")
    tree_order = Treeview(fm, columns=columns, show="headings")
    
    # frame inside
    #menubar
    bar_home(user)
    
    #head name page
    Label(fm,text="Order",bg=cl_white,fg='black',font=font_h3_bold).grid(row=0,column=0,sticky=W,padx=spacing_comp)
    
    #search frame
    search_home_entry = Entry(fm,bg=cl_white,fg='black',font=font_h5,textvariable=search_var)
    search_home_entry.grid(row=0,column=1, ipadx=long_entry,ipady=high_entry ,padx=spacing_comp, sticky=E) #Spy Gb
    search_button = Button(fm,image=search_icon,command=lambda: search_order(search_var.get(), user))
    search_button.grid(row=0, column=1,padx=spacing_comp, sticky=E)
    
    # กำหนดหัวตาราง
    for col in columns:
        tree_order.heading(col, text=col)
        tree_order.column(col, width=50, anchor=W)
    
    # เพิ่มข้อมูล
    for row in order:
        tree_order.insert("", END, value=row)
    
    context_menu = Menu(root, tearoff=0)
    context_menu.add_command(label="info", command=lambda: info_order_page(tree_order))
    context_menu.add_command(label="delete", command=lambda: delete_order(tree_order))
    
    #ผูกการคลิกขวากับ show_context_menu
    tree_order.bind("<Button-3>", lambda event: show_context_menu(event, tree_order, context_menu))
    # # แสดง Treeview
    tree_order.grid(row=1, columnspan=3, padx=spacing_comp, sticky=NSEW)
       
def stock(user,product=None):
    # - Layout Frame -
    # frame outside
    fm = Frame(fm_main, bg=cl_white)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure(0, weight=1)
    fm.grid_columnconfigure((0), weight=1)
    fm.grid_rowconfigure(1, weight=10)
    
    # variable
    global  tree_stock
    search_var = StringVar()
    # find product
    if product is None:
        product = retrieve_product(user[0])
    # table product
    columns = ("id", "name", "price", "amount")
    tree_stock = Treeview(fm, columns=columns, show="headings")
    
    # frame inside
    #menubar
    bar_home(user)
    
    #head name page
    Label(fm,text="Stock",bg=cl_white,fg='black',font=font_h3_bold).grid(row=0,column=0,sticky=W,padx=spacing_comp)
    
    #search frame
    search_home_entry = Entry(fm,bg=cl_white,fg='black',font=font_h5,textvariable=search_var)
    search_home_entry.grid(row=0,column=1, ipadx=long_entry,ipady=high_entry ,padx=spacing_comp, sticky=E) #Spy Gb
    search_button = Button(fm,image=search_icon,command=lambda: search_products(search_var.get(), user))
    search_button.grid(row=0, column=1,padx=spacing_comp, sticky=E)
    
    # add product
    add_button = Button(fm,image=add_item_icon, text="add product",fg=cl_black,font=font_h5,compound=LEFT,padx=10, pady=5, bg=cl_white_gray,command=lambda: add_product_page(user))
    add_button.grid(row=0, column=2,padx=spacing_comp, sticky=E)
    

    # กำหนดหัวตาราง
    for col in columns:
        tree_stock.heading(col, text=col)
        tree_stock.column(col, width=50, anchor=W)
    
    # เพิ่มข้อมูล
    for row in product:
        tree_stock.insert("", END, value=row)
    
    context_menu = Menu(root, tearoff=0)
    context_menu.add_command(label="edit", command=lambda: edit_product_page(tree_stock,user))
    context_menu.add_command(label="delete", command=lambda: delete_product(tree_stock))
    
    #ผูกการคลิกขวากับ show_context_menu
    tree_stock.bind("<Button-3>", lambda event: show_context_menu(event, tree_stock, context_menu))
    # # แสดง Treeview
    tree_stock.grid(row=1, columnspan=3, padx=spacing_comp, sticky=NSEW)
    
def profile(user):
    # - Layout Frame -
    # frame outside
    fm = Frame(fm_main, bg=cl_white, padx=295, pady=104)
    fm.grid(row=0, column=0, sticky=NSEW)
    
    # config layout for scroll page
    fm.grid_rowconfigure(0, weight=1)
    fm.grid_rowconfigure(1, weight=1)
    fm.grid_columnconfigure((0,1), weight=1)
    
    # frame inside
    top = Frame(fm,bg=cl_white)
    top.rowconfigure((0,1,2),weight=1)
    top.columnconfigure(0,weight=1)
    top.columnconfigure(1,weight=2)
    top.grid(row=0,columnspan=2,sticky=NSEW)
    
    bot = Frame(fm,bg=cl_white)
    bot.rowconfigure(0,weight=1)
    bot.columnconfigure((0,1),weight=1)
    bot.grid(row=1,columnspan=2,sticky=NSEW)
    
    #global veriable
    global name_profile_entry, username_profile_entry
    username = StringVar(value=user[1])
    password = StringVar(value=user[2])
    name = StringVar(value=user[3])
    user_id = user[0]
    
    #set scale of component
    
    
    # - component inside -
    #menubar
    bar_home(user)
    
    # top frame 
    Label(top,text="name : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=0,column=0,sticky='e')
    name_profile_entry = Entry(top,bg=cl_white_gray, textvariable = name)
    name_profile_entry.grid(row=0,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(top,text="username : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=1,column=0,sticky='e')
    username_profile_entry = Entry(top,bg=cl_white_gray, textvariable = username)
    username_profile_entry.grid(row=1,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(top,text="password  : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=2,column=0,sticky='e')
    password_profile_label = Label(top,bg=cl_white_gray, textvariable = password, anchor=W,)
    password_profile_label.grid(row=2,column=1,sticky='w',ipadx=145 , ipady=high_entry ,padx=spacing_comp)
    
    # bot frame 
    update_btn = Button(bot,text="update profile",bg=cl_red,fg=cl_white,font=font_h3_bold,command=lambda: update_profile(name.get(), username.get(), user_id))
    update_btn.grid(row=0,column=0, ipadx=50, ipady=5, padx=10)
    change_password_btn = Button(bot,text="change password",bg=cl_red,fg=cl_white,font=font_h3_bold,command=lambda: change_password_page(user))
    change_password_btn.grid(row=0,column=1, ipadx=50, ipady=5, padx=10)

""" POP UP """
def change_password_page(user):
    
    popup = Toplevel(fm_main, bg=cl_white)
    popup.title("Change Password")
    popup.geometry("500x200")
    
    popup.grid_rowconfigure((0,1,2), weight=1)
    popup.grid_columnconfigure((0,1), weight=1)

    #global veriable
    global change_password_entry, change_confirm_password_entry
    new_password = StringVar()
    confirm_password = StringVar()
    user_id = user[0]    
    # - component inside -
    
    Label(popup,text="new password : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=0,column=0,sticky='e')
    change_password_entry = Entry(popup,bg=cl_white_gray, textvariable = new_password)
    change_password_entry.grid(row=0,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(popup,text="confirm password : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=1,column=0,sticky='e')
    change_confirm_password_entry = Entry(popup,bg=cl_white_gray, textvariable = confirm_password)
    change_confirm_password_entry.grid(row=1,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    change_password_btn = Button(popup,text="submit",bg=cl_red,fg=cl_white,font=font_h3_bold,command=lambda: change_password(new_password.get(),confirm_password.get(),user_id))
    change_password_btn.grid(row=2,columnspan=2, ipadx=50, ipady=5, padx=10)
    
def edit_product_page(tree,user):
    selected = tree.selection()
    item = tree.item(selected, "values")
    
    popup = Toplevel(fm_main, bg=cl_white)
    popup.title("Edit Product")
    popup.geometry("500x200")
    
    popup.grid_rowconfigure((0,1,2,3), weight=1)
    popup.grid_columnconfigure((0,1), weight=1)

    #veriable
    global name_edit_product_entry, price_edit_product_entry, amount_edit_product_entry
    name_product = StringVar(value=item[1])
    price_product = StringVar(value=item[2])
    amount_product = StringVar(value=item[3])    
    
    # - component inside -
    Label(popup,text="name : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=0,column=0,sticky='e')
    name_edit_product_entry = Entry(popup,bg=cl_white_gray, textvariable = name_product)
    name_edit_product_entry.grid(row=0,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(popup,text="price : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=1,column=0,sticky='e')
    price_edit_product_entry = Entry(popup,bg=cl_white_gray, textvariable = price_product)
    price_edit_product_entry.grid(row=1,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(popup,text="amount : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=2,column=0,sticky='e')
    amount_edit_product_entry = Entry(popup,bg=cl_white_gray, textvariable = amount_product)
    amount_edit_product_entry.grid(row=2,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    edit_product_btn = Button(popup,text="submit",bg=cl_red,fg=cl_white,font=font_h3_bold,command=lambda: edit_product(name_product.get(),price_product.get(),amount_product.get(),item[0],user))
    edit_product_btn.grid(row=3,columnspan=2, ipadx=50, ipady=5, padx=10)

def add_product_page(user):
    popup = Toplevel(fm_main, bg=cl_white)
    popup.title("Add Product")
    popup.geometry("500x200")
    
    popup.grid_rowconfigure((0,1,2,3), weight=1)
    popup.grid_columnconfigure((0,1), weight=1)

    #veriable
    global name_add_product_entry, price_add_product_entry, amount_add_product_entry
    name_product = StringVar()
    price_product = StringVar()
    amount_product = StringVar()
    
    # - component inside -
    Label(popup,text="name : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=0,column=0,sticky='e')
    name_add_product_entry = Entry(popup,bg=cl_white_gray, textvariable = name_product)
    name_add_product_entry.grid(row=0,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(popup,text="price : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=1,column=0,sticky='e')
    price_add_product_entry = Entry(popup,bg=cl_white_gray, textvariable = price_product)
    price_add_product_entry.grid(row=1,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    Label(popup,text="amount : ",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=2,column=0,sticky='e')
    amount_add_product_entry = Entry(popup,bg=cl_white_gray, textvariable = amount_product)
    amount_add_product_entry.grid(row=2,column=1,sticky='w',ipadx=long_entry , ipady=high_entry ,padx=spacing_comp)
    
    add_btn = Button(popup,text="submit",bg=cl_red,fg=cl_white,font=font_h3_bold,command=lambda: add_product(name_product.get(),price_product.get(),amount_product.get(),user))
    add_btn.grid(row=3,columnspan=2, ipadx=50, ipady=5, padx=10)

def info_order_page(tree):
    selected = tree.selection()
    item = tree.item(selected, "values")
    
    popup = Toplevel(fm_main, bg=cl_white)
    popup.title("info order")
    popup.geometry("500x500")
    popup.grid_rowconfigure((0), weight=4)
    popup.grid_rowconfigure((1,2), weight=1)
    popup.grid_columnconfigure((0,1), weight=1)

    #veriable
    global tree_order_info
    
    order_item = retrieve_order_item(item[0])
    for row in order_item:
        value = row[2]  # ดึง column index ที่ 2
        product = retrieve_product_order(value)
        
    print(product)
    columns = ("name", "amount", "price","total price")
    tree_order_info = Treeview(popup, columns=columns, show="headings")
    # - component inside -
    for col in columns:
        tree_order_info.heading(col, text=col)
        tree_order_info.column(col, width=20, anchor=W)
    
    for row in order_item:
        value = row[2]  # ดึง column index ที่ 2
        product = retrieve_product_order(value)
        
        row_data = (
            product[1],
            row[3],
            product[2],
            row[4]
        )
        tree_order_info.insert("", END, value=row_data)
    
    tree_order_info.grid(row=0, columnspan=2, padx=spacing_comp,pady=spacing_comp, sticky=NSEW)
    
    
    Label(popup,text=f"Total Amount : {item[1]}",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=1,columnspan=2,sticky='w', padx=spacing_comp)
    Label(popup,text=f"Total Price : {item[2]}",bg=cl_white,fg=cl_gray,font=font_h5).grid(row=2,columnspan=2,sticky='w', padx=spacing_comp)
    
    
""" BACK END """
def login_click(username,password) :
    # Is username blank?
    if username == "" :
        messagebox.showwarning("Admin:","Please enter username")
        username_login_entry.focus_force()
    else :
        if password == "" :
            # check username exists on database.
            messagebox.showwarning("Admin:","Please enter password")
            password_login_entry.focus_force()
        else :
            # check username and password 
            sql = "select * from user where username = ? and password = ? "
            cursor.execute(sql,[username, password])
            user = cursor.fetchone()
            if user :
                messagebox.showinfo("Admin:","Login Successfully")
                print(user)
                dashboard(user)   # <-- ส่ง user เข้าฟังก์ชัน
            else :
                messagebox.showwarning("Admin:","Username not found\n Please register before Login")
                password_login_entry.select_range(0,END)
                password_login_entry.focus_force()

#ตรวจสอบว่ามีข้อมูล username นี้อยู่ในตารางมั้ย
def check_user(username):
    sql = "select * from user where username = ?"
    cursor.execute(sql, [username])
    profile = cursor.fetchone()    
    return profile

def update_profile(name, username, user_id):
    if name == "" :
        messagebox.showwarning("Admin:","Please enter name")
        name_profile_entry.focus_force() 
    else :
        if username == "" :
            messagebox.showwarning("Admin:","Please enter username")
            username_profile_entry.focus_force()  
        else :
            #เรียกหาข้อมูลเก่าของผู้ใช้งาน
            sql = "select * from users where user_id = ?"
            cursor.execute(sql,[user_id])
            old_username = cursor.fetchone()
            #ตรวจข้อมูลชื่อผู้ใช้ ใหม่ว่าเหมือนกับข้อมูลผู้ใช้คนอื่นมั้ย
            sql = "select * from users where username = ?"
            cursor.execute(sql,[username])
            new_username = cursor.fetchone()
            if new_username :
                #ตรวจสอบว่าซ้ำกันจริง โดยแบ่งเป็นซ้ำกันตัวอื่นหรีอซ้ำกับตัวมันเอง
                if new_username == old_username :   
                    #หากซ้ำกับตัวมันเอง ให้ทำการ update name ได้
                    sql = 'update users set name = ? where user_id = ?'
                    cursor.execute(sql, (name, user_id))
                    conn.commit()
                    if cursor.rowcount > 0:
                        messagebox.showinfo("Update Profile", "Updated profile successfully.")
                        user = retrieve_user(user_id)
                        profile(user)
                    else:
                        messagebox.showwarning("Update Profile", "No data changes.")
                else :
                    messagebox.showwarning("Admin:","The username already exists in the system. Please enter a new username")
                    username_profile_entry.focus_force() 
            else :
                #ทำการ update username และ name
                sql = 'update users set username = ?, name = ? where user_id = ?'
                cursor.execute(sql, (username, name, user_id))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Update Profile", "Updated profile successfully.")
                    user = retrieve_user(user_id)
                    profile(user)
                else:
                    messagebox.showwarning("Update Profile", "No data changes.")   

def retrieve_user_management():
    sql = "select * from user "
    cursor.execute(sql)
    tableUser = cursor.fetchall()
    return tableUser


def retrieve_user(user_id):
    sql = "select * from users where user_id = ?"
    cursor.execute(sql, [user_id])
    user = cursor.fetchone()
    
    return user
def retrieve_product(user_id):
    sql = "select * from products where user_id = ?"
    cursor.execute(sql, [user_id])
    product = cursor.fetchall()
    
    return product
def retrieve_product_order(product_id):
    sql = "select * from products where product_id = ?"
    cursor.execute(sql, [product_id])
    product = cursor.fetchone()
   
    return product
def retrieve_order(user_id):
    sql = "select * from orders where userID = ?"
    cursor.execute(sql, [user_id])
    order = cursor.fetchall()
    
    return order
def retrieve_order_item(order_id):
    sql = "select * from order_items where order_id = ?"
    cursor.execute(sql, [order_id])
    order = cursor.fetchall()
    
    return order

def change_password(new_password, confirm_password, user_id):
    if new_password == "" :
        messagebox.showwarning("Admin:","Please enter new password")
        change_password_entry.focus_force() 
    else :
        if confirm_password == "" :
            messagebox.showwarning("Admin:","Please enter confirm password")
            change_confirm_password_entry.focus_force()  
        else :
            if new_password == confirm_password :
                sql = 'update users set password = ? where user_id = ?'
                cursor.execute(sql, (new_password, user_id))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Update Profile", "Updated new password successfully.")
                    user = retrieve_user(user_id)
                    profile(user)
                else:
                    messagebox.showwarning("Update Profile", "No data changes.")
            else :
                messagebox.showwarning("Admin:","Your new password and confirmation do not match. Kindly confirm your password again")
                change_confirm_password_entry.focus_force() 
def show_context_menu(event, tree, context_menu):
    selected_item = tree.identify_row(event.y)
    if selected_item:
        tree.selection_set(selected_item)
        context_menu.post(event.x_root, event.y_root)
        
def delete_product(tree):
    selected = tree.selection()
    if selected:
        item = tree.item(selected, "values")
        confirm = messagebox.askyesno("Delete", f"ต้องการลบ: {item[1]} หรือไม่?")
        if confirm:
            conn, cursor = db_connection()
            cursor.execute("DELETE FROM products WHERE product_id=?", (item[0],))
            conn.commit()
            conn.close()
            tree.delete(selected)
            messagebox.showinfo("Delete", "ลบข้อมูลสำเร็จแล้ว!")
            
def edit_product(name,price_txt,amount_txt,product_id,user):
    if name == "" :
        messagebox.showwarning("Admin:","Please enter name product")
        name_edit_product_entry.focus_force()  
    else :
        if price_txt == "" :
            messagebox.showwarning("Admin:","Please enter price product")
            price_edit_product_entry.focus_force() 
        else :
            try :
                price = int(price_txt)
            except ValueError:
                messagebox.showerror("Admin:", "Price must be an integer number")
                price_edit_product_entry.focus_force()
                return
            
            if amount_txt == "" :
                messagebox.showwarning("Admin:","Please enter amount product")    
                amount_edit_product_entry.focus_force() 
            else :
                try :
                    amount = int(amount_txt)
                except ValueError:
                    messagebox.showerror("Admin:","Amount must be an integer product")
                    amount_edit_product_entry.focus_force()
                    return
                sql = 'update products set name = ? , price = ?, stock_quantity = ? where product_id = ?'
                cursor.execute(sql, (name, price, amount, product_id))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Edit Product", "Edit product successfully.")
                    stock(user)
                else:
                    messagebox.showwarning("Edit Product", "No data changes.")
                    name_edit_product_entry.focus_force() 
def add_product(name,price_txt,amount_txt,user):
    if name == "" :
        messagebox.showwarning("Admin:","Please enter name product") 
        name_add_product_entry.focus_force() 
    else :
        if price_txt == "" :
            messagebox.showwarning("Admin:","Please enter price product")
            price_add_product_entry.focus_force() 
        else :
            try :
                price = int(price_txt)
            except ValueError:
                messagebox.showerror("Admin:", "Price must be an integer number")
                price_add_product_entry.focus_force()
                return
            if amount_txt == "" :
                messagebox.showwarning("Admin:","Please enter amount product")
                amount_add_product_entry.focus_force()     
            else :
                try :
                    amount = int(amount_txt)
                except ValueError:
                    messagebox.showerror("Admin:","Amount must be an integer product")
                    amount_add_product_entry.focus_force()
                    return
                sql = "insert into products (name, price, stock_quantity, user_id) values ( ?, ?, ?, ?)"
                cursor.execute(sql, (name, price, amount, user[0]))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Add Product", "Add product successfully.")
                    stock(user)
                else:
                    messagebox.showwarning("Add Product", "No data changes.")
                    name_add_product_entry.focus_force() 

def search_products(search_text, user):
    # ล้างข้อมูลเก่าใน treeview
    search = f'%{search_text}%'
    
    for item in tree_stock.get_children():
        tree_stock.delete(item)
        
    # ถ้าไม่ได้กรอกอะไร ให้ดึงทั้งหมด
    if search_text == "":
        sql = "SELECT product_id, name, price, stock_quantity FROM products WHERE user_id = ?"
        cursor.execute(sql, (user[0],))
    else :
        sql = """
        SELECT product_id, name, price, stock_quantity
        FROM products
        WHERE user_id = ?
        AND (
            product_id LIKE ?
            OR name LIKE ?
            OR price LIKE ?
            OR stock_quantity LIKE ?
            )
            """
        cursor.execute(sql, (user[0], search, search, search, search))
    
    results = cursor.fetchall()
    for row in results:
        tree_stock.insert("", END, values=row)

def delete_order(tree):
    selected = tree.selection()
    if selected:
        item = tree.item(selected, "values")
        confirm = messagebox.askyesno("Delete", f"ต้องการคำสั่งซื้อ: {item[1]} หรือไม่ ?")
        if confirm:
            conn, cursor = db_connection()
            order_id = item[0]

            # ลบ order_item ที่มี product_id นี้ก่อน
            cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))

            # ลบ order ที่ไม่มี order_item คงเหลือ
            cursor.execute("""
                DELETE FROM orders
                WHERE order_id NOT IN (
                    SELECT DISTINCT order_id FROM order_items
                )
            """)
            conn.commit()
            conn.close()

            tree.delete(selected)
            messagebox.showinfo("Delete", "ลบคำสั่งซื้อเรียบร้อยแล้ว!")

def search_order(search_text, user):
    # ล้างข้อมูลเก่าใน treeview
    search = f'%{search_text}%'
    
    for item in tree_order.get_children():
        tree_order.delete(item)
        
    # ถ้าไม่ได้กรอกอะไร ให้ดึงทั้งหมด
    if search_text == "":
        sql = "SELECT order_id, quantity , total_price FROM orders WHERE user_id = ?"
        cursor.execute(sql, (user[0],))
    else :
        sql = """
        SELECT order_id, quantity , total_price
        FROM orders
        WHERE user_id = ?
        AND (
            order_id LIKE ?
            )
            """
        cursor.execute(sql, (user[0], search))
    
    results = cursor.fetchall()
    for row in results:
        tree_order.insert("", END, values=row)    
# --------------------------------------------------------------------------------------------------------
root = create_window()
fm_main = create_layout(root)
conn,cursor = db_connection()

# - Spy -


# - img -
logo_img = PhotoImage(file="img/logo_full.png").subsample(4,4)
add_cart_icon = PhotoImage(file="img/add_cart.png")
add_item_icon = PhotoImage(file="img/add_item.png")
delete_icon = PhotoImage(file="img/delete.png")
edit_icon = PhotoImage(file="img/edit.png")
search_icon = PhotoImage(file="img/search.png")


# admin run
sql = "select * from user where userID = 2501001"
cursor.execute(sql)
user = cursor.fetchone()   


# - RUN -
userManagement(user)
root.mainloop()

conn.close()
