# CLAUDE.md — Claude Code (RD-1: dedup stub)

> **Protocol เต็มทั้งหมดอยู่ใน root `CLAUDE.md`** (single source — ใช้ได้ทั้ง template-dev และ clone).
> ไฟล์นี้เคย duplicate ~80% ของ root แล้วทำให้ AI อ่านซ้ำทุก session (compliance-decay) — RD-1 ยุบรวม.

Claude Code auto-loads `CLAUDE.md` จาก root อยู่แล้ว → อ่านที่นั่น. สรุป pointer:

- **Bootstrap / Session Start / Session End / Project Context / TACP / Language / Branching / Key Rules (ครบ 14 ข้อ)** → root `CLAUDE.md`
- **Claude-Code-specific** (Batch Checkpoint, Context Window Management, Game Specialist Agents, `/caw-*` commands รวม game) → root `CLAUDE.md` section "Claude Code-specific" + "Available Slash Commands"
- **AI tool อื่น** (Cursor/Windsurf/claude.ai) → `platforms/universal/AI.md` (universal protocol, ไม่มี auto-hooks)
- **Game specialist agents** ไฟล์จริง → `platforms/claude-code/agents/`

ไม่มี protocol prose ในไฟล์นี้แล้ว — มีอะไรขัดกับ root ให้เชื่อ root.
