---
globs: ["src/**/*", "app/**/*", "lib/**/*"]
---

# Core Coding Standards

Rules สำหรับ source code ทั้งหมด — โหลดอัตโนมัติเมื่อแก้ไขไฟล์ใน src/, app/, lib/

## สิ่งที่ต้องทำเสมอ

- ทุก function ที่ซับซ้อน (> 20 บรรทัด) ต้องอธิบาย WHY ไม่ใช่ WHAT
- ทุก TODO/FIXME ต้องมี task reference: `// TODO T-XXX: คำอธิบาย`
- dependency ใหม่ทุกตัวต้องมี ADR draft ก่อน merge
- ห้าม hardcode config value ที่อาจเปลี่ยนตาม environment

## สิ่งที่ห้ามทำ

- ห้ามใส่ credentials, API key, หรือ secret ใน code
- ห้าม log sensitive data (password, token, PII)
- ห้ามใช้ `eval()` หรือ dynamic code execution โดยไม่มีเหตุผลชัดเจน
- ห้าม SQL query ที่ต่อ string ตรงจาก user input

## File Size Limit

- ไฟล์เดียว: ไม่เกิน 500 บรรทัด (C-01)
- Function/method: ไม่เกิน 50 บรรทัด (C-05)
- ถ้าเกิน: สร้าง REFACTOR-PENDING task ก่อน merge

## Compliance Tag

เมื่อ defer violation: `// REFACTOR-PENDING[C-XX]: description — T-XXX`
