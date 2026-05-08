<!-- AI-CONTEXT
protocol: TACP
version: 1.0
layers: [L1_machine, L2_user, L3_shared]
L2_LANG: th
verbosity_scale: 1-5
status: active
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
- English only (ยกเว้น proper nouns ที่ไม่มีคำแปล)
- Key-value หรือ YAML-like format
- No full sentences
- No polite words
- Abbreviate freely (in_progress, impl, ref, doc, spec)

---

## 3. L2 — User-Facing Rules

### 3.1 Verbosity Scale

AI เลือก verbosity level ตาม message type:

| Level | ชื่อ | ใช้กับ | Max length |
|-------|------|--------|-----------|
| V1 | Terse | ยืนยัน, ack, status single-line | 1-2 บรรทัด |
| V2 | Brief | รายการสั้น, output ที่ชัดเจน, progress | 3-8 บรรทัด |
| V3 | Normal | อธิบาย, ถามคำถาม, วิเคราะห์ | 1 ย่อหน้า + list |
| V4 | Detailed | เสนอ design, ADR, options, review | หลาย section |
| V5 | Full | warning, destructive op, concept ใหม่, ครั้งแรก | ไม่จำกัด + examples |

**Examples:**

```
# V1 — ยืนยัน
เสร็จแล้วครับ — push ขึ้น dev แล้ว

# V2 — รายการ
อัปเดต 3 ไฟล์:
- work-status.md ✓
- task-board.md ✓  
- work-log-index.md ✓

# V3 — อธิบาย
ไฟล์ CLAUDE.md มี reference ไปที่ doc/ ซึ่งไม่มีอยู่แล้ว
แนะนำ update เป็น CoreAiWorkspaces/ — ต้องการให้แก้ไหมครับ?

# V4 — เสนอ design
มีสองทางเลือก:
**A) Component versioning** — แต่ละส่วนมี version ของตัวเอง
  ข้อดี: update เฉพาะจุดได้ | ข้อเสีย: version drift
**B) Single release** — ทุกอย่างออก version เดียวกัน  
  ข้อดี: ง่าย | ข้อเสีย: small fix ต้อง bump ทั้งก้อน
แนะนำ B ครับ เพราะ...

# V5 — warning
⚠️ การดำเนินการนี้ไม่สามารถย้อนกลับได้
จะ reset --hard ซึ่งจะลบ uncommitted changes ทั้งหมด
ตรวจแล้ว: มี 3 ไฟล์ที่ยังไม่ได้ commit ได้แก่ [...]
ยืนยันดำเนินการต่อไหมครับ?
```

### 3.2 Thai Compression Rules

เมื่อ L2_LANG = `th` — AI ใช้กฎต่อไปนี้เพื่อลด token:

**กฎ P-01: One Anchor Per Block**
```
# ✗ ทุกประโยคมี ครับ
ทำเสร็จแล้วครับ ไฟล์อัปเดตแล้วครับ task เสร็จแล้วครับ

# ✓ หนึ่ง anchor ต่อ message block
ทำเสร็จแล้ว ไฟล์อัปเดต task เสร็จ — ครับ
```

**กฎ P-02: Drop Redundant Particles**
```
# ✗ มี particle ที่ไม่เพิ่มความหมาย
มันก็จะทำให้เกิดปัญหาขึ้นมาได้นะ

# ✓ ตัด particle ที่ไม่จำเป็น
อาจเกิดปัญหาได้
```

**กฎ P-03: Prefer Noun Phrases in Lists**
```
# ✗ full sentences ในรายการ
- ระบบจะทำการตรวจสอบ compliance
- ระบบจะทำการอัปเดต work-status

# ✓ noun phrases
- ตรวจ compliance
- อัปเดต work-status
```

**กฎ P-04: Drop Nominalizer When Meaning Preserved**
```
# ✗ การ/ความ ที่ไม่จำเป็น
การทำ compliance check มีความสำคัญมาก

# ✓ ตัด nominalizer
compliance check สำคัญมาก
```

**กฎ P-05: English for Technical Terms**
```
# ✓ ใช้ English สำหรับ technical terms (เป็น convention ปกติในภาษาไทยเทค)
รัน compliance scan ตรวจ C-01 ถึง C-11
อัปเดต AI-CONTEXT block ของ task-board
```

**กฎ P-06: Implied Subject**
```
# ✗ ระบุ subject ซ้ำ
AI จะอ่านไฟล์ แล้ว AI จะวิเคราะห์ แล้ว AI จะรายงาน

# ✓ subject implied จาก context
อ่านไฟล์ → วิเคราะห์ → รายงาน
```

### 3.3 Verbosity Selection Logic

```
IF message is ack/confirm → V1
IF message is progress/status update → V2
IF message is explanation/question → V3
IF message is design proposal/ADR/options → V4
IF message involves: warning | destructive op | new concept | first-time explanation → V5
IF unsure → V3 (default)
```

---

## 4. L3 — Shared File Format

ไฟล์ที่ AI และมนุษย์อ่านร่วมกัน ใช้ **dual-block format**:

```markdown
<!-- AI-CONTEXT
[L1: English key-value block]
cmd: caw-example
steps: [step1, step2, step3]
output_layer: L2
-->
<!-- HUMAN-CONTEXT lang=th
# /caw-example

[L2: Thai explanation for humans]
คำอธิบายการใช้งานสำหรับมนุษย์
-->

[เนื้อหาทั่วไปที่ทั้ง AI และมนุษย์อ่าน]
```

**กฎ:**
- AI-CONTEXT block: L1 rules (English, dense)
- HUMAN-CONTEXT block: L2 rules (L2_LANG, verbosity V3)
- เนื้อหาทั่วไปด้านล่าง: เขียนสำหรับมนุษย์เป็นหลัก

---

## 5. L2_LANG Configuration

ตั้งค่าในไฟล์ `CoreAiWorkspaces/04-way-of-work/way-of-work.md`:

```yaml
tacp:
  L2_LANG: th       # th | en | ja | ...
  verbosity_default: 3
  politeness_level: minimal  # minimal | standard | formal
```

การเปลี่ยน `L2_LANG: en` จะ switch output ภาษาอังกฤษทั้งหมด — ไม่ต้องแก้ไฟล์อื่น

---

## 6. Token Savings Summary

| Category | Before TACP | After TACP | Savings |
|----------|------------|-----------|---------|
| AI-CONTEXT blocks (was Thai) | ~100% Thai | 100% English | 60-70% |
| Thai prose (particle-heavy) | Uncompressed | P-01 to P-06 applied | 25-40% |
| caw-*.md slash commands | Thai human text only | Dual-block | AI reads L1, human reads L2 |
| Verbosity mismatches | V5 for everything | V1-V5 by type | 30-50% for ack/status |

---

## 7. Exceptions

กรณีที่ L1/L2 rule ไม่ apply:

| กรณี | Override |
|------|---------|
| คำเตือนเรื่อง data loss / security | บังคับ V5 เสมอ ไม่ว่า context จะชัดแค่ไหน |
| ผู้ใช้ถามว่า "ทำไม" / "อธิบาย" | V4 ขึ้นไปเสมอ |
| Error message จาก tool | อ้างอิงและสรุป อย่า copy-paste ยาว |
| ผู้ใช้ระบุ verbosity ชัดเจน | ทำตามที่บอก — override scale |

---

## 8. Protocol Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-08 | Initial TACP — 3-layer model, P-01 to P-06, V1-V5 scale |
