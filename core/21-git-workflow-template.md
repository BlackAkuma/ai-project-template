# Git Workflow Template

**นี่คือ Core Principle** — AI ต้องอ่านและปฏิบัติตามทุก session
ความสำคัญเทียบเท่า session protocol และ decision protocol

---

## หลักการหลัก (ห้ามละเมิด)

**`doc/` และ `CLAUDE.md` ต้องไม่อยู่บน production branch**

เหตุผล:
- production deploy ควรมีเฉพาะ code ที่ใช้งานจริง
- AI working files (doc/) ไม่ควร expose ใน production environment
- ถ้า repo เป็น public: planning docs / ADR / session logs ไม่ควรมองเห็น

---

## Branch Strategy (แนะนำ)

```
[production branch]   ← code เท่านั้น — deploy จาก branch นี้
      ↑ merge code only
[dev branch]          ← code + doc/ + CLAUDE.md — ทำงาน AI ที่นี่
      ↑ branch off
[feature/* branches]  ← optional
```

**กฎ:**
- `doc/` อยู่บน dev branch เสมอ
- merge dev → production = **merge code เท่านั้น** ไม่เอา `doc/` ขึ้น
- production branch ชื่ออะไรก็ได้ (main / master / release / prod)
- dev branch ชื่ออะไรก็ได้ — AI ต้องถามและบันทึกไว้

---

## AI ต้องทำ: Branch Check ก่อน Bootstrap

**ทำก่อนขั้นตอนอื่นทั้งหมด — ก่อนถามภาษา ก่อนสร้างไฟล์ใดๆ**

```
1. ตรวจ branch ปัจจุบัน: git branch --show-current
2. ถ้าอยู่บน production branch → ไปที่ Scenario 1
3. ถ้าอยู่บน dev/non-production branch → proceed ได้เลย
4. บันทึก git_prod_branch + git_dev_branch ใน work-status AI-CONTEXT block
```

---

## Scenarios

### Scenario 1 — เริ่มโปรเจ็กต์ใหม่บน production branch (main/master)

**สัญญาณ:** `git branch --show-current` คืนค่า main หรือ master และยังไม่มี `doc/`

**AI แจ้งผู้ใช้:**
```
คุณอยู่บน [branch] ซึ่งเป็น production branch
แนะนำให้สร้าง dev branch ก่อน bootstrap เพื่อแยก AI files ออกจาก production

เลือก:
A) สร้าง dev branch ทันที (แนะนำ)
   → git checkout -b dev
   → bootstrap และ doc/ ทั้งหมดจะอยู่บน dev

B) ทำต่อบน [branch] นี้ (single-branch mode)
   → doc/ จะอยู่บน production branch
   → ต้อง exclude doc/ เองตอน deploy
   → AI จะเตือนทุกครั้งที่ commit doc/ ลงบน branch นี้
```

**ผู้ใช้เลือก A:**
```bash
git checkout -b dev
```
→ bootstrap ปกติ บันทึก git_prod_branch: main, git_dev_branch: dev, git_mode: branch-separated

**ผู้ใช้เลือก B:**
→ bootstrap ต่อบน main บันทึก git_mode: single-branch
→ สร้าง `.deployignore` ให้อัตโนมัติ (ดูด้านล่าง)
→ เตือนทุกครั้งที่ session end ว่า "doc/ อยู่บน production branch — exclude ตอน deploy"

---

### Scenario 2 — dev branch ถูกลบโดยไม่ตั้งใจ

**สัญญาณ:** ไม่มี dev branch, มีแค่ production branch พร้อม code

**ตรวจสอบก่อน:**
```bash
git branch -a                      # remote ยังมี dev ไหม?
git reflog | grep dev              # มี commit ล่าสุดของ dev ไหม?
```

**ถ้า remote ยังมี dev:**
```bash
git checkout -b dev origin/dev     # restore ได้เลย ไม่มีอะไรหาย
```

**ถ้า remote ไม่มี (doc/ หายจริง):**
- code ยังอยู่ครบบน production branch ✓
- doc/ หาย แต่ code และ git history ยังอยู่ครบ
- ต้อง bootstrap ใหม่: AI อ่าน code + git log เพื่อ reconstruct context เท่าที่ทำได้
- สิ่งที่สร้างใหม่ไม่ได้: session logs และ ADR history ที่ไม่เคย commit

**ป้องกัน:** push dev ขึ้น remote ทุกสิ้น session (เพิ่มใน session end checklist)
```bash
git push origin dev
```

---

### Scenario 3 — โปรเจ็กต์มี branch structure ของตัวเอง

**สัญญาณ:** โปรเจ็กต์ใช้ develop / release / staging / หรือชื่ออื่น

**AI ถามตอน bootstrap:**
```
production branch ของโปรเจ็กต์คืออะไร? (branch ที่ deploy จริง)
development branch ที่ AI จะทำงานคืออะไร?
```

บันทึกคำตอบใน work-status AI-CONTEXT block ทันที
**กฎยังเหมือนเดิม:** doc/ อยู่บน dev_branch เท่านั้น ไม่ขึ้น prod_branch

---

### Scenario 4 — Solo developer ต้องการ single branch

**สัญญาณ:** ผู้ใช้เลือก B ใน Scenario 1 หรือระบุว่า "ไม่ต้องการแยก branch"

**AI ทำ:**
1. ยอมรับและทำงานต่อได้ ไม่ต้อง force แยก branch
2. บันทึก `git_mode: single-branch` ใน work-status
3. สร้าง `.deployignore` อัตโนมัติ:
```
doc/
CLAUDE.md
*.lance
ai-workspace/
```
4. เตือนทุกสิ้น session:
```
[REMINDER] git_mode: single-branch
doc/ อยู่บน production branch — ตอน deploy ต้อง exclude doc/ และ CLAUDE.md
```

---

## Merge Policy: dev → production branch

**merge ขึ้น production:**
- ✅ source code, build files, configs
- ✅ package.json, requirements.txt, Dockerfile
- ✅ README.md (ถ้าต้องการ)
- ❌ `doc/` — ห้าม merge ขึ้น production
- ❌ `CLAUDE.md` — ห้าม merge
- ❌ `doc/08-vector-index/` — อยู่ใน .gitignore อยู่แล้ว

**วิธี merge ที่ถูกต้อง (เลือกหนึ่ง):**

```bash
# Option A: merge แล้ว unstage doc/ (clean)
git checkout [prod-branch]
git merge dev --no-ff
git rm -r --cached doc/ CLAUDE.md 2>/dev/null || true
git commit -m "chore: exclude AI working files from production"

# Option B: cherry-pick เฉพาะ code commits
git checkout [prod-branch]
git cherry-pick [commit] [commit] ...

# Option C: PR/MR — reviewer ต้อง exclude doc/ ก่อน approve
```

---

## .gitignore ที่ต้องมีในทุกโปรเจ็กต์

```gitignore
# AI Vector Index (rebuilt from doc/ automatically)
doc/08-vector-index/
*.lance

# AI Workspace (cross-project memory, outside project repo)
ai-workspace/
```

---

## บันทึกใน work-status AI-CONTEXT Block

ทุกโปรเจ็กต์ต้องมีใน AI-CONTEXT block:

```yaml
git_prod_branch: main          # branch ที่ deploy — ห้าม commit doc/ ที่นี่
git_dev_branch: dev            # branch ที่ AI ทำงาน — doc/ อยู่ที่นี่
git_mode: branch-separated     # หรือ single-branch
```

**AI อ่าน field นี้ทุก session start** — ถ้าไม่มี field นี้ใน work-status ให้ถามผู้ใช้และเพิ่มทันที

---

## Session End — Git Checklist เพิ่มเติม

เพิ่มใน session end checklist ของทุกโปรเจ็กต์ที่ใช้ branch-separated mode:

```
□ git push origin [dev_branch]   ← push doc/ ขึ้น remote ป้องกัน data loss
□ ไม่มี doc/ หรือ CLAUDE.md หลุดไป commit บน [prod_branch]
```

---

## สิ่งที่ AI ต้องไม่ทำ (เกี่ยวกับ git)

- ❌ commit doc/ ลงบน production branch โดยไม่แจ้งผู้ใช้
- ❌ merge CLAUDE.md ขึ้น production branch
- ❌ ข้าม branch check ตอน bootstrap
- ❌ ลบ branch ใดๆ โดยไม่ได้รับคำสั่งชัดเจน
- ❌ force push ใดๆ โดยไม่ได้รับคำสั่งชัดเจน
- ❌ สร้าง branch ใหม่โดยไม่แจ้งผู้ใช้ก่อน (ยกเว้น dev branch ตอนผู้ใช้เลือก A)
