# Coding Standards Template

คัดลอกและปรับไฟล์นี้เป็น `CoreAiWorkspaces/04-way-of-work/coding-standards.md`

## Working Principle

- พัฒนาจาก flow หลักของผู้ใช้ก่อน feature รอง
- ทุกงานต้องตอบให้ได้ก่อนว่า:
  - ผู้ใช้คือใคร
  - ใช้หน้าหรือ API ไหน
  - ขั้นตอนก่อนหน้าและหลังจากนั้นคืออะไร
  - งานนี้ผูกกับ workflow หลักของระบบตรงไหน

## Naming

- ใช้ชื่อที่สื่อความหมายตรงไปตรงมา
- function ต้องบอกพฤติกรรม
- variable ต้องบอกข้อมูลที่เก็บ
- component ต้องบอกบทบาทบนหน้าจอ

## File Size and Structure

- ไฟล์โค้ดไม่ควรยาวเกิน `500` บรรทัด ไม่นับคอมเมนต์และบรรทัดว่าง
- ถ้าไฟล์เริ่มยาว ให้แยกตาม concern จริง

## Comments

- เขียนคอมเมนต์เท่าที่จำเป็น
- คอมเมนต์ควรอธิบายเหตุผล, constraint, invariant, หรือ tradeoff

## Change Discipline

- แก้ให้อยู่ใน scope ของงานเดียวกัน
- ถ้าเปลี่ยน workflow, architecture, database, storage, หรือ API contract ต้องอัปเดตเอกสารรอบเดียวกัน

## Verification

- ก่อนปิดงานต้องมี validation อย่างน้อยหนึ่งอย่างที่สัมพันธ์กับงาน
- ถ้ายังไม่ได้ตรวจ ต้องเขียนชัดว่าอะไรยังไม่ได้ตรวจ

## Git Policy

- ห้าม commit `.env`, credentials, runtime logs, export outputs, และ local-only files
- ถ้า repo ไม่ต้องเก็บ daily records ให้ ignore ตั้งแต่ต้น
