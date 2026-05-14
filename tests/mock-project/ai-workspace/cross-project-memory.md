<!-- AI-CONTEXT
last_updated: 2026-04-20
total_projects: 1
active_patterns: 2
-->

# Cross-Project Memory

อัปเดตล่าสุด: 2026-04-20

---

## Patterns That Worked

- **JWT + refresh token rotation** — ป้องกัน token hijack โดยไม่ต้องมี session DB (source: project-alpha, 2026-01)
  Context: REST API ที่ต้องการ stateless auth
  Notes: ต้อง blacklist refresh token เมื่อ logout — ถ้าไม่ทำจะ logout ไม่ได้จริง

- **Rate-limit ก่อน deploy เสมอ** — เจอ DDoS ใน project-alpha หลัง launch (source: project-alpha, 2026-02)
  Context: ทุก API endpoint ที่ exposed ต่อ public
  Notes: ใช้ express-rate-limit กับ Redis store ถ้าต้องการ distributed

---

## Lessons Learned

- **อย่าใช้ Redux กับ project ขนาดเล็ก** (source: project-alpha, 2026-01)
  สิ่งที่เกิดขึ้น: boilerplate มากเกิน overhead สูงสำหรับ state ไม่ซับซ้อน
  วิธีแก้ที่ใช้: migrate ไป Zustand

---

## Reusable Decisions (ADR Cross-Reference)

- **project-alpha/ADR-001**: JWT auth pattern — stateless, refresh rotation
  ใช้ได้กับ: web app ที่ต้องการ auth โดยไม่มี session storage

---

## Project Registry

| Project | Type | Started | Status | Path |
|---------|------|---------|--------|------|
| project-alpha | web app | 2026-01 | active | ~/projects/project-alpha/ |
