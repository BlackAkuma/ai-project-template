# Vector Memory — Quick Reference

ใช้ร่วมกับ `core/20-vector-memory-optional.md`
อ่าน core/20 ก่อนเพื่อเข้าใจบริบทและ decision protocol

---

## Requirements

```bash
pip install mempalace
```

disk: ~300 MB สำหรับ embedding model (โหลดครั้งแรกอัตโนมัติ)

---

## Setup (ครั้งเดียว)

```bash
# 1. สร้าง palace
mempalace init ~/ai-workspace/mempalace/<project-name>

# 2. index ไฟล์ทั้งหมดใน ai/
mempalace mine ai/ --wing <project-name>

# 3. ทดสอบ
mempalace search "test query" --wing <project-name>
```

---

## คำสั่งประจำวัน

```bash
# ค้นหา
mempalace search "<query>" --wing <project-name>

# อัปเดต index หลังแก้ ai/
mempalace mine ai/ --wing <project-name>

# ค้นข้ามโปรเจ็กต์
mempalace search "<query>" --wing ai-workspace
```

---

## Token Budget (ห้ามเกิน)

- สูงสุด **5 chunks** ต่อ search
- สูงสุด **1,500 token** รวมจาก retrieval ทั้งหมด
- ทิ้ง chunk ที่ similarity score < 0.60

---

## Wing Naming Convention

| สิ่งที่ index | Wing name |
|--------------|-----------|
| โปรเจ็กต์นี้ | ชื่อโปรเจ็กต์ (lowercase, hyphen) |
| cross-project memory | `ai-workspace` |

---

## Claude Code MCP Setup

ดู: https://mempalaceofficial.com/reference/mcp-tools

## Auto-save Hooks Setup

ดู: https://mempalaceofficial.com/guide/hooks

---

## Troubleshooting

**search คืนผลที่ไม่เกี่ยว:**
→ ลอง query ที่เฉพาะขึ้น หรือเพิ่ม `--wing` ให้ถูกต้อง

**mine ใช้เวลานาน:**
→ ปกติ — embedding model รันบนเครื่อง, ครั้งแรกโหลด model ~300 MB

**index เสีย / ผลผิดพลาด:**
```bash
rm -rf ~/ai-workspace/mempalace/<project-name>
mempalace init ~/ai-workspace/mempalace/<project-name>
mempalace mine ai/ --wing <project-name>
```
