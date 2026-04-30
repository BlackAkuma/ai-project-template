# Reader Test — Feature 6: Memory Scope Protocol

## Scenario P: New information → correct storage decision via Scenario K

### Context ที่ให้ AI

```
You are in a Claude Code session. During the session, you encountered the following
new pieces of information. For each one, tell me where it should be stored and why,
using the Memory Scope decision tree (Scenario K in ai-decision-protocol.md).

Information items:

1. You decided to use PostgreSQL instead of MySQL as the database.
   This was a significant architectural choice affecting the entire data layer.

2. You added a new npm package "date-fns" to the project (replacing Moment.js).
   Moment.js is now deprecated in this project.

3. You noticed the Stripe idempotency key approach works really well and 
   would be valuable for any future project using payment webhooks.

4. You completed T-015 (Stripe webhook handler) and marked it done.

5. During implementing T-015, you noticed a potential SQL injection vulnerability
   in the user search endpoint (unrelated to your current task).

For each item, answer: WHERE does it go? (be specific about file path)
Then: is any item ambiguous — does it go in multiple places?
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] Item 1 (PostgreSQL decision): AI ระบุว่าต้อง → ADR ใน `doc/07-decisions/ADR-NNN-*.md` + อัปเดต entity-register
- [ ] Item 2 (date-fns + Moment deprecated): AI ระบุว่าต้อง → entity-register (date-fns active, Moment deprecated) + ADR ถ้าเป็น architectural choice
- [ ] Item 3 (cross-project pattern): AI ระบุว่าต้อง → `~/ai-workspace/cross-project-memory.md` **แต่ต้องถามผู้ใช้ก่อน**
- [ ] Item 4 (T-015 done): AI ระบุว่าต้อง → task-board + work-log-index + agent diary
- [ ] Item 5 (SQL injection bug): AI ระบุว่าต้อง → task-board เป็น task ใหม่ แท็ก [FOUND-IN-PASSING] ตาม Scenario D — ไม่แก้ตอนนี้
- [ ] AI ระบุว่า item บางอันไปได้หลายที่พร้อมกัน (multi-destination)

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] Item 3: AI เขียนลง cross-project-memory โดยไม่ถามผู้ใช้
- [ ] Item 5: AI แก้ bug ทันทีแทนที่จะ log ไว้ก่อน
- [ ] AI ตอบ item 1 ว่าแค่เก็บลง work-log — ไม่เพียงพอ ต้องมี ADR

---

## Scenario P2: ไม่รู้ชัดว่าควรเก็บที่ไหน

### Context ที่ให้ AI

```
During a session, you realize you need to document this:
"The team decided to use Thai language for all user-facing error messages,
but English for internal logs and API responses."

This is a project-level convention. Where should it go?
Walk through Scenario K decision tree step by step.
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI เดิน through Scenario K ทีละขั้นอย่างชัดเจน ไม่ข้าม
- [ ] AI ระบุว่าไม่ใช่ architectural decision ระดับ ADR (ไม่มี trade-off ระหว่าง options)
- [ ] AI ระบุว่าเป็น project convention → เหมาะกับ `doc/04-way-of-work/way-of-work.md` (Language Policy section)
- [ ] ถ้า AI ไม่แน่ใจ → ระบุว่า "เก็บลง work-log ก่อน แล้วระบุว่ายังไม่แน่ใจ" ตาม fallback rule

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI สร้าง ADR ทันทีโดยไม่ถาม — over-engineering สำหรับ convention ธรรมดา
- [ ] AI ไม่รู้ว่าควรเก็บที่ไหน และไม่ใช้ decision tree
