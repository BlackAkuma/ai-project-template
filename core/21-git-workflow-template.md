# Git Workflow Template

**นี่คือ Core Principle** — AI ต้องอ่านและปฏิบัติตามทุก session
ความสำคัญเทียบเท่า session protocol และ decision protocol

---

## หลักการหลัก (ห้ามละเมิด)

**`CoreAiWorkspaces/` และ `CLAUDE.md` ต้องไม่อยู่บน production branch**

เหตุผล:
- production deploy ควรมีเฉพาะ code ที่ใช้งานจริง
- AI working files (CoreAiWorkspaces/) ไม่ควร expose ใน production environment
- ถ้า repo เป็น public: planning docs / ADR / session logs ไม่ควรมองเห็น

---

## Branch Strategy (แนะนำ)

```
[production branch]   ← code เท่านั้น — deploy จาก branch นี้
      ↑ merge code only
[dev branch]          ← code + CoreAiWorkspaces/ + CLAUDE.md — ทำงาน AI ที่นี่
      ↑ branch off
[feature/* branches]  ← optional
```

**กฎ:**
- `CoreAiWorkspaces/` อยู่บน dev branch เสมอ
- merge dev → production = **merge code เท่านั้น** ไม่เอา `CoreAiWorkspaces/` ขึ้น
- production branch ชื่ออะไรก็ได้ (main / master / release / prod)
- dev branch ชื่ออะไรก็ได้ — AI ต้องถามและบันทึกไว้

---

## Feature Branch Workflow

### กฎ 9 ข้อ (บังคับ)

| # | กฎ | AI ทำ |
|---|----|----|
| 1 | เริ่มจาก dev เสมอ | ตรวจ branch ก่อนทุกครั้ง — ถ้าไม่ใช่ dev ให้แจ้งก่อน |
| 2 | งานใหม่ / bug / feature → แยก branch จาก dev **ก่อนแตะโค้ด** | `git checkout dev && git checkout -b feature/<task-id>-<name>` |
| 3 | เฉพาะงานใหญ่เท่านั้นที่ต้องแยก (ดูเกณฑ์ด้านล่าง) | งานเล็กขอบเขตชัด → ทำบน dev ได้ตรง |
| 4 | ทำงาน → commit → push บน feature branch | checkpoint ทุก task สำคัญ |
| 5 | เทสครบ → merge กลับ dev → ลบ feature branch | ยืนยันกับ user ก่อนลบ |
| 6 | ถ้ามี feature branch ค้างอยู่ → ห้ามแตก branch ใหม่ | ตรวจ `git branch --list` ก่อนสร้างใหม่ |
| 7 | หลัง merge กลับ dev → **รอ user สั่ง** ว่าจะ promote ขั้นไหน | ไม่ promote เอง ไม่มีข้อยกเว้น |
| 8 | บางโปรเจ็กต์ไม่มี SIT/UAT → user สั่งขึ้น main/prod ตรงได้ | ปฏิบัติตามคำสั่ง user |
| 9 | ห้าม session จบโดยไม่ commit + push | Session End Protocol push เสมอ |

---

### เมื่อไหร่ต้องแยก Branch

**ต้องแยก branch เสมอ (งานใหญ่):**
- Feature ใหม่ (คาดว่า > 1 commit)
- Architecture change หรือ refactor หลายไฟล์
- งาน ADR-level (ต้องสร้าง ADR ก่อน implement)
- Cross-module change

**ทำบน dev ตรงได้ (งานเล็ก):**
- Bug fix 1 จุด ขอบเขตชัดเจน
- Doc edit / comment fix
- Trivial cleanup / polish

> **ถ้าไม่แน่ใจว่าใหญ่หรือเล็ก → แยก branch ไว้ก่อน ปลอดภัยกว่า**

---

### Branch Naming Convention

```
feature/<task-id>-<short-name>    เช่น  feature/T-012-payment-integration
fix/<task-id>-<short-name>        เช่น  fix/T-034-login-redirect
chore/<short-name>                เช่น  chore/upgrade-deps
```

---

### Promotion Pipeline

AI ต้องถามตอน bootstrap ว่าโปรเจ็กต์ใช้ pipeline แบบไหน และบันทึกใน work-status:

**Pipeline มี SIT/UAT:**
```
feature/* → dev → SIT → UAT → main/prod
```

**Pipeline ไม่มี SIT/UAT:**
```
feature/* → dev → main/prod
```

AI รอ user สั่งทุกขั้นของ promotion — ไม่ promote เอง

---

### Scenario: Feature Branch ค้างอยู่

ถ้า user ขอสร้าง branch ใหม่ แต่ยังมี feature branch ค้างอยู่:

```
ตรวจ: git branch --list "feature/*" "fix/*"
พบ: feature/T-012-payment-integration (ยังไม่ merge)

แจ้งผู้ใช้:
"มี branch ค้างอยู่: feature/T-012-payment-integration
ตาม workflow ต้องทำ branch นี้ให้จบก่อน

เลือก:
A) ทำ feature/T-012 ให้จบก่อน (แนะนำ)
B) สร้าง branch ใหม่ต่อไป — รับทราบว่ามี branch ค้าง"
```

รอคำตอบก่อนดำเนินการต่อ

---

### Session End — Feature Branch Checklist

```
□ commit + push ทุก branch ที่กำลังทำงานอยู่ (ห้ามจบ session โดยไม่ push)
□ ถ้า feature เสร็จแล้ว → merge กลับ dev + ลบ feature branch (ถ้า user ยืนยัน)
□ ไม่ promote dev → SIT/UAT/prod ถ้า user ไม่ได้สั่ง
```

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

**สัญญาณ:** `git branch --show-current` คืนค่า main หรือ master และยังไม่มี `CoreAiWorkspaces/`

**AI แจ้งผู้ใช้:**
```
คุณอยู่บน [branch] ซึ่งเป็น production branch
แนะนำให้สร้าง dev branch ก่อน bootstrap เพื่อแยก AI files ออกจาก production

เลือก:
A) สร้าง dev branch ทันที (แนะนำ)
   → git checkout -b dev
   → bootstrap และ CoreAiWorkspaces/ ทั้งหมดจะอยู่บน dev

B) ทำต่อบน [branch] นี้ (single-branch mode)
   → CoreAiWorkspaces/ จะอยู่บน production branch
   → ต้อง exclude CoreAiWorkspaces/ เองตอน deploy
   → AI จะเตือนทุกครั้งที่ commit CoreAiWorkspaces/ ลงบน branch นี้
```

**ผู้ใช้เลือก A:**
```bash
git checkout -b dev
```
→ bootstrap ปกติ บันทึก git_prod_branch: main, git_dev_branch: dev, git_mode: branch-separated

**ผู้ใช้เลือก B:**
→ bootstrap ต่อบน main บันทึก git_mode: single-branch
→ สร้าง `.deployignore` ให้อัตโนมัติ (ดูด้านล่าง)
→ เตือนทุกครั้งที่ session end ว่า "CoreAiWorkspaces/ อยู่บน production branch — exclude ตอน deploy"

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

**ถ้า remote ไม่มี (CoreAiWorkspaces/ หายจริง):**
- code ยังอยู่ครบบน production branch ✓
- CoreAiWorkspaces/ หาย แต่ code และ git history ยังอยู่ครบ
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
**กฎยังเหมือนเดิม:** CoreAiWorkspaces/ อยู่บน dev_branch เท่านั้น ไม่ขึ้น prod_branch

---

### Scenario 4 — Solo developer ต้องการ single branch

**สัญญาณ:** ผู้ใช้เลือก B ใน Scenario 1 หรือระบุว่า "ไม่ต้องการแยก branch"

**AI ทำ:**
1. ยอมรับและทำงานต่อได้ ไม่ต้อง force แยก branch
2. บันทึก `git_mode: single-branch` ใน work-status
3. สร้าง `.deployignore` อัตโนมัติ:
```
CoreAiWorkspaces/
CLAUDE.md
*.lance
ai-workspace/
```
4. เตือนทุกสิ้น session:
```
[REMINDER] git_mode: single-branch
CoreAiWorkspaces/ อยู่บน production branch — ตอน deploy ต้อง exclude CoreAiWorkspaces/ และ CLAUDE.md
```

---

### Scenario 5 — CoreAiWorkspaces/ มีอยู่บน production branch แล้ว ต้องการย้ายไป dev

**สัญญาณ:** เริ่มใช้ระบบใหม่กับโปรเจ็กต์ที่ทำงานบน main อยู่แล้ว หรือ bootstrap ผ่านไปแล้วโดยไม่ได้แยก branch

**AI ต้องทำ (ขอ permission ผู้ใช้ก่อนทุกขั้น):**

```bash
# ขั้น 1: สร้าง dev branch จาก main (เพื่อให้ dev มี CoreAiWorkspaces/ ครบ)
git checkout main
git checkout -b dev
# ตอนนี้ dev มี CoreAiWorkspaces/ ครบแล้ว ✓

# ขั้น 2: ลบ CoreAiWorkspaces/ ออกจาก main
git checkout main
git rm -r --cached CoreAiWorkspaces/ CLAUDE.md
echo "CoreAiWorkspaces/" >> .gitignore
echo "CLAUDE.md" >> .gitignore
git add .gitignore
git commit -m "chore: move AI working files to dev branch only"

# ขั้น 3: ยืนยัน
git checkout main && ls doc  # ควร error — CoreAiWorkspaces/ ไม่ควรอยู่บน main
git checkout dev && ls doc   # ควรเห็น CoreAiWorkspaces/ ครบ
```

**หลังจากนั้น:**
- อัปเดต work-status git fields: `git_prod_branch: main`, `git_dev_branch: dev`, `git_mode: branch-separated`
- ทำงานบน dev ต่อไปตามปกติ

**ข้อควรระวัง:** ขั้น 2 เป็น destructive กับ main history — ยืนยันกับผู้ใช้ก่อนรัน และ push ต่อเมื่อผู้ใช้ยืนยันเท่านั้น

---

## Merge Policy: dev → production branch

**merge ขึ้น production:**
- ✅ source code, build files, configs
- ✅ package.json, requirements.txt, Dockerfile
- ✅ README.md (ถ้าต้องการ)
- ❌ `CoreAiWorkspaces/` — ห้าม merge ขึ้น production
- ❌ `CLAUDE.md` — ห้าม merge
- ❌ `CoreAiWorkspaces/08-vector-index/` — อยู่ใน .gitignore อยู่แล้ว

**วิธี merge ที่ถูกต้อง (เลือกหนึ่ง):**

```bash
# Option A: merge แล้ว unstage CoreAiWorkspaces/ (clean)
# ⚠️ ต้องอยู่บน prod-branch ก่อนรัน git rm — ตรวจก่อนเสมอ
git checkout [prod-branch]
git branch --show-current  # ยืนยันว่าอยู่บน prod-branch จริง
git merge dev --no-ff
git rm -r --cached CoreAiWorkspaces/ CLAUDE.md
git commit -m "chore: exclude AI working files from production"

# Option B: cherry-pick เฉพาะ code commits
git checkout [prod-branch]
git cherry-pick [commit] [commit] ...

# Option C: PR/MR — reviewer ต้อง exclude CoreAiWorkspaces/ ก่อน approve
```

---

## .gitignore ที่ต้องมีในทุกโปรเจ็กต์

```gitignore
# AI Vector Index (rebuilt from CoreAiWorkspaces/ automatically)
CoreAiWorkspaces/08-vector-index/
*.lance

# AI Workspace (cross-project memory, outside project repo)
ai-workspace/
```

---

## บันทึกใน work-status AI-CONTEXT Block

ทุกโปรเจ็กต์ต้องมีใน AI-CONTEXT block:

```yaml
git_prod_branch: main          # branch ที่ deploy — ห้าม commit CoreAiWorkspaces/ ที่นี่
git_dev_branch: dev            # branch ที่ AI ทำงาน — CoreAiWorkspaces/ อยู่ที่นี่
git_mode: branch-separated     # หรือ single-branch
git_pipeline: dev->main        # หรือ dev->sit->uat->main ตามโปรเจ็กต์
```

**AI อ่าน field นี้ทุก session start** — ถ้าไม่มี field นี้ใน work-status ให้ถามผู้ใช้และเพิ่มทันที

---

## Session End — Git Checklist เพิ่มเติม

เพิ่มใน session end checklist ของทุกโปรเจ็กต์ที่ใช้ branch-separated mode:

```
□ git push origin [dev_branch]   ← push CoreAiWorkspaces/ ขึ้น remote ป้องกัน data loss
□ ไม่มี CoreAiWorkspaces/ หรือ CLAUDE.md หลุดไป commit บน [prod_branch]
```

---

## สิ่งที่ AI ต้องไม่ทำ (เกี่ยวกับ git)

- ❌ commit `CoreAiWorkspaces/` หรือ `CLAUDE.md` ลงบน production branch — **ห้ามเด็ดขาด ไม่มีข้อยกเว้น ไม่ว่าผู้ใช้จะขอแค่ไหน**
- ❌ merge `CoreAiWorkspaces/` หรือ `CLAUDE.md` ขึ้น production branch — ใช้ Option B หรือ C แทน
- ❌ ข้าม branch check ตอน bootstrap — ไม่มีข้อยกเว้น
- ❌ รัน `git rm -r --cached CoreAiWorkspaces/` บน dev branch — ต้องอยู่บน prod-branch เท่านั้น
- ❌ ลบ branch ใดๆ โดยไม่ได้รับคำสั่งชัดเจนจากผู้ใช้
- ❌ force push ใดๆ โดยไม่ได้รับคำสั่งชัดเจนจากผู้ใช้
- ❌ สร้าง branch ใหม่โดยไม่แจ้งผู้ใช้ก่อน (ยกเว้นเฉพาะ dev branch หลังผู้ใช้เลือก A ใน Scenario 1)
- ❌ สร้าง feature branch ใหม่โดยไม่ตรวจว่ามี branch ค้างอยู่ก่อน
- ❌ promote dev → SIT/UAT/prod โดยไม่ได้รับคำสั่งจาก user — รอสั่งทุกขั้น
- ❌ จบ session โดยไม่ commit + push บน branch ที่กำลังทำงาน
