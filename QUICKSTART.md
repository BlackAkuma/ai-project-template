# QUICKSTART — ใช้งาน Template

โฟลเดอร์นี้ใช้ **ครั้งเดียว** — AI อ่านแล้วสร้างระบบเอกสารให้ จากนั้นลบโฟลเดอร์นี้ทิ้งได้เลย

---

## หลักการสำคัญก่อนอ่านต่อ

```
Template folder  ←  อ่านครั้งเดียว แล้วลบทิ้ง
    ↓ AI อ่านแล้วสร้าง
doc/ folder      ←  อยู่ในโปรเจ็กต์ของคุณตลอดไป ต้อง commit ใน git ด้วย
```

**template folder และ project ต้องอยู่คนละที่** — ห้าม clone template ไว้ใน folder โปรเจ็กต์ เพราะ git จะชนกัน

---

## Use Case 1 — โปรเจ็กต์ใหม่ ยังไม่มี git

```
/home/you/
  temp/
    ai-project-template/   ← clone template ที่นี่ (นอก project)
  projects/
    my-new-game/           ← folder โปรเจ็กต์ใหม่
```

**ขั้นตอน:**

```bash
# 1. Clone template ไว้ที่ temp (หรือที่ไหนก็ได้นอก project)
git clone https://github.com/BlackAkuma/ai-project-template.git ~/temp/ai-project-template

# 2. สร้าง folder โปรเจ็กต์
mkdir ~/projects/my-new-game

# 3. Copy prompt ด้านล่างให้ AI ระบุ path ทั้งสอง
```

Copy prompt นี้ให้ AI:

```
คุณกำลังจะ setup ระบบเอกสารสำหรับโปรเจ็กต์ใหม่

ข้อมูลโปรเจ็กต์:
- ชื่อ: [PROJECT_NAME]
- Path ที่จะสร้าง doc/: [/home/you/projects/my-new-game]
- Template อยู่ที่: [/home/you/temp/ai-project-template]
- ประเภท: [app / web / game / mobile]
- Source docs: [แนบไฟล์มาด้วย / ยังไม่มี]
- เป้าหมาย: [PROJECT_GOAL_SUMMARY]

ขั้นตอน:
1. ถามว่าจะสื่อสารกันเป็นภาษาอะไร รอคำตอบก่อน
2. อ่านไฟล์ทุกไฟล์ใน core/ ตามลำดับ (00 → 16)
3. ถ้าโปรเจ็กต์เป็น game หรือ web game ให้อ่าน skills/game/ ต่อด้วย (00 → 06)
4. สร้างโครงสร้าง doc/ ที่ path ด้านบน
5. กรอกข้อมูลโปรเจ็กต์ที่มี ถ้าไม่พอใส่ placeholder ห้ามเดา
6. ตรวจสอบกับ core/10-bootstrap-checklist-template.md ก่อนประกาศว่าเสร็จ
```

```bash
# 4. หลัง AI ทำเสร็จ ลบ template ทิ้ง
rm -rf ~/temp/ai-project-template

# 5. Init git ใน project แล้ว commit doc/ ด้วย
cd ~/projects/my-new-game
git init
git add doc/
git commit -m "setup: add AI project documentation"
```

---

## Use Case 2 — โปรเจ็กต์เดิมที่มี git อยู่แล้ว

```
/home/you/
  temp/
    ai-project-template/   ← clone template ที่นี่ (นอก project!)
  projects/
    my-existing-game/      ← โปรเจ็กต์เดิม มี .git อยู่แล้ว
      src/
      .git/
```

**ขั้นตอน:**

```bash
# 1. Clone template ไว้นอก project
git clone https://github.com/BlackAkuma/ai-project-template.git ~/temp/ai-project-template

# 2. Copy prompt ด้านล่างให้ AI ชี้ไปที่ project เดิม
```

Copy prompt นี้ให้ AI (เหมือน Use Case 1 ต่างแค่ path):

```
คุณกำลังจะ setup ระบบเอกสารสำหรับโปรเจ็กต์ที่มีอยู่แล้ว

ข้อมูลโปรเจ็กต์:
- ชื่อ: [PROJECT_NAME]
- Path ที่จะสร้าง doc/: [/home/you/projects/my-existing-game]
- Template อยู่ที่: [/home/you/temp/ai-project-template]
- ประเภท: [app / web / game / mobile]
- Source docs: [แนบไฟล์มาด้วย / ยังไม่มี]
- เป้าหมาย: [PROJECT_GOAL_SUMMARY]

ขั้นตอน:
1. ถามว่าจะสื่อสารกันเป็นภาษาอะไร รอคำตอบก่อน
2. อ่านไฟล์ทุกไฟล์ใน core/ ตามลำดับ (00 → 16)
3. ถ้าโปรเจ็กต์เป็น game หรือ web game ให้อ่าน skills/game/ ต่อด้วย (00 → 06)
4. สร้างโครงสร้าง doc/ ที่ path ด้านบน
5. กรอกข้อมูลโปรเจ็กต์ที่มี ถ้าไม่พอใส่ placeholder ห้ามเดา
6. ตรวจสอบกับ core/10-bootstrap-checklist-template.md ก่อนประกาศว่าเสร็จ
```

```bash
# 3. หลัง AI ทำเสร็จ ลบ template ทิ้ง
rm -rf ~/temp/ai-project-template

# 4. Commit doc/ เข้า project git เดิม
cd ~/projects/my-existing-game
git add doc/
git commit -m "setup: add AI project documentation"
```

---

## ถ้าใช้ Claude Code — setup เพิ่มเติม

ทำหลังจาก `doc/` setup เสร็จแล้ว:

```bash
# 5. Copy CLAUDE.md ไปที่ root ของ project
cp ~/temp/ai-project-template/platforms/claude-code/CLAUDE.md ~/projects/my-game/

# 6. Setup hooks
mkdir -p ~/projects/my-game/.claude/hooks
cp ~/temp/ai-project-template/platforms/claude-code/hooks/*.sh ~/projects/my-game/.claude/hooks/
chmod +x ~/projects/my-game/.claude/hooks/*.sh

# 7. Setup rules
mkdir -p ~/projects/my-game/.claude/rules
cp ~/temp/ai-project-template/platforms/claude-code/rules/*.md ~/projects/my-game/.claude/rules/

# game projects เท่านั้น — ลบ gameplay-code.md ออกถ้าไม่ใช่ game

# 8. Setup slash commands
mkdir -p ~/projects/my-game/.claude/skills
cp ~/temp/ai-project-template/platforms/claude-code/skills/*.md ~/projects/my-game/.claude/skills/

# 9. Commit ทั้งหมด
cd ~/projects/my-game
git add CLAUDE.md .claude/
git commit -m "setup: add Claude Code platform layer"
```

ดูรายละเอียดเพิ่มเติมที่ [`platforms/claude-code/README.md`](platforms/claude-code/README.md)

---

## doc/ กับ git — ต้อง commit ไปด้วยหรือเปล่า?

**ใช่ — ต้อง commit เสมอ**

`doc/` ไม่ใช่แค่เอกสาร มันคือ **memory ของโปรเจ็กต์**:

| ไฟล์ | ทำไมต้อง commit |
|------|----------------|
| `doc/01-plan/work-status.md` | AI session ใหม่อ่านตรงนี้เพื่อรู้ว่าต้องทำอะไรต่อ |
| `doc/02-task/task-board.md` | track งานที่ค้าง ประวัติการตัดสินใจ |
| `doc/03-log/` | บันทึก session — ทีมรู้ว่าใครทำอะไรไปแล้ว |
| `doc/07-decisions/` | ADR — ป้องกัน AI session ใหม่ reverse decision เดิม |

**แนะนำ:** commit `doc/` พร้อมกับ code ทุกครั้ง หรืออย่างน้อย end of day

```bash
git add doc/ && git commit -m "docs: update work status and session log"
```

---

## สรุปภาพรวม

```
ครั้งเดียว (setup):
  Clone template → AI อ่าน → สร้าง doc/ → ลบ template → commit doc/

ทุก session หลังจากนั้น:
  AI อ่าน doc/ → ทำงาน → อัพเดต doc/ → commit

ทีม:
  ทุกคน pull ล่าสุด → AI อ่าน doc/ → รู้ทันทีว่าโปรเจ็กต์อยู่ตรงไหน
```
