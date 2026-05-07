<!-- AI-CONTEXT
last_session: 2026-05-07
tool: Claude Code
completed: [T-010,T-011,T-012,T-013,T-014,bootstrap-ai]
checkpoint: none
next_from_last: update ROADMAP + CHANGELOG (T-020, T-021)
notes: structural restructure complete + ai/ bootstrapped
deep_context: none
-->

# Work Log Index — ai-project-template

## Milestone Summary

| Milestone | Status | Completed |
|-----------|--------|-----------|
| M1: Core Template System (core/ 00–21, skills, platforms) | ✅ done | 2026-05 |
| M2: Structural Integrity (doc→ai, gh-pages, clone fix, tests) | ✅ done | 2026-05-07 |
| M3: Release Prep (ROADMAP, CHANGELOG, merge to master) | 🔄 todo | — |

## Recent Sessions

### 2026-05-07 — [Structural Restructure + MemPalace + ai/ Bootstrap]

**สิ่งที่ทำ:**
- ออกแบบและเขียน core/20-vector-memory-optional.md (MemPalace Phase 3 template)
- เขียน tools/vector-memory/README.md (quick reference)
- อัปเดต core/19-memory-architecture-overview.md (Layer 4 + compliance C-20/21/22)
- Rename doc/ → ai/ ครบทุกไฟล์ (101 files, 589 occurrences) บน branch `restructure/doc-to-ai`
- ย้าย docs/ web pages ไป gh-pages branch (orphaned)
- สร้าง CLAUDE.md ที่ repo root — fix clone flow ที่ broken
- สร้าง tests/functional/test-user-flows.sh (35 tests, Flow A/B/C + Structural)
- Fix test S5 ให้ใช้ `git ls-files` แทน filesystem check
- Merge restructure/doc-to-ai → dev, push both dev + gh-pages
- Bootstrap ai/ สำหรับ template project นี้เอง (meta-bootstrap)

**ผล:** 35/35 tests passing, dev branch clean + pushed

**Next:** T-020 (ROADMAP), T-021 (CHANGELOG), T-023 (merge to master เมื่อพร้อม)

---

### ก่อนหน้า 2026-05-07 — [Core Template Development]

**สรุป:** พัฒนา core/ templates 00–21 ทั้งหมด รวมถึง:
- Session protocol, task lifecycle, compliance, ADR system
- Memory architecture Phase 1–2 (entity register, cross-project memory, agent diary)
- Git workflow template (core/21)
- skills/game/ (00–11)
- Web pages (how-it-works.html, workflow-diagram.html) สำหรับ GitHub Pages
- Functional tests สำหรับ reader scripts

**Decisions:**
- เลือก MemPalace เป็น Phase 3 vector memory implementation (local-first, ไม่ต้อง cloud)
- เปลี่ยนชื่อ doc/ → ai/ เพื่อความชัดเจน (ไม่ชน docs/ folder)
- แยก docs/ ไป gh-pages branch — user project ไม่ได้รับ web pages เมื่อ clone
