# Reader Test — Feature 4: Agent Diary Protocol

## Scenario L: Session Start reads agent diary

### Context ที่ให้ AI

```
You are starting a new Claude Code session on a project.

Files available:
- tests/mock-project/CoreAiWorkspaces/01-plan/work-status.md
- tests/mock-project/CoreAiWorkspaces/03-log/work-log-index.md
- tests/mock-project/CoreAiWorkspaces/02-task/task-board.md
- tests/mock-project/CoreAiWorkspaces/03-log/agents/claude-code.md  ← IMPORTANT: this exists

Follow the Session Start Protocol from platforms/claude-code/CLAUDE.md.
Report your session status after completing the protocol.
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI อ่าน AI-CONTEXT block ของ work-status, work-log-index, task-board (3 ไฟล์หลัก)
- [ ] AI ตรวจว่า `CoreAiWorkspaces/03-log/agents/claude-code.md` มีอยู่ และอ่าน AI-CONTEXT block ของมัน
- [ ] AI รายงาน checkpoint จาก diary: "T-015: webhook handler done, pending sandbox test"
- [ ] AI ไม่ข้าม diary step หรือถามว่า "ต้องอ่านไหม" — ทำเป็น standard protocol

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI ข้าม diary อ่านเฉพาะ 3 ไฟล์หลัก ไม่อ่าน diary
- [ ] AI อ่าน diary body ทั้งหมดแทนที่จะอ่าน AI-CONTEXT block ก่อน

---

## Scenario M: Session End writes to agent diary

### Context ที่ให้ AI

```
You are finishing a Claude Code session. You have just completed:
- Wrote Stripe sandbox tests for T-015 (all passing)
- Marked T-015 as done
- Started scoping T-016 (refund flow)

The project has CoreAiWorkspaces/03-log/agents/claude-code.md already.
Run /session-end with summary "sandbox tests passed, T-015 done, starting T-016".
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI sync work-status, work-log-index, task-board (steps 1–6) ตามปกติ
- [ ] AI เพิ่ม entry ใหม่ใน `CoreAiWorkspaces/03-log/agents/claude-code.md` สำหรับ session นี้
- [ ] Entry ใหม่มี: งานที่ทำ (T-015 sandbox tests), decisions, next (T-016)
- [ ] AI อัปเดต AI-CONTEXT block ของ diary: last_session = วันนี้, focus = T-015, checkpoint = none (เสร็จแล้ว)
- [ ] AI ไม่ cross-write ลง diary tool อื่น (เช่น claude-ai.md)

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI ข้าม diary step ทำ steps 1–6 แล้ว jump ไป daily log เลย
- [ ] AI สร้าง diary ใหม่แทนที่จะเพิ่ม entry ใน diary ที่มีอยู่แล้ว
