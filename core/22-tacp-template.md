<!-- AI-CONTEXT
template_id: 22
name: TACP (Token-Aware Communication Protocol)
output_path: CoreAiWorkspaces/04-way-of-work/tacp.md
version: 1.0
-->
# Token-Aware Communication Protocol (TACP)

ระบบควบคุมภาษาและ verbosity ของ AI ทุก session
เป้าหมาย: ลด token waste โดยไม่สูญเสียความชัดเจน

---

## 1. Three-Layer Model

Output destination กำหนด format — ไม่ใช่ topic

| Layer | Destination | Language | Format |
|-------|-------------|----------|--------|
| L1 | Machine-facing (AI-CONTEXT blocks, slash cmd logic, internal reasoning) | English only | Dense, no prose, key-value |
| L2 | User-facing (chat responses) | L2_LANG (default: `th`) | Compressed natural language, verbosity by type |
| L3 | Shared files (read by both AI and human) | Dual-block | AI-CONTEXT block (L1) + HUMAN-CONTEXT block (L2_LANG) |

**กฎหลัก:** AI ไม่ "ตัดสินใจ" ว่าจะใช้ภาษาอะไร — layer ของ destination กำหนดให้อัตโนมัติ

---

## 2. L1 — Machine-Facing Rules

ใช้กับ: AI-CONTEXT blocks, slash command logic files, internal planning

```
# ✓ ถูกต้อง — dense, English, key-value
<!-- AI-CONTEXT
status: in_progress
phase: 3
blocked_by: T-041
next: implement payment flow
-->

# ✗ ผิด — prose, Thai, verbose
<!-- AI-CONTEXT
กำลังทำงานอยู่ในเฟส 3 ซึ่งติดปัญหาที่ T-041 อยู่ก่อน
-->
```

**L1 Rules:**
- English only
- Key-value หรือ YAML-like format
- No full sentences, no polite words
- Abbreviate freely

---

## 3. L2 — User-Facing Rules

### 3.1 Verbosity Scale

| Level | ชื่อ | ใช้กับ | Max length |
|-------|------|--------|-----------|
| V1 | Terse | ยืนยัน, ack, status single-line | 1-2 บรรทัด |
| V2 | Brief | รายการสั้น, progress | 3-8 บรรทัด |
| V3 | Normal | อธิบาย, ถามคำถาม | 1 ย่อหน้า + list |
| V4 | Detailed | เสนอ design, ADR, options | หลาย section |
| V5 | Full | warning, destructive op, concept ใหม่ | ไม่จำกัด + examples |

### 3.2 Thai Compression Rules (L2_LANG = th)

| Rule | กฎ |
|------|----|
| P-01 | One ครับ/ค่ะ anchor per message block — ไม่ใช้ทุกประโยค |
| P-02 | Drop redundant particles (นะ, เลย, ก็, ด้วย ที่ไม่เพิ่มความหมาย) |
| P-03 | Noun phrases in lists แทน full sentences |
| P-04 | Drop การ/ความ nominalizer เมื่อความหมายยังครบ |
| P-05 | English for technical terms (standard Thai tech convention) |
| P-06 | Implied subject — ไม่ระบุ subject ซ้ำ |

### 3.3 Verbosity Selection Logic

```
IF ack/confirm → V1
IF progress/status → V2
IF explanation/question → V3
IF design proposal/ADR/options → V4
IF warning | destructive | new concept | first-time → V5
IF unsure → V3 (default)
```

---

## 4. L3 — Shared File Format (Dual-Block)

ไฟล์ที่ AI และมนุษย์อ่านร่วมกัน:

```markdown
<!-- AI-CONTEXT
[L1: English key-value]
-->
<!-- HUMAN-CONTEXT lang=th
[L2: Thai explanation for humans]
-->

[เนื้อหาทั่วไปสำหรับมนุษย์]
```

---

## 5. L2_LANG Configuration

ตั้งค่าใน `CoreAiWorkspaces/04-way-of-work/way-of-work.md`:

```yaml
tacp:
  L2_LANG: th
  verbosity_default: 3
  politeness_level: minimal
```

เปลี่ยน `L2_LANG` เพื่อ switch ภาษา output ทั้งระบบ

---

## 6. Exceptions

| กรณี | Override |
|------|---------|
| Warning / data loss / security | บังคับ V5 เสมอ |
| ผู้ใช้ถามว่า "ทำไม" / "อธิบาย" | V4 ขึ้นไปเสมอ |
| ผู้ใช้ระบุ verbosity ชัดเจน | ทำตามที่บอก |
