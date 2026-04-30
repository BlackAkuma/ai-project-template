# QUICKSTART — ใช้งาน Template

โฟลเดอร์นี้ใช้ **ครั้งเดียว** — AI อ่านแล้วสร้างระบบเอกสารให้ จากนั้นลบโฟลเดอร์นี้ทิ้งได้เลย

---

## ทำไม template ต้องอยู่ในโปรเจ็กต์

AI tool ส่วนใหญ่ (Claude, ChatGPT, Gemini, Claude Code ฯลฯ) อ่านไฟล์ได้เฉพาะในโฟลเดอร์โปรเจ็กต์ที่เปิดอยู่ — ออกไปนอกไม่ได้

ดังนั้น template ต้องอยู่ **ใน** โปรเจ็กต์ก่อน แล้วค่อยลบทิ้งหลัง setup เสร็จ

**ปัญหา:** ถ้า `git clone` ตรง ๆ ใน project ที่มี git อยู่แล้ว จะเกิด nested git repo → git พัง

**วิธีแก้:** ดาวน์โหลดเป็น ZIP แทน — ไม่มี `.git` มาด้วย

---

## Use Case 1 — โปรเจ็กต์ใหม่ ยังไม่มี git

```bash
# 1. สร้าง folder โปรเจ็กต์
mkdir ~/projects/my-new-game
cd ~/projects/my-new-game

# 2. Download template เป็น ZIP แล้วแตกไฟล์
curl -L https://github.com/BlackAkuma/ai-project-template/archive/master.zip -o _template.zip
unzip _template.zip
mv ai-project-template-master _template
rm _template.zip
```

โครงสร้างตอนนี้:
```
my-new-game/
  _template/    ← template อยู่นี่ ลบทิ้งหลัง setup
```

Copy prompt นี้ให้ AI:

```
คุณกำลังจะ setup ระบบเอกสารสำหรับโปรเจ็กต์ใหม่

ข้อมูลโปรเจ็กต์:
- ชื่อ: [PROJECT_NAME]
- Path ที่จะสร้าง doc/: [path โปรเจ็กต์นี้ / current directory]
- Template อยู่ที่: _template/
- ประเภท: [app / web / game / mobile]
- Source docs: [แนบไฟล์มาด้วย / ยังไม่มี]
- เป้าหมาย: [PROJECT_GOAL_SUMMARY]

ขั้นตอน:
1. ถามว่าจะสื่อสารกันเป็นภาษาอะไร รอคำตอบก่อน
2. อ่านไฟล์ทุกไฟล์ใน _template/core/ ตามลำดับ (00 → 18)
3. ถ้าโปรเจ็กต์เป็น game หรือ web game ให้อ่าน _template/skills/game/ ต่อด้วย (00 → 06)
4. สร้างโครงสร้าง doc/ ใน current directory
5. กรอกข้อมูลโปรเจ็กต์ที่มี ถ้าไม่พอใส่ placeholder ห้ามเดา
6. ตรวจสอบกับ _template/core/10-bootstrap-checklist-template.md ก่อนประกาศว่าเสร็จ
```

```bash
# 3. หลัง AI ทำเสร็จ ลบ template ทิ้ง
rm -rf _template/

# 4. Init git แล้ว commit doc/
git init
git add doc/
git commit -m "setup: add AI project documentation"
```

---

## Use Case 2 — โปรเจ็กต์เดิมที่มี git อยู่แล้ว

```bash
# 1. เข้าไปใน project
cd ~/projects/my-existing-game

# 2. Download template เป็น ZIP (ห้าม git clone — จะ nested git)
curl -L https://github.com/BlackAkuma/ai-project-template/archive/master.zip -o _template.zip
unzip _template.zip
mv ai-project-template-master _template
rm _template.zip

```

โครงสร้างตอนนี้:
```
my-existing-game/
  src/          ← code เดิม
  .git/         ← git เดิม (ยังอยู่ครบ)
  _template/    ← template ที่ download มา (ไม่มี .git ซ้อน)
  .gitignore
```

Copy prompt นี้ให้ AI (เหมือน Use Case 1):

```
คุณกำลังจะ setup ระบบเอกสารสำหรับโปรเจ็กต์ที่มีอยู่แล้ว

ข้อมูลโปรเจ็กต์:
- ชื่อ: [PROJECT_NAME]
- Path ที่จะสร้าง doc/: [path โปรเจ็กต์นี้ / current directory]
- Template อยู่ที่: _template/
- ประเภท: [app / web / game / mobile]
- Source docs: [แนบไฟล์มาด้วย / ยังไม่มี]
- เป้าหมาย: [PROJECT_GOAL_SUMMARY]

ขั้นตอน:
1. ถามว่าจะสื่อสารกันเป็นภาษาอะไร รอคำตอบก่อน
2. อ่านไฟล์ทุกไฟล์ใน _template/core/ ตามลำดับ (00 → 18)
3. ถ้าโปรเจ็กต์เป็น game หรือ web game ให้อ่าน _template/skills/game/ ต่อด้วย (00 → 06)
4. สร้างโครงสร้าง doc/ ใน current directory
5. กรอกข้อมูลโปรเจ็กต์ที่มี ถ้าไม่พอใส่ placeholder ห้ามเดา
6. ตรวจสอบกับ _template/core/10-bootstrap-checklist-template.md ก่อนประกาศว่าเสร็จ
```

```bash
# 3. หลัง AI ทำเสร็จ ลบ template ทิ้ง
rm -rf _template/

# 4. Commit doc/ เข้า project git เดิม
# (.gitignore ถูก AI เพิ่ม _template/ ให้แล้วระหว่าง setup)
git add doc/ .gitignore
git commit -m "setup: add AI project documentation"
```

---

## ถ้าใช้ Claude Code — setup เพิ่มเติม

ทำหลังจากขั้นตอนด้านบนเสร็จแล้ว (ก่อนลบ `_template/`):

```bash
# Copy CLAUDE.md ไปที่ root
cp _template/platforms/claude-code/CLAUDE.md ./

# Setup hooks
mkdir -p .claude/hooks
cp _template/platforms/claude-code/hooks/*.sh .claude/hooks/
chmod +x .claude/hooks/*.sh

# Setup rules (ปรับ glob paths ให้ตรงกับโครงสร้าง project)
mkdir -p .claude/rules
cp _template/platforms/claude-code/rules/core-standards.md .claude/rules/
cp _template/platforms/claude-code/rules/design-docs.md .claude/rules/
cp _template/platforms/claude-code/rules/test-standards.md .claude/rules/
# game projects เท่านั้น:
# cp _template/platforms/claude-code/rules/gameplay-code.md .claude/rules/

# Setup slash commands
mkdir -p .claude/skills
cp _template/platforms/claude-code/skills/*.md .claude/skills/

# ลบ template แล้ว commit ทั้งหมด
rm -rf _template/
git add doc/ CLAUDE.md .claude/ .gitignore
git commit -m "setup: add AI project documentation and Claude Code layer"
```

ดูรายละเอียดเพิ่มเติมที่ [`platforms/claude-code/README.md`](platforms/claude-code/README.md)

---

## doc/ กับ git — ต้อง commit ไปด้วยหรือเปล่า?

**ใช่ — ต้อง commit เสมอ**

`doc/` คือ memory ของโปรเจ็กต์ที่ทีมและ AI ทุก session ต้องอ่าน:

| ไฟล์ | ทำไมต้อง commit |
|------|----------------|
| `work-status.md` | AI session ใหม่อ่านตรงนี้เพื่อรู้ว่าต้องทำอะไรต่อ |
| `task-board.md` | track งานที่ค้าง ประวัติการตัดสินใจ |
| `work-log-index.md` | บันทึก session — ทีมรู้ว่าใครทำอะไรไปแล้ว |
| `doc/07-decisions/` | ADR — ป้องกัน AI session ใหม่ reverse decision เดิม |

```bash
# Commit doc/ พร้อมกับ code หรืออย่างน้อย end of day
git add doc/ && git commit -m "docs: update work status and session log"
```

---

## สรุปภาพรวม

```
Setup (ครั้งเดียว):
  Download ZIP → แตกเป็น _template/ → AI อ่าน → สร้าง doc/ → ลบ _template/ → commit doc/

ทุก session หลังจากนั้น:
  AI อ่าน doc/ → ทำงาน → อัพเดต doc/ → commit

ทีมหลายคน:
  git pull → AI อ่าน doc/ → รู้ทันทีว่าโปรเจ็กต์อยู่ตรงไหน ใครทำอะไรไปแล้ว
```
