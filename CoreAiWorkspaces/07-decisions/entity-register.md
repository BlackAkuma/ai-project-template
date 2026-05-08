<!-- AI-CONTEXT
entities_active: [bash,markdown,mempalace,chromadb,git]
entities_deprecated: []
last_updated: 2026-05-07
-->

# Entity Register — ai-project-template

อัปเดตล่าสุด: 2026-05-07

## Active Entities

| Entity | Type | Status | Since | ADR | Notes |
|--------|------|--------|-------|-----|-------|
| Bash | lang/runtime | active | 2026-01 | — | สำหรับ scripts/ และ tests/ |
| Markdown (.md) | format | active | 2026-01 | — | ทุก template เป็น .md |
| MemPalace | tool/vector-db | active | 2026-05 | ADR-002 | Phase 3 optional memory — local-first, ChromaDB backend |
| ChromaDB | db | active | 2026-05 | ADR-002 | Backend ของ MemPalace — ไม่ต้อง manage โดยตรง |
| Git (branch-separated) | vcs | active | 2026-01 | ADR-003 | dev / master / gh-pages workflow |

## Deprecated / Removed Entities

| Entity | Type | Status | Since | Until | ADR | Replaced By |
|--------|------|--------|-------|-------|-----|-------------|
| doc/ folder naming | convention | deprecated | 2026-01 | 2026-05-07 | ADR-001 | CoreAiWorkspaces/ folder naming |
