# ติดตั้ง Governance ลงโปรเจ็กต์อื่น (2 นาที) — BL-7

## ขั้นตอน (คำสั่งเดียว)

```bash
# จาก repo template นี้ ชี้ไปยังโปรเจ็กต์ของคุณ:
python engine/cli.py init --target /path/to/your-repo
```

ได้อะไร:
- `engine/` — governance engine ครบ (self-contained, ไม่ผูก path กลาง)
- hooks 3 ตัว (merge เข้า `.claude/settings.json` โดย**ไม่ทับ**ของเดิม):
  - **PreToolUse** — บล็อก commit ที่มี secret/placeholder · งานเสี่ยง (force-push ฯลฯ) → Decision Inbox รอคุณอนุมัติ
  - **SessionStart** — ฉีด PROJECT-MEMORY DIGEST (AI จำโปรเจ็กต์ข้าม session)
  - **SessionEnd** — บันทึก session ลง store อัตโนมัติ
- `CoreAiWorkspaces/` state files (สร้างเฉพาะที่ยังไม่มี)

## หลังติดตั้ง (ทางเลือกแต่แนะนำ)

```bash
# 1. ตั้งคำสั่งเทสจริง (เปิดใช้กฎ "done ต้องเทสเขียว"):
cp engine/testcmd.txt.example engine/testcmd.txt   # แล้วแก้เป็นคำสั่งเทสของโปรเจ็กต์

# 2. เปิด Cockpit dashboard:
python engine/api.py    # → http://127.0.0.1:8777
```

## ถอนการติดตั้ง
ลบ `engine/`, `platforms/claude-code/hooks/{govern-action,session-digest,session-writeback}.sh` และ hook entries ใน `.claude/settings.json` — hooks ตรวจเองว่าไม่มี engine แล้วผ่านเงียบ (template-only mode)
