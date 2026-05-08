<!-- AI-CONTEXT
phase: maintenance
active_task: none
blocker: none
last_updated: 2026-05-08
git_mode: branch-separated
git_dev_branch: dev
git_prod_branch: master
read_more:
  plan: CoreAiWorkspaces/01-plan/project-plan.md
  decisions: CoreAiWorkspaces/07-decisions/README.md
  roadmap: ROADMAP.md
-->

# Work Status — ai-project-template

อัปเดตล่าสุด: 2026-05-08

## สถานะปัจจุบัน

**Phase:** maintenance — v1.3.0 released ✅
**Active Task:** none
**Blocker:** none

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

- ระบบ stable — รอ feature request ถัดไป
- Note: `merge=ours` ใน `.gitattributes` ทำงานสองทาง — เมื่อ merge master→dev ต้อง `git checkout HEAD~1 -- CoreAiWorkspaces/` เพื่อ restore

## สถานะ Tests

**43/43 passing** — tests/functional/test-user-flows.sh

## Branch State

```
master  ← v1.2.0 (09fe310) — stable package
dev     ← v1.3.0-rc (193de20) — 7 commits ahead
```
