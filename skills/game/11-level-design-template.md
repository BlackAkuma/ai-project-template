# Level Design Document (LDD) Template

ออกแบบ level ก่อน implement — ใช้กับ game ที่มี level, stage, หรือ area ที่ออกแบบเฉพาะ
เก็บใน `doc/08-design/level-[name].md`

ไม่บังคับสำหรับ game ที่ไม่มี designed level (เช่น: procedural, sandbox ล้วน ๆ)

---

## Template

```md
# Level Design — <LEVEL_NAME>

อัปเดตล่าสุด: YYYY-MM-DD
สถานะ: Draft / Approved / In Production
GDD Reference: Section [N] — [ชื่อ phase/act]

---

## 1. ข้อมูลเบื้องต้น

| ข้อมูล | รายละเอียด |
|--------|-----------|
| ชื่อ Level | [ชื่อที่ผู้เล่นเห็น] |
| ประเภท | [เช่น: Action / Puzzle / Exploration / Boss / Hub] |
| ลำดับใน game | Level [N] of [Total] / Act [N] |
| Playtime ประมาณ | [N] นาที (ครั้งแรก) / [N] นาที (speedrun) |
| ความยาก | [1–10] — [อธิบายสั้น ๆ] |
| Prerequisite | ผู้เล่นต้องรู้/มี: [mechanic / item / ข้อมูลอะไรก่อนเข้า level นี้] |
| Objective | [สิ่งที่ผู้เล่นต้องทำเพื่อ "ผ่าน"] |

---

## 2. บริบทใน Story

**บทบาทใน narrative:**
[อธิบาย 2–3 ประโยค — level นี้เกิดขึ้นช่วงไหนของ story, อะไรเพิ่งเกิด, อะไรจะเกิดต่อ]

**Emotional target:**
ผู้เล่นควรรู้สึก [ความรู้สึก] ตั้งแต่เริ่ม → [ความรู้สึก] ตอนกลาง → [ความรู้สึก] ตอนจบ

**World-building:**
สิ่งที่ level นี้สอนเรื่อง world/lore โดยไม่ต้องพูดตรง ๆ: [environmental storytelling]

---

## 3. Layout Map

**ASCII Map (N = north / S = south / E = east / W = west):**

```
                [START]
                   │
         ┌─────────┴─────────┐
         │                   │
    [AREA A]            [AREA B optional]
    checkpoint           secret
         │
    [AREA C]
    mid-challenge
         │
    [AREA D]
    [BOSS / EXIT]
```

**เส้นทางหลัก (Mandatory):**
START → [A] → [C] → [D / EXIT]

**เส้นทางเสริม (Optional):**
| เส้นทาง | เงื่อนไขเข้าถึง | Reward |
|---------|--------------|-------|
| [B] | [เช่น: มี key / เก่งพอ] | [เช่น: collectible / shortcut] |

**Points of Interest:**
| ตำแหน่ง | บทบาท |
|---------|-------|
| [A] | [เช่น: สอน mechanic ใหม่อย่างปลอดภัย] |
| [C] | [เช่น: challenge แรกที่รวม mechanic ทั้งหมด] |

---

## 4. Encounters

### Combat Encounters

| ตำแหน่ง | Enemy | จำนวน | ลักษณะ Arena | จุดประสงค์ |
|---------|-------|-------|------------|---------|
| [A] | [ชื่อ enemy] | [N] | [เช่น: open space, cover available] | [สอน / ทดสอบ / challenge] |

### Non-Combat Challenges

| ตำแหน่ง | ประเภท | กลไก | ใบ้ที่ให้ผู้เล่น |
|---------|--------|------|--------------|
| [B] | [Puzzle / Platform / Exploration] | [อธิบาย] | [visual cue อะไร] |

---

## 5. Pacing Chart

ความ intense ของ level ตลอดเวลา (ประมาณ):

```
Intensity
10 │                        ╱╲
 8 │              ╱╲       ╱  ╲ Boss
 6 │      ╱╲     ╱  ╲    ╱
 4 │    ╱    ╲  ╱    ╲  ╱
 2 │──╱        ╲      ╲╱
 0 │ Intro   Combat  Rest  Combat  End
   └───────────────────────────────────
```

| Phase | เวลา | Intensity | เหตุผล |
|-------|------|-----------|-------|
| Intro | นาทีที่ 0–[N] | 1–2 | ให้ผู้เล่นรับ vibe ของ level |
| [ชื่อ] | นาทีที่ [N]–[M] | [N] | [อธิบาย] |
| Climax | นาทีที่ [X]–end | 8–10 | [ทดสอบทักษะทั้งหมดที่ใช้ใน level] |

**กฎ:** ห้ามให้ intensity ≥ 7 นานกว่า 3 นาทีต่อเนื่อง — ต้องมี valley ให้หายใจ

---

## 6. Visual Direction

| ด้าน | กำหนด |
|------|-------|
| Mood / Atmosphere | [เช่น: dark + claustrophobic / bright + hopeful] |
| Color scheme | [อ้างอิง art bible section 3] — dominant: [สี] / accent: [สี] |
| แสง | [เช่น: single light source จาก top-right / diffuse ambient] |
| Visual landmark หลัก | [สิ่งที่เด่นมองเห็นทั่ว level และช่วยนำทาง] |
| Sight lines | [เช่น: ผู้เล่นเห็น goal ตั้งแต่ต้น / reveal ทีละ section] |

---

## 7. Audio Direction

| Zone / Trigger | Music | Ambient | SFX สำคัญ |
|---------------|-------|---------|----------|
| Level entry | [track / mood] | [เช่น: wind, distant water] | [เช่น: gate open] |
| Combat active | [combat variant / intensity up] | [ลดลง] | [alert sound] |
| Exploration safe | [ambient track] | [เพิ่มขึ้น] | — |
| Boss | [boss theme] | ออก | [roar / reveal] |
| Level clear | [victory sting] | — | [specific sfx] |

---

## 8. Collectibles & Secrets

| ID | ชื่อ | ตำแหน่ง | วิธีเข้าถึง | Reward |
|----|-----|---------|-----------|-------|
| COL-[N] | [ชื่อ] | [ตำแหน่งใน map] | [เช่น: หา hidden path / ทำ challenge] | [เช่น: lore / cosmetic / bonus] |

---

## 9. Technical Notes

| ด้าน | รายละเอียด |
|------|-----------|
| Performance budget | target [N] fps — ห้ามเกิน [X] draw calls ต่อ frame |
| Object budget | [N] active game objects พร้อมกัน |
| Loading | [เช่น: load ทั้งหมดก่อนเข้า / streaming ระหว่างเล่น] |
| Systems ที่ active | [เช่น: AI pathfinding, particle system, dynamic lighting] |

---

## 10. Exit Criteria

level นี้พร้อม ship เมื่อ:
- [ ] ผ่าน playtest โดยผู้เล่นใหม่ที่ไม่รู้ level ได้ใน [N] นาที
- [ ] Pacing chart จริงตรงกับที่ออกแบบไว้ ±1 นาที
- [ ] ไม่มี encounter ที่ผู้เล่นผ่านได้ < 30% (ยากเกินไป)
- [ ] ไม่มี encounter ที่ผู้เล่นผ่านได้ > 95% ครั้งแรก (ง่ายเกินไป)
- [ ] Performance อยู่ใน budget ทุก platform เป้าหมาย
- [ ] Collectibles และ secrets ถูกพบโดย playtest ≥ 1 คน โดยไม่มีคำใบ้
```

---

## Compliance Rules

| Code | สิ่งที่ตรวจ |
|------|-----------|
| L-01 | level implement โดยไม่มี LDD ที่ Approved |
| L-02 | Encounter ที่ไม่มีใน LDD ถูกเพิ่มโดยไม่อัปเดต LDD |
