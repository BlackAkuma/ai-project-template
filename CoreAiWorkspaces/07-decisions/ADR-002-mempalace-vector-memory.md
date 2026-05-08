# ADR-002: MemPalace เป็น Phase 3 vector memory implementation

**Date:** 2026-05-07
**Status:** Accepted
**Author:** AI session - 2026-05-07
**Source Reference:** ROADMAP.md (Phase 3 planning), https://github.com/MemPalace/mempalace
**Related Tasks:** T-005 (core/20)

## Context

ROADMAP.md ระบุ Phase 3 เป็น "Semantic Search Layer" — ต้องการ vector DB
สำหรับ semantic search ข้าม session เก่าๆ ใน CoreAiWorkspaces/ folder

ข้อกำหนด:
- **Local-first** — ไม่ต้อง cloud API, ไม่มีค่าใช้จ่ายรายเดือน
- **ไม่ LLM call เพิ่ม** — embedding ทำเองบนเครื่อง
- **ใช้ง่าย** — developer ทั่วไปใช้ได้ด้วย `pip install`
- **Claude Code compatible** — ควรมี MCP server support

## Options Considered

1. **MemPalace** — local ChromaDB, Wing/Room/Drawer hierarchy, 29 MCP tools, 96.6% R@5
   Pro: local-first, ไม่ต้อง cloud, MCP ready, pip install ง่าย
   Con: project ยังค่อนข้างใหม่ ต้องการ ~300 MB disk

2. **Chroma standalone** — ChromaDB โดยตรง
   Pro: battle-tested Con: ต้องเขียน integration code เอง, ไม่มี MCP support

3. **Qdrant (local mode)** — Pro: production-grade Con: setup ซับซ้อนกว่า, ไม่มี MCP สำเร็จรูป

4. **OpenAI embeddings + Pinecone** — Pro: powerful Con: cloud dependency, มีค่าใช้จ่าย — ขัด design principle

## Decision

เลือก **MemPalace** เพราะตรงตามข้อกำหนดทุกข้อ:
- Local-first (ChromaDB backend)
- ไม่ต้อง LLM call เพิ่ม
- `pip install mempalace` — ติดตั้งง่าย
- มี 29 MCP tools สำหรับ Claude Code โดยตรง
- Wing/Room/Drawer map ตรงกับโครงสร้าง CoreAiWorkspaces/ ของเรา (project=Wing, subfolder=Room, file=Drawer)

## Consequences

- **ง่ายขึ้น:** user ได้ semantic search แบบ local ไม่มีค่าใช้จ่าย
- **ยากขึ้น:** ต้องใช้ ~300 MB disk สำหรับ embedding model (โหลดครั้งแรก)
- **ต้องระวัง:** MemPalace เป็นโปรเจ็กต์ใหม่ — ต้อง field test ก่อน recommend ให้ user ใช้จริง (T-022)
- Phase 3 เป็น optional — user ไม่ต้องใช้ถ้า Phase 1–2 เพียงพอ

## Review Trigger

ถ้า MemPalace หยุดพัฒนาหรือมี breaking changes → evaluate Chroma standalone แทน
