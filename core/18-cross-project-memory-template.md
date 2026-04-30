# Cross-Project Memory Template

ไฟล์นี้เป็น template สำหรับ `~/ai-workspace/cross-project-memory.md`
วางอยู่นอกโปรเจ็กต์ ระดับ user workspace เพื่อให้ AI ทุก session ทุกโปรเจ็กต์อ่านได้

**วัตถุประสงค์:** เก็บ pattern, lesson learned, และ reusable decisions ที่สะสมข้ามโปรเจ็กต์
AI bootstrap โปรเจ็กต์ใหม่อ่านไฟล์นี้ก่อน — เพื่อไม่เริ่มจากศูนย์ทุกครั้ง

---

## โครงสร้าง workspace

```
~/ai-workspace/                      ← ไม่ใช่ git repo — เป็น local-only workspace
  cross-project-memory.md            ← ไฟล์นี้
  entity-registry.md                 ← entity ที่ใช้ข้ามโปรเจ็กต์ (optional)
```

**กฎ:** ไฟล์นี้ต้องอยู่นอก git เสมอ — เนื้อหาอาจมี pattern ที่ project-specific
ถ้าต้องการแชร์กับทีม ให้ curate เฉพาะส่วนที่ไม่ sensitive แล้ว copy ไปที่ project doc/

---

## กฎการใช้งาน

**เมื่อ AI อ่านไฟล์นี้:**
- อ่านตอน bootstrap โปรเจ็กต์ใหม่ก่อนสร้าง doc/ structure
- ใช้ pattern ที่ relevant กับ project type ปัจจุบัน
- ห้าม apply pattern โดยไม่ตรวจว่า context ตรงกัน
- ถ้า pattern ขัดแย้งกับ source doc ของโปรเจ็กต์ใหม่ → เชื่อ source doc

**เมื่อ AI เขียนลงไฟล์นี้ (ผ่าน /session-end):**
- เพิ่มเฉพาะ pattern ที่ proven — ไม่ใส่สิ่งที่ยังไม่ได้ทดสอบ
- ระบุ source project เสมอ
- ไม่เขียน project-specific detail ที่ไม่ applicable กับโปรเจ็กต์อื่น

---

## Template

```md
<!-- AI-CONTEXT
last_updated: YYYY-MM-DD
total_projects: 0
active_patterns: 0
-->

# Cross-Project Memory

อัปเดตล่าสุด: YYYY-MM-DD

---

## Patterns That Worked

Pattern ที่ทดสอบแล้วในโปรเจ็กต์จริง และใช้ได้ดี

<!-- FORMAT:
- [pattern-name] — [อธิบายสั้น] (source: project-name, date)
  Context: เหมาะกับสถานการณ์แบบไหน
  Notes: ข้อควรระวัง
-->

*(ยังไม่มี pattern — เพิ่มเมื่อมี session แรกที่พบ pattern ที่ควรจำ)*

---

## Lessons Learned

สิ่งที่ลองแล้วไม่ได้ผล หรือทำให้เสียเวลา — เพื่อไม่ให้ทำซ้ำ

<!-- FORMAT:
- [บทเรียน] (source: project-name, date)
  สิ่งที่เกิดขึ้น: ...
  วิธีแก้ที่ใช้: ...
-->

*(ยังไม่มี lesson — เพิ่มเมื่อมีสิ่งที่ควรหลีกเลี่ยง)*

---

## Reusable Decisions (ADR Cross-Reference)

ADR จากโปรเจ็กต์เก่าที่อาจ apply ได้กับโปรเจ็กต์ใหม่

<!-- FORMAT:
- [project-name]/ADR-NNN: [ชื่อ decision] — [สรุปสั้น]
  ใช้ได้กับ: [project type หรือ context]
  Path: ~/projects/[project-name]/doc/07-decisions/ADR-NNN-*.md
-->

*(ยังไม่มี ADR cross-reference)*

---

## Project Registry

โปรเจ็กต์ที่ใช้ template นี้ — เพื่อให้ค้น pattern source ได้

| Project | Type | Started | Status | Path |
|---------|------|---------|--------|------|
| *(เพิ่มเมื่อ bootstrap โปรเจ็กต์แรก)* | | | | |
```

---

## ตัวอย่างที่กรอกแล้ว

```md
<!-- AI-CONTEXT
last_updated: 2026-04-29
total_projects: 2
active_patterns: 3
-->

# Cross-Project Memory

อัปเดตล่าสุด: 2026-04-29

---

## Patterns That Worked

- **JWT + refresh token rotation** — ป้องกัน token hijack โดยไม่ต้องมี session DB (source: project-alpha, 2026-01)
  Context: REST API ที่ต้องการ stateless auth
  Notes: ต้อง blacklist refresh token เมื่อ logout — ถ้าไม่ทำจะ logout ไม่ได้จริง

- **Stripe webhook idempotency key** — ป้องกัน duplicate event โดยไม่ต้อง deduplication table (source: project-beta, 2026-04)
  Context: payment webhook ทุก provider ที่ส่ง event ซ้ำได้
  Notes: ใช้ event ID จาก Stripe เป็น idempotency key โดยตรง

---

## Lessons Learned

- **อย่าใช้ Redux กับ project ขนาดเล็ก** (source: project-alpha, 2026-01)
  สิ่งที่เกิดขึ้น: boilerplate มากเกิน สำหรับ state ที่ไม่ซับซ้อน ทีมใช้เวลาเขียน action/reducer มากกว่า business logic
  วิธีแก้ที่ใช้: migrate ไป Zustand — เบากว่า 80% ของ code ที่เกี่ยวกับ state

---

## Reusable Decisions (ADR Cross-Reference)

- **project-alpha/ADR-003**: Stripe integration pattern — ใช้ SDK official + idempotency key
  ใช้ได้กับ: web app ที่ต้องการ payment integration กับ Stripe
  Path: ~/projects/project-alpha/doc/07-decisions/ADR-003-stripe-integration.md

---

## Project Registry

| Project | Type | Started | Status | Path |
|---------|------|---------|--------|------|
| project-alpha | web app | 2026-01 | active | ~/projects/project-alpha/ |
| project-beta | saas | 2026-03 | active | ~/projects/project-beta/ |
```
