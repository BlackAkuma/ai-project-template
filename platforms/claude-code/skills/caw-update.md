# /caw-update

อัปเดต caw-* commands และ CLAUDE.md เป็น version ล่าสุดจาก template
โดยไม่แตะ CoreAiWorkspaces/, source docs, หรือไฟล์โปรเจ็กต์ใดๆ

---

## ขั้นตอน

### ถ้ามี _template/ อยู่ในโปรเจ็กต์

```bash
bash _template/scripts/new-project.sh "<PROJECT_NAME>" . --update-commands
```

### ถ้าไม่มี _template/ (กรณีทั่วไป)

1. Download template ล่าสุดจาก GitHub:
   ```bash
   mkdir _template
   # วาง ai-project-template ที่ดาวน์โหลดมาใน _template/
   ```

2. รัน update:
   ```bash
   bash _template/scripts/new-project.sh "<PROJECT_NAME>" . --update-commands
   ```

3. ลบ _template/ หลังเสร็จ:
   ```bash
   rm -rf _template/
   ```

---

## สิ่งที่อัปเดต

| ไฟล์ | การกระทำ |
|------|---------|
| `.claude/commands/caw-*.md` | overwrite ด้วย version ใหม่ |
| `CLAUDE.md` | overwrite ด้วย version ใหม่ |

## สิ่งที่ไม่แตะ

| ส่วน | เหตุผล |
|------|-------|
| `CoreAiWorkspaces/` | เนื้อหาโปรเจ็กต์ — ห้ามแตะ |
| source docs | requirement ของโปรเจ็กต์ |
| `.git/` | history โปรเจ็กต์ |
| source code | ไม่ใช่หน้าที่ของ template |
