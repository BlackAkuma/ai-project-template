# Vector Memory — Quick Reference

ใช้ร่วมกับ `core/20-vector-memory-optional.md`
อ่าน core/20 ก่อนเพื่อเข้าใจบริบทและ decision protocol

---

## Requirements

```bash
pip install mempalace
```

disk: ~300 MB สำหรับ embedding model (โหลดครั้งแรกอัตโนมัติ)
Palace: `~/.mempalace/palace` (global — ทุกโปรเจ็กต์ใช้ palace เดียวกัน แยกด้วย wing)

---

## Setup (ครั้งเดียว)

```bash
# 1. (Optional) init wizard — ตรวจ git history, interactive
mempalace init .

# 2. mine ai/ — ต้องระบุ --wing เสมอ (ไม่งั้น wing = 'ai' ชนทุกโปรเจ็กต์)
mempalace mine ai/ --wing <project-name>

# 3. ทดสอบ
mempalace search "test query" --wing <project-name>
mempalace status
```

---

## คำสั่งประจำวัน

```bash
# ค้นหา
mempalace search "<query>" --wing <project-name>

# ค้นหาใน room เฉพาะ
mempalace search "<query>" --wing <project-name> --room general

# อัปเดต index หลังแก้ ai/
mempalace mine ai/ --wing <project-name>

# Wake-up context สำหรับ session start (~600-900 tokens)
mempalace wake-up --wing <project-name>

# ดูสิ่งที่ index ไว้แล้ว
mempalace status

# ค้นข้ามโปรเจ็กต์ (ถ้า mine หลายโปรเจ็กต์)
mempalace search "<query>"   # ไม่ใส่ --wing = ค้นทุก wing
```

---

## Token Budget (ห้ามเกิน)

- สูงสุด **5 chunks** ต่อ search
- สูงสุด **1,500 token** รวมจาก retrieval ทั้งหมด
- Threshold: **0.35** สำหรับ Thai/mixed content, **0.50** สำหรับ English-only
- ทิ้ง chunk ที่ similarity score ต่ำกว่า threshold

---

## Wing Naming Convention

| สิ่งที่ mine | Wing name |
|--------------|-----------|
| `ai/` ของโปรเจ็กต์นี้ | ชื่อโปรเจ็กต์ (lowercase, hyphen) |
| ค้นข้ามทุกโปรเจ็กต์ | ไม่ใส่ `--wing` |

**กฎ:** ต้องระบุ `--wing` ทุกครั้งที่ mine `ai/` subfolder
เพราะ default wing = directory name = 'ai' ซึ่งจะชนกันทุกโปรเจ็กต์

---

## Claude Code MCP Setup

```bash
mempalace mcp   # แสดงคำสั่ง setup สำหรับเชื่อม Claude Code
```

ดูรายละเอียด: https://mempalaceofficial.com/reference/mcp-tools

## Auto-save Hooks Setup

ดู: https://mempalaceofficial.com/guide/hooks

---

## Troubleshooting

**search คืนผลที่ไม่เกี่ยว:**
→ ลอง query ที่เฉพาะขึ้น หรือตรวจ `--wing` ว่าถูกต้อง

**score ต่ำทุก result (< 0.35):**
→ ปกติสำหรับ content ภาษาไทย + English mixed — ดูเนื้อหาว่า relevant ไหม อย่าตัดทิ้งแค่เพราะ score ต่ำ

**mine ใช้เวลานาน:**
→ ปกติ — embedding model รันบนเครื่อง, ครั้งแรกโหลด model ~300 MB

**index เสีย / ผลผิดพลาด:**
```bash
mempalace repair
```
หรือ rebuild ใหม่:
```bash
# mine ซ้ำได้เลย — idempotent, skip ไฟล์ที่ไม่เปลี่ยน
mempalace mine ai/ --wing <project-name>
```
