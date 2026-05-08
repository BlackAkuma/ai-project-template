<!-- AI-CONTEXT
phase: feature-complete
active_task: T-035 done (feat/savetoken — await merge approval)
blocker: none
last_updated: 2026-05-08
git_mode: branch-separated
git_dev_branch: dev
git_prod_branch: master
active_branch: feat/savetoken
read_more:
  plan: CoreAiWorkspaces/01-plan/project-plan.md
  decisions: CoreAiWorkspaces/07-decisions/README.md
  roadmap: ROADMAP.md
next_action: รอ user อนุมัติ merge feat/savetoken → dev → master (v1.5.0)
-->

# Work Status — ai-project-template

อัปเดตล่าสุด: 2026-05-08

## สถานะปัจจุบัน

**Phase:** feature-complete — TACP v1.5.0 พร้อม merge ✅
**Active Task:** T-035 (feat/savetoken) — done, await merge approval
**Blocker:** none

## สิ่งที่เสร็จแล้ว session นี้ (2026-05-08 TACP)

### TACP — Token-Aware Communication Protocol (T-035) ✅

- `core/22-tacp-template.md` — template ใหม่ distribute ไปยัง new projects
- `CoreAiWorkspaces/04-way-of-work/tacp.md` — protocol anchor เต็ม
- `CLAUDE.md` + `platforms/claude-code/CLAUDE.md` — TACP section
- `way-of-work.md` — tacp config block (L2_LANG, verbosity_default)
- 11 caw-*.md → dual-block format (L3: AI-CONTEXT + HUMAN-CONTEXT)
- `new-project.sh` — bootstrap tacp.md ไปยัง new projects
- `ADR-005` — architectural decision record
- `tests/token-savings/tacp-benchmark.md` — 15 test cases, ~54% session savings
- tests: 46 → 67 (+21 TACP tests)
- VERSION: 1.4.0 → 1.5.0
- Branch: feat/savetoken — pushed

## สิ่งที่เสร็จแล้ว session ล่าสุด (2026-05-08 ต่อ)

### Docs merged to master (T-032) ✅
- docs/architecture/overview.md: Package Concept section + 3 structure diagrams
- docs/advanced-setup.md: merge workflow + CoreAiWorkspaces/ restore step
- GitHub Pages updated

### /caw-update + --update-commands (T-033) ✅
- `new-project.sh --update-commands`: อัปเดต caw-* + CLAUDE.md โดยไม่แตะ CoreAiWorkspaces/
- slash command `/caw-update`: สั่งจาก AI ได้โดยตรง
- tests: 43 → 44 tests (เพิ่ม caw-update.md ใน SLASH_FILES)

## สิ่งที่เสร็จแล้ว session นี้

### Package Install Flow (T-028) ✅
- `new-project.sh` upgrade: auto-install CLAUDE.md + `.claude/commands/` + `.git/hooks/validate-commit`
- user ลบ `_template/` ได้ทันทีหลัง bootstrap — ไม่ต้อง copy อะไรเอง

### Slash Commands — caw- prefix (T-029) ✅
- rename 10 files: `session-end.md` → `caw-session-end.md` ฯลฯ
- `caw-` = CoreAiWorkspaces abbreviation — ป้องกัน namespace collision
- อัปเดต 29 files + tests ครบ

### Documentation (T-026, T-030) ✅
- docs/ 14 files: web pages + architecture + integrations
- แก้ `claude.CoreAiWorkspaces/code` URL bugs
- ลบ manual copy steps ทุกที่ → สอน script flow แทน
- เพิ่มคำอธิบาย caw- ทุก touchpoint

### Tests (T-031) ✅
- 35 → 43 tests: เพิ่ม A8–A13 (CLAUDE.md auto-install, slash commands)
- แก้ B2/S5: docs/ tracked on dev = intentional (GitHub Pages)
- C6: chmod failure → warning (Windows NTFS limitation)

### verify-install.sh (T-027) ✅
- post-install check script: 6 sections, ตรวจทุก artifact ที่ new-project.sh สร้าง

## Next Actions

- รอ user อนุมัติ merge feat/savetoken → dev → master (v1.5.0)
- Note: `merge=ours` ใน `.gitattributes` ทำงานสองทาง — เมื่อ merge master→dev ต้อง `git checkout HEAD~1 -- CoreAiWorkspaces/` เพื่อ restore

## สถานะ Tests

**67/67 passing** — tests/functional/test-user-flows.sh

## Branch State

```
master  ← v1.4.0 (stable)
dev     ← v1.4.0 (in sync with master)
feat/savetoken ← v1.5.0 (TACP — b80cc35) — ready for merge
```
