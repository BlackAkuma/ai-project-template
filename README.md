# AI Project Template

ชุด template สำหรับวางโครงสร้างการทำงานร่วมกันระหว่าง **นักพัฒนา** และ **AI** ในโปรเจ็กต์ซอฟต์แวร์

---

## ทำไมถึงสร้างสิ่งนี้ขึ้นมา

การทำงานกับ AI หลาย session บนโปรเจ็กต์เดียวกันมักเจอปัญหาเหล่านี้:

- **AI ไม่รู้ว่าทำอะไรไปแล้ว** — ทุก session เริ่มใหม่จากศูนย์ ทำงานซ้ำหรือข้ามสิ่งสำคัญ
- **Requirement เปลี่ยนโดยไม่มีร่องรอย** — ไม่รู้ว่าเปลี่ยนเมื่อไหร่ ทำไม และใครตัดสินใจ
- **AI ตัดสินใจเองในสิ่งที่ไม่ควร** — หรือหยุดชะงักในสิ่งที่ควรตัดสินใจได้เอง
- **หลายคนทำงานไม่ไปทิศทางเดียวกัน** — แต่ละคนใช้ AI คนละแบบ ได้ผลลัพธ์ไม่สอดคล้องกัน

Template ชุดนี้แก้ปัญหาเหล่านั้นด้วยโครงสร้างที่ชัดเจนและ protocol ที่ AI ทุกตัวสามารถทำตามได้

---

## ข้อดีที่ได้จากการใช้

- **Session ต่อกันได้ไม่สะดุด** — AI ใหม่อ่าน status แล้วรู้ทันทีว่าต้องทำอะไรต่อ
- **Requirements ไม่สูญหาย** — source docs เป็น versioned immutable records
- **ทุก task มีที่มา** — traceability จาก task กลับไปถึง requirement จริง
- **AI รู้ขอบเขตตัวเอง** — protocol ชัดเจนว่าตัดสินใจอะไรได้เอง อะไรต้องรอมนุษย์
- **ทีมหลายคนทำงานไปทิศทางเดียวกัน** — ทุกคนยึด template เดียวกัน AI ทุกตัวทำงานตาม standard เดียวกัน
- **ตรวจสอบ code quality อัตโนมัติ** — compliance check ทำงานทุก session จับ violation ก่อนสะสม
- **ใช้ได้กับทุกประเภทโปรเจ็กต์** — app, web, game, mobile ใช้ได้หมด ไม่ผูกกับ stack ใด

---

## วิธีใช้งานเบื้องต้น

### 1. Clone หรือ Download โฟลเดอร์นี้

```bash
git clone https://github.com/BlackAkuma/ai-project-template.git
```

### 2. เตรียมข้อมูลโปรเจ็กต์ใหม่ของคุณ

| ข้อมูล | ตัวอย่าง |
|--------|---------|
| ชื่อโปรเจ็กต์ | `my-app` |
| path ที่จะสร้าง `doc/` | `/projects/my-app` |
| source docs | ไฟล์ PRD / spec (ถ้ายังไม่มีพิมพ์ว่า "ยังไม่มี") |
| เป้าหมายสั้น ๆ | "แอปจองคิวออนไลน์" |

### 3. Copy prompt นี้ให้ AI

```
คุณกำลังจะ setup ระบบเอกสารสำหรับโปรเจ็กต์ใหม่

ข้อมูลโปรเจ็กต์:
- ชื่อ: [PROJECT_NAME]
- Path ที่จะสร้าง doc/: [PROJECT_ROOT_PATH]
- Source docs: [แนบไฟล์มาด้วย / ยังไม่มี]
- เป้าหมาย: [PROJECT_GOAL_SUMMARY]

ข้อกำหนด:
- ถามฉันก่อนว่าจะสื่อสารกันเป็นภาษาอะไร
- กระบวนการคิดภายใน: ใช้ภาษาอังกฤษเพื่อประหยัด token
- AI-CONTEXT block ในไฟล์: ใช้ภาษาอังกฤษเสมอ
- output และเอกสาร: ใช้ภาษาที่ตกลงกัน

ขั้นตอน:
1. ถามภาษาที่จะใช้สื่อสาร รอคำตอบก่อน
2. อ่านไฟล์ทุกไฟล์ในโฟลเดอร์ template นี้ตามลำดับใน README.md
3. สร้างโครงสร้าง doc/ ที่ path ด้านบน
4. กรอกข้อมูลโปรเจ็กต์ที่มี ถ้าไม่พอให้ใส่ placeholder ชัดเจน ห้ามเดา
5. ตรวจสอบกับ 10-bootstrap-checklist-template.md ก่อนประกาศว่าเสร็จ
```

### 4. รอ AI ทำงาน แล้วลบโฟลเดอร์ template นี้ทิ้ง

เมื่อ AI รายงานว่าผ่าน checklist แล้ว โฟลเดอร์นี้ลบทิ้งได้เลย — `doc/` ในโปรเจ็กต์ของคุณคือสิ่งที่เหลือไว้

> ดูรายละเอียดเพิ่มเติมใน [QUICKSTART.md](QUICKSTART.md)

---

## Template ที่มีในชุดนี้

| ไฟล์ | หน้าที่ |
|------|--------|
| `00` Bootstrap Master | ภาพรวม rules และขั้นตอน setup |
| `01` Folder Structure | โครงสร้างโฟลเดอร์มาตรฐาน |
| `02` Source Doc Versioning | การจัดการ requirements แบบ versioned |
| `03` Way of Work | กติกา session protocol และ language policy |
| `04` Coding Standards | มาตรฐาน code และ workflow |
| `05` Project Plan | template แผนโปรเจ็กต์ + quality gates |
| `06` Work Status | สถานะโปรเจ็กต์ พร้อม AI-CONTEXT block |
| `07` Task Board | จัดการ task พร้อม AI-CONTEXT block |
| `08` Log & Summary | บันทึก session และ summary รายวัน/เดือน |
| `09` Extension Doc | เอกสารขยายที่ไม่ใช่ source doc |
| `10` Bootstrap Checklist | ตรวจสอบว่า setup ครบก่อน deploy |
| `11` AI Decision Protocol | กฎว่า AI ตัดสินใจอะไรได้เอง อะไรต้องถาม |
| `12` ADR | บันทึก architectural decisions |
| `13` Retrospective | ทบทวนการทำงานรายช่วง |
| `14` Anti-Patterns | สิ่งที่ไม่ควรทำ |
| `15` Compliance Check | ตรวจ code quality อัตโนมัติทุก session |

---

## หลักการออกแบบ

- **Source docs คือ source of truth** — ห้ามแก้ requirement โดยตรง ต้อง version ใหม่เท่านั้น
- **AI อ่าน AI-CONTEXT block ก่อน** — 3 ไฟล์หลักมี compact block ด้านบนเพื่อประหยัด token
- **ทุก task มี traceability** — trace กลับถึง requirement ได้ทุก task
- **Do less, document more** — AI หยุดพร้อมบันทึกชัดเจน ดีกว่าตัดสินใจเงียบ ๆ แล้วผิด
- **ใช้ได้กับทุก AI tool** — Claude, ChatGPT, Gemini หรือ tool ใดก็ตามที่ทีมใช้

---

## License

MIT
