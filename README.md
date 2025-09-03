# เว็บแอปรายรับ-รายจ่าย

เว็บแอปสำหรับจัดการการเงินส่วนบุคคล ที่ช่วยให้คุณติดตามรายรับ-รายจ่าย ตั้งงบประมาณ และดูรายงานการเงินได้อย่างครบถ้วน พร้อมรองรับการเชื่อมต่อกับ Supabase เพื่อการจัดการข้อมูลบนคลาวด์

## คุณสมบัติหลัก

- **จัดการรายรับ-รายจ่าย**: บันทึกและติดตามรายการเงินของคุณได้อย่างง่ายดาย
- **ระบบหมวดหมู่**: จัดกลุ่มรายการตามประเภทและหมวดหมู่ที่กำหนดเอง
- **งบประมาณ**: ตั้งงบประมาณรายเดือนสำหรับแต่ละหมวดหมู่
- **รายงานและวิเคราะห์**: ดูรายงานสรุป รายได้-รายจ่าย และแนวโน้มการเงิน
- **แดชบอร์ด**: มุมมองภาพรวมของการเงินของคุณ
- **เชื่อมต่อ Supabase**: จัดเก็บและซิงค์ข้อมูลกับ Supabase (PostgreSQL Cloud)

## การติดตั้ง

### ข้อกำหนดเบื้องต้น
- Python 3.8+
- pip

### ขั้นตอนการติดตั้ง

1. โคลนโปรเจค
```bash
git clone <repository-url>
cd webappincome
```

2. สร้าง virtual environment
```bash
python -m venv env
```

3. เปิดใช้งาน virtual environment
```bash
# Windows
env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

4. ติดตั้ง dependencies
```bash
pip install -r requirements.txt
```

5. สร้างฐานข้อมูล
```bash
python manage.py makemigrations
python manage.py migrate
```

6. สร้างหมวดหมู่เริ่มต้น
```bash
python manage.py setup_categories
```

7. สร้าง superuser (ไม่บังคับ)
```bash
python manage.py createsuperuser
```

8. รันเซิร์ฟเวอร์
```bash
python manage.py runserver
```

9. เปิดเบราว์เซอร์ไปที่ `http://127.0.0.1:8000/`

## การเชื่อมต่อกับ Supabase

1. สมัครและสร้างโปรเจคบน [Supabase](https://supabase.com/)
2. นำค่า `SUPABASE_URL` และ `SUPABASE_KEY` ไปใส่ในไฟล์ `.env` หรือใน `settings.py`
3. ติดตั้งไลบรารี Supabase Python
```bash
pip install supabase
```
4. ใช้งาน Supabase ในโปรเจค เช่นใน `models.py` หรือ `views.py` เพื่ออ่าน/เขียนข้อมูล

## การใช้งาน

### เริ่มต้นใช้งาน

1. **ลงทะเบียน**: สร้างบัญชีผู้ใช้ใหม่
2. **เพิ่มหมวดหมู่**: สร้างหมวดหมู่สำหรับรายรับและรายจ่ายของคุณ
3. **บันทึกรายการ**: เพิ่มรายรับและรายจ่ายตามหมวดหมู่
4. **ตั้งงบประมาณ**: กำหนดงบประมาณรายเดือน
5. **ดูรายงาน**: ติดตามและวิเคราะห์การเงินของคุณ

### หมวดหมู่เริ่มต้น

**รายรับ:**
- เงินเดือน
- โบนัส
- รายได้เสริม
- ดอกเบี้ย
- อื่นๆ

**รายจ่าย:**
- อาหาร
- การเดินทาง
- ที่พัก
- เสื้อผ้า
- ความบันเทิง
- สุขภาพ
- การศึกษา
- ช้อปปิ้ง
- อื่นๆ

## โครงสร้างโปรเจค

```
webappincome/
├── manage.py
├── requirements.txt
├── README.md
├── webappincome/          # Django project settings
├── webpage/              # Main app
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── forms.py          # Forms
│   ├── urls.py           # URL patterns
│   └── admin.py          # Admin interface
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Landing page
│   ├── dashboard.html    # Dashboard
│   ├── transactions.html # Transactions list
│   └── ...
└── statics/             # Static files (CSS, JS, images)
```

## เทคโนโลยีที่ใช้

- **Backend**: Django 5.2.5
- **Database**: SQLite3, Supabase (PostgreSQL)
- **Frontend**: Bootstrap 5, FontAwesome
- **Authentication**: Django built-in user system, Supabase Auth (optional)

## การพัฒนา

### การเพิ่มฟีเจอร์ใหม่

1. สร้างโมเดลใน `models.py`
2. สร้างฟอร์มใน `forms.py`
3. เพิ่ม view ใน `views.py`
4. เพิ่ม URL ใน `urls.py`
5. สร้างเทมเพลตใน `templates/`
6. ทดสอบและรัน migrations

### การทดสอบ

```bash
python manage.py test
```

## การปรับแต่ง

### การเปลี่ยนธีม

แก้ไขไฟล์ `templates/base.html` และ `statics/css/styles.css`

### การเพิ่มหมวดหมู่ใหม่

ใช้ Django admin หรือรัน command:
```bash
python manage.py setup_categories
```

## การแก้ไขปัญหา

### ปัญหาที่พบบ่อย

1. **Database errors**: รัน `python manage.py migrate`
2. **Static files not loading**: รัน `python manage.py collectstatic`
3. **Import errors**: ตรวจสอบ virtual environment
4. **Supabase connection**: ตรวจสอบค่า URL/KEY และการเชื่อมต่ออินเทอร์เน็ต

## การสนับสนุน

หากมีปัญหาหรือคำถาม กรุณาสร้าง issue ใน GitHub repository

## License

MIT License

## ผู้พัฒนา

สิทธิชัย ลบยุทธ, ภัคพล เเก้วคำ, ก้องเกียรติ คงนิล, เเทนไทย พันธุชาติ

---

**หมายเหตุ**:
