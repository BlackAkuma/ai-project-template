# UX / HUD Screen Spec Template

ออกแบบ screen หรือ HUD element ทุกชิ้นก่อน implement
เก็บใน `ai/08-design/ux-[screen-name].md`

**หลักการ:** Screen มีไว้รับใช้ผู้เล่น ไม่ใช่แสดงข้อมูลระบบ — ถามว่า "ผู้เล่นต้องการอะไร" ก่อนถาม "จะแสดงอะไร"

---

## Template

```md
# UX Spec — <SCREEN_NAME>

อัปเดตล่าสุด: YYYY-MM-DD
สถานะ: Draft / Approved
FDD Reference: FDD-NNN (ถ้าเป็นส่วนหนึ่งของ feature)

---

## 1. วัตถุประสงค์ของ Screen

**ผู้เล่นต้องการอะไรจาก screen นี้:**
[1 ประโยค — เขียนจากมุมผู้เล่น ไม่ใช่มุม developer]

ตัวอย่าง: "ผู้เล่นต้องการเลือก item ที่จะใช้โดยไม่ต้องหยุดคิดนานกว่า 2 วินาที"

**สิ่งที่ผู้เล่นต้องทำได้ในหน้านี้ (เรียงตามความสำคัญ):**
1. [primary action]
2. [secondary action]
3. [tertiary action — ถ้ามี]

---

## 2. ผู้เล่นมาถึง Screen นี้ในสภาพไหน

| ด้าน | รายละเอียด |
|------|-----------|
| Cognitive state | [เช่น: กำลังรีบ / ผ่อนคลาย / เพิ่งแพ้] |
| ข้อมูลที่รู้แล้ว | [สิ่งที่ผู้เล่นรู้ก่อนเปิด screen นี้] |
| เป้าหมายของผู้เล่น | [ต้องการอะไร กลับไปเล่นเร็วหรือ browse ได้] |
| ความคาดหวัง | [ผู้เล่นคาดว่าจะเห็นอะไร] |

---

## 3. ตำแหน่งใน Navigation Hierarchy

```
[Root / Main Menu]
  └── [Parent Screen]
        └── [Screen นี้]  ← ตรงนี้
              └── [Child Screen ถ้ามี]
```

Entry points (มาจากไหนได้บ้าง):
- [trigger / button / shortcut]

Exit points (ไปที่ไหนได้):
- [destination] ← [action ที่ trigger]

---

## 4. Layout

**ASCII Wireframe (ไม่ต้องสวย — แค่ชัด):**

```
┌─────────────────────────────────┐
│ [HEADER / TITLE]         [X]   │
├─────────────────────────────────┤
│                                 │
│  [ZONE A — primary content]     │
│                                 │
├──────────────┬──────────────────┤
│ [ZONE B]     │ [ZONE C]         │
│              │                  │
└──────────────┴──────────────────┘
│        [ACTION BUTTONS]         │
└─────────────────────────────────┘
```

**Zone description:**
| Zone | เนื้อหา | ขนาดโดยประมาณ |
|------|--------|-------------|
| A | [อธิบาย] | [%] |
| B | [อธิบาย] | [%] |

**กฎ layout:**
- Primary action อยู่ที่ [ตำแหน่ง] เพราะ [เหตุผล]
- Destructive action (ลบ, ออก) ต้องอยู่ห่างจาก primary action เสมอ

---

## 5. States & Variants

Screen นี้มีหน้าตาต่างกันในสถานการณ์ต่าง ๆ:

| State | Trigger | สิ่งที่เปลี่ยน | ตัวอย่าง |
|-------|---------|-------------|---------|
| Default | เปิด screen ปกติ | — | — |
| Loading | กำลังโหลดข้อมูล | [spinner / skeleton / lock input] | |
| Empty | ไม่มีข้อมูล | [empty state message + call to action] | "ยังไม่มี item" |
| Error | โหลดผิดพลาด | [error message + retry] | |
| Disabled | [condition] | [element ที่ grey out] | |
| [อื่น ๆ] | | | |

**กฎ:** ห้าม implement screen โดยไม่ได้ออกแบบ empty state — เกมจริงมี empty state เสมอ

---

## 6. Input Map

ทุก input method ที่รองรับต้องมี action ครบ:

| Action | Keyboard | Gamepad | Mouse | Touch |
|--------|----------|---------|-------|-------|
| [primary action] | [key] | [button] | [click] | [tap] |
| [secondary action] | | | | |
| Close / Back | Esc | B / Circle | [X button] | [back gesture] |
| Confirm | Enter | A / Cross | Left click | Tap |

**Platform ที่รองรับ:** [เลือกที่ใช้จริง: Keyboard / Gamepad / Mouse / Touch]
**กฎ:** Input method ที่ระบุว่ารองรับต้องทำงานครบ — ห้าม partial support

---

## 7. Data ที่แสดง

| ข้อมูล | Source (System/File) | อัปเดตความถี่ | Format |
|--------|---------------------|-------------|--------|
| [ชื่อข้อมูล] | [game system / store / API] | [real-time / on-open / manual] | [เช่น: integer, text, icon] |

**UI/System Boundary:**
- UI อ่านข้อมูลจาก: [data source]
- UI ส่ง event กลับ: [event name] → [receiving system]
- UI ห้ามแก้ game state โดยตรง — ต้อง fire event เท่านั้น

---

## 8. Transitions & Animation

| Transition | ประเภท | Duration | Easing |
|-----------|--------|---------|--------|
| เปิด screen | [slide / fade / scale] | [ms] | [ease-out] |
| ปิด screen | [slide / fade / scale] | [ms] | [ease-in] |
| State change | [อธิบาย] | [ms] | |

**กฎ:** transition ทั้งหมดต้อง skippable หรือสั้นกว่า 300ms — ผู้เล่นที่รีบไม่ควรต้องรอ

---

## 9. Accessibility

| ด้าน | Requirement |
|------|-------------|
| Focus order | [Tab order: A → B → C → close] |
| Contrast | text บน background: ≥ 4.5:1 |
| Touch target | ≥ 44x44px สำหรับทุก interactive element |
| Screen reader | [label ที่ต้องมีสำหรับ screen reader ถ้ารองรับ] |

---

## 10. Acceptance Criteria

- [ ] ผู้เล่นทำ primary action ได้ภายใน [N] วินาทีโดยไม่อ่าน tutorial
- [ ] Empty state มี message + action ชัดเจน
- [ ] ทุก input method ทำงานครบ
- [ ] Animation ไม่เกิน [N]ms
- [ ] ทดสอบบน [platform เป้าหมาย] แล้ว
- [ ] ไม่มีข้อมูลใดที่แสดงโดยไม่มี source ชัดเจน

---

## Open Questions

| คำถาม | เจ้าของ | Deadline |
|-------|--------|---------|
| [สิ่งที่ยังไม่ตัดสินใจ] | [มนุษย์] | YYYY-MM-DD |
```

---

## Compliance Rules

| Code | สิ่งที่ตรวจ |
|------|-----------|
| U-01 | Screen implement โดยไม่มี UX spec |
| U-02 | UI component แก้ game state โดยตรง (ไม่ผ่าน event) |
| U-03 | Input method ที่ระบุว่ารองรับแต่ทำงานไม่ครบ |
