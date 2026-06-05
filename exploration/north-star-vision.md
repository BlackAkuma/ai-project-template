# North-Star Vision — ai-project-template

**Date:** 2026-06-05
**Branch:** `explore/odysseus-analysis`
**Status:** 🧭 Directional north-star — Stage 1 = committed, Stage 2 = hypothesis (ยังไม่ผูกมัด)
**Trigger:** วิเคราะห์ Odysseus → ตกผลึกว่าโปรเจ็กต์นี้คือ "สมอง" ไม่ใช่ "ร่าง"

> เอกสารนี้คือเข็มทิศ ไม่ใช่สัญญา — กลับมาอ่าน/แก้ได้ทุกเมื่อที่ทิศเปลี่ยน

---

## ที่มา (Origin)

ระบบนี้เกิดจากข้อจำกัดของการพัฒนาโครงการผ่าน AI web

เดิมที vision เต็มคือ: **เว็บสำหรับ control การทำงาน** — ผู้พัฒนาคุยกับ AI หรือเอาเอกสารออกแบบมาแปลงเป็นโปรเจ็กต์ แล้ว control ข้าม **หลาย repo** เพื่อให้ AI เข้าใจ *ทั้งโครงการ* ไม่ว่าจะเล็ก ใหญ่ หรือหลาย repo ที่ต้องประกอบกัน — ให้การพัฒนาราบรื่น

`ai-project-template` (สิ่งที่ทำอยู่ตอนนี้) = **ส่วน context ที่จำเป็นที่สุด ที่ถอดออกมาทำก่อน**

แล้ว Odysseus โผล่มา (มีหน้าจอ) → ทำให้ "ร้อนรน" เพราะมันคือ basic capability ที่น่าจะทำได้ **แต่มันไม่มีการบริหารโครงการแบบนี้**

---

## Thesis หลัก — สิ่งที่ทุกอย่างตั้งอยู่บน

> **ความเก่งของ AI ไม่ได้อยู่ที่ตัว model อย่างเดียว — แต่อยู่ที่ context การทำงานที่เรียบเรียงมา**
>
> Model = commodity (เปลี่ยนได้ เสียบได้) · Context engineering = moat (ลอกยาก เพราะเป็นปรัชญา+วินัย)

**Odysseus พิสูจน์ thesis นี้โดยไม่ตั้งใจ:** 52k stars, MIT, ใครก็ fork ได้ → "หน้าจอ + API key + ต่อ model" คือของ commodity ไปแล้ว สิ่งที่ Odysseus *ไม่มี* คือ project/structural governance = จุดที่เราถือ moat

---

## โมเดล 3 ชั้น (สร้างจากล่างขึ้นบน)

```
┌─────────────────────────────────────────────┐
│ ชั้น 3 — SHELL (ร่าง)         [Stage 2: directional]
│ แอปแบบ Odysseus: หน้าจอ + API key +
│ model-agnostic + multi-agent รุมวิเคราะห์ +
│ multi-repo                    ← commodity, สร้างทีหลัง
├─────────────────────────────────────────────┤
│ ชั้น 2 — ENGINE (สะพาน)       [bridge: the moat]
│ governance ที่ "เครื่องบังคับ gate ได้เอง"
│ ไม่ใช่แค่ "AI ช่วยอ่าน docs"   ← machine-readable spec
├─────────────────────────────────────────────┤
│ ชั้น 1 — SUBSTRATE (สมอง)     [Stage 1: committed ✅]
│ ai-project-template ที่ใช้กับ AI tool ตัวไหนก็ได้
│                               ← ของจริงวันนี้
└─────────────────────────────────────────────┘
```

**กฎเหล็ก:** ชั้น 3 มีค่าก็ต่อเมื่อชั้น 1 แกร่ง — เพราะ value proposition ทั้งหมดของชั้น 3 *คือ* ชั้น 1
ถ้าสมองอ่อน ร่างก็เป็นแค่ Odysseus อีกตัว

---

## สิ่งที่ prototype ไว้แล้ว (endgame เวอร์ชันจิ๋ว)

โครงสร้างปัจจุบัน = เมล็ดพันธุ์ของปลายทาง:

| มีแล้ว | คือเมล็ดของ |
|--------|------------|
| `core/` (session protocol, task-board, ADR, compliance) | substrate ชั้น 1 |
| `skills/game/` | domain pack — พิสูจน์ว่า substrate รองรับงานเขียนเกม |
| `platforms/claude-code/agents/` (game-designer, art-director, ux...) | **multi-agent รุมวิเคราะห์ใน project เดียว** = Stage 2 จิ๋ว |
| slash commands (`/caw-*`) | gate engine ชั้น 2 แบบ manual |

→ เคยทำ multi-agent ในบริบทโครงการเดียวกันแล้ว — แค่ผูกกับ Claude Code ตัวเดียว
Stage 2 เพิ่มจริงแค่ 3 อย่าง: **(1) หน้าจอ (2) model-agnostic ผ่าน API key (3) multi-repo** — methodology เดิมทั้งหมด

---

## เป้าหมายปลายทาง (ตามคำผู้ใช้)

1. **เวอร์ชันนี้ (Stage 1):** template ที่เอาไปใช้กับ AI tool ตัวไหนก็ได้ — universal
2. **บั้นปลาย (Stage 2):** AI tool ของตัวเองแบบ Odysseus ที่ทำงาน *เชิงโปรเจ็กต์ เชิงโครงสร้าง* — เสียบ API key model ไหนก็ได้ มี multi-agent รุมวิเคราะห์ในบริบทโครงการเดียวกัน เอาไปใช้กับงานอะไรก็ได้ รวมถึงงานเขียนเกม

> งานเขียนเกม ≠ ผลิตภัณฑ์คนละตัว — เป็น skill pack บน substrate เดียวกัน (พิสูจน์แล้วด้วย `skills/game/`)

---

## Roadmap

| Stage | สถานะ | ทำอะไร | Done เมื่อ |
|-------|-------|--------|-----------|
| **1 — Substrate** | ✅ committed (กำลังทำ) | template ชั้น 1 ให้ "แกร่งพอเป็นของตัวเองโดยสมบูรณ์" ในฐานะ spec | ใช้กับ tool ไหนก็ได้, governance ครบ, gate ทำงาน |
| **2a — Engine** | 🔬 hypothesis | แปลง governance: markdown → machine-readable spec (เครื่องบังคับ gate) | gate enforce ได้โดยไม่พึ่งโมเดลตีความ |
| **2b — Shell** | 🔬 hypothesis | หน้าจอ + LiteLLM + multi-agent orchestration + multi-repo | เสียบ model ไหนก็ได้, รุมวิเคราะห์ใน project เดียว |

**ลำดับห้ามกลับ:** 1 → 2a → 2b เสมอ

---

## Guardrails — 3 ความเสี่ยงที่ต้องเฝ้า

**1. กับดัก "ร้อนรน" = ศัตรูตัวจริง**
Odysseus ทำให้อยากกระโดดไปชั้น 3 เลย แต่ชั้น 3 คือส่วน *ง่ายและ commodity ที่สุด*
ถ้ากลับลำดับ (สร้างร่างก่อนสมองพร้อม) → ได้ทั้งแอปครึ่งๆ และ template ครึ่งๆ
→ **สร้างร่างเป็นอันดับสุดท้าย บนสมองที่พิสูจน์แล้ว**

**2. Model-floor มีจริง**
thesis "context > model" ถูก *แต่มีพื้น* — โมเดลอ่อนไม่เคารพ gate
พอเปิด "เสียบ model ไหนก็ได้" จะเจอ user เอาโมเดลจิ๋วมาเสียบ → governance กลายเป็นละคร
→ ชั้น 2 ต้อง **บังคับด้วยเครื่อง** ไม่ใช่ขอร้องโมเดล

**3. "universal" vs "tool ของตัวเอง" มีแรงตึง**
ถ้า Stage 2 เจ๋ง คนจะยังอยากเป็นกลางทำไม? ถ้า optimize template เพื่อ tool ตัวเอง มันเลิก universal
→ วันหนึ่งอาจต้องเลือก — **แต่ยังไม่ใช่ตอนนี้** เก็บ Stage 1 ให้ universal ไว้ก่อน

---

## ประโยคเดียวที่สรุปทั้งหมด

> **เรากำลังสร้าง "สมอง" ที่ทำให้ AI ตัวไหนก็ทำงานเชิงโครงการได้ดีขึ้น —
> ไม่ใช่ "ร่าง" อีกตัวที่แข่งกับ Odysseus
> ร่างค่อยสร้างทีหลัง เมื่อสมองพิสูจน์ตัวเองแล้ว**

---

*บันทึกจาก session วิเคราะห์ Odysseus — คู่กับ `exploration/odysseus-analysis.md`*
*Promote เป็น `VISION.md` ที่ root เมื่อ merge ถ้าตัดสินใจ commit ทิศนี้*
