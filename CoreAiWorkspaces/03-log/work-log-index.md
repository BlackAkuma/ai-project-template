<!-- AI-CONTEXT
last_session: 2026-05-08
tool: Claude Code
completed: [T-023,T-024,T-025,T-026,T-027,T-028,T-029,T-030,T-031,T-032,T-033]
checkpoint: none
next_from_last: none — ระบบ stable รอ feature request ถัดไป
notes: v1.3.0 released on master. /caw-update + --update-commands added.
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

### 2026-05-08 — [v1.3.0 Release + /caw-update]

**สิ่งที่ทำ:**
- Merge dev → master: v1.3.0 (caw- prefix, package install flow, docs)
- Merge docs: Package Concept diagrams + merge workflow notes → master → GitHub Pages live
- feat: `--update-commands` flag ใน new-project.sh — อัปเดต commands ไม่แตะ CoreAiWorkspaces/
- feat: `/caw-update` slash command — สั่งอัปเดตจาก AI ได้โดยตรง
- tests: 43 → 44 (เพิ่ม caw-update.md ใน SLASH_FILES check)
- อัปเดต platforms/claude-code/README.md + CLAUDE.md ให้รู้จัก /caw-update

**ผล:** 44/44 tests passing, dev pushed, ระบบ stable
**Next:** รอ feature request ถัดไป

---


### 2026-05-07 — [Structural Restructure + MemPalace + CoreAiWorkspaces/ Bootstrap]

**สิ่งที่ทำ:**
- ออกแบบและเขียน core/20-vector-memory-optional.md (MemPalace Phase 3 template)
- เขียน tools/vector-memory/README.md (quick reference)
- อัปเดต core/19-memory-architecture-overview.md (Layer 4 + compliance C-20/21/22)
- Rename doc/ → CoreAiWorkspaces/ ครบทุกไฟล์ (101 files, 589 occurrences) บน branch `restructure/doc-to-ai`
- ย้าย docs/ web pages ไป gh-pages branch (orphaned)
- สร้าง CLAUDE.md ที่ repo root — fix clone flow ที่ broken
- สร้าง tests/functional/test-user-flows.sh (35 tests, Flow A/B/C + Structural)
- Fix test S5 ให้ใช้ `git ls-files` แทน filesystem check
- Merge restructure/doc-to-ai → dev, push both dev + gh-pages
- Bootstrap CoreAiWorkspaces/ สำหรับ template project นี้เอง (meta-bootstrap)

**ผล:** 35/35 tests passing, dev branch clean + pushed

**Next:** T-023 (merge dev → master รอ permission)

---

### 2026-05-08 — [T-022: MemPalace Field Test + Doc Corrections]

**สิ่งที่ทำ:**
- ติดตั้ง mempalace 3.3.4 จริง และ test บน template project's CoreAiWorkspaces/ folder
- พบ 4 ข้อผิดพลาดในเอกสาร แก้ไขทั้งหมด:
  1. `init` command — เป็น interactive wizard ไม่ใช่ path command / ข้ามได้
  2. Palace location — `~/.mempalace/palace` (global) ไม่ใช่ `~/ai-workspace/mempalace/`
  3. `--wing` flag — ต้องระบุเสมอเมื่อ mine จาก `CoreAiWorkspaces/` subfolder (ไม่งั้น wing = 'ai')
  4. Threshold — 0.60 → 0.35 สำหรับ Thai/mixed (จาก actual cosine scores 0.31–0.53)
- ค้นพบ `mempalace wake-up`, `mempalace status` commands ที่ไม่ได้เขียนไว้
- Mine 22 files, 62 drawers สำเร็จ / Search ทำงานได้ถูกต้อง
- อัปเดต core/20, core/19, tools/vector-memory/README.md

**ผล:** T-022 complete — docs ถูกต้องแล้ว

---

### 2026-05-08 — [ROADMAP + CHANGELOG + Release Prep]

**สิ่งที่ทำ:**
- อัปเดต ROADMAP.md — Phase 3 Semantic Search Layer เปลี่ยนจาก "planned" เป็น "✅ template done"
- อัปเดต CHANGELOG.md — เพิ่ม v1.1.0 (memory architecture Phase 1–3) และ v1.2.0 (structural integrity)
- อัปเดต task-board.md — T-020/021 done, T-022 (field test) คือ next

**ผล:** ROADMAP ตรงกับ reality, CHANGELOG บันทึกครบ, งานเหลือ T-022 + T-023

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
- เปลี่ยนชื่อ doc/ → CoreAiWorkspaces/ เพื่อความชัดเจน (ไม่ชน docs/ folder)
- แยก docs/ ไป gh-pages branch — user project ไม่ได้รับ web pages เมื่อ clone
