# วิธีใช้งานโปรเจกต์นี้

## 🔧 ความต้องการเบื้องต้น

- ติดตั้ง [Python 3](https://www.python.org/downloads/) ในเครื่องของคุณแล้ว

## ▶️ วิธีใช้งาน

เปิด terminal และรันคำสั่งต่อไปนี้ตามลำดับ:

1. **สร้าง virtual environment**

   ```bash
   make create_python_env
   ```

2. **ติดตั้ง dependencies จาก `requirements.txt`**

   ```bash
   make install
   ```

3. **รันโปรแกรมหลัก (`main.py`)**

   ```bash
   make update_env
   ```

> 💡 หรือหากต้องการรันทันทีโดยให้ระบบตรวจสอบและติดตั้ง dependencies ให้อัตโนมัติ:

```bash
make update_env
```
