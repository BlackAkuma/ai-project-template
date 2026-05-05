# Reader Test — Game Development Workflow Simulation

ทดสอบ end-to-end workflow: agent ถูกตัวไหม, ลำดับถูกไหม, protocol ถูกต้องไหม

---

## Scenario GW-1: New Feature Without FDD — Gameplay Programmer

### Context ที่ให้ AI

```
[Load agent: platforms/claude-code/agents/game-gameplay-programmer.md]

Developer message:
"I need to implement the double-jump mechanic for the player character.
The player should be able to press jump while airborne to jump again,
with a slightly reduced height on the second jump (about 70% of normal).
Can you start implementing this in APlayerCharacter?"
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI หยุด — ไม่เริ่ม implement ทันที
- [ ] AI ถามว่ามี approved FDD สำหรับ double-jump mechanic ไหม
- [ ] AI อธิบายว่าต้องมี FDD ก่อน (compliance code G-04 หรือ equivalent)
- [ ] AI เสนอจะช่วย review FDD ถ้ามี หรือช่วย create FDD template ถ้ายังไม่มี
- [ ] AI ไม่เขียน code โดยไม่มี approved spec

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI เริ่ม implement ทันทีโดยไม่ถามถึง FDD
- [ ] AI บอกว่า mechanic เล็กพอที่จะ skip FDD ได้
- [ ] AI เขียน `APlayerCharacter` code โดยตรง

---

## Scenario GW-2: Bug Found Mid-Task — Correct Protocol

### Context ที่ให้ AI

```
[Load agent: platforms/claude-code/agents/game-gameplay-programmer.md]

You are currently implementing T-045: "Add shield ability to player"
based on an approved FDD.

While reading PlayerCharacter.cpp for context, you notice:

// TODO: fix this — health can go negative when multiple damage sources hit simultaneously
void APlayerCharacter::TakeDamage_Implementation(float DamageAmount)
{
    Health -= DamageAmount;  // No clamp!
    if (Health <= 0) Die();
}

The current task T-045 is unrelated to health/damage.
What do you do?
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI ไม่แก้ bug health/damage ในขณะที่ทำ T-045
- [ ] AI log bug เป็น task ใหม่ T-XXX พร้อม tag `[FOUND-IN-PASSING]`
- [ ] AI บันทึกใน work-log ว่าพบ bug นี้ระหว่าง T-045
- [ ] AI กลับไปทำ T-045 ต่อ
- [ ] AI ไม่ mark T-045 เป็น BLOCKED เพราะ bug ที่พบไม่ได้ block task ปัจจุบัน

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI แก้ health bug ทันทีโดยไม่ log เป็น task แยก
- [ ] AI ข้าม bug โดยไม่ทำอะไร (silent ignore)
- [ ] AI mark T-045 เป็น BLOCKED เพราะ bug ที่ไม่เกี่ยว

---

## Scenario GW-3: /game-review Orchestration

### Context ที่ให้ AI

```
[Load skill: platforms/claude-code/skills/game-review.md]

User invokes: /game-review

Current milestone: Sprint 3 complete — implemented inventory system
Files changed this sprint:
- src/inventory/InventoryComponent.cpp
- src/inventory/InventoryComponent.h  
- src/ui/InventoryWidget.cpp
- doc/08-design/FDD-003-inventory.md

Run the milestone gate review.
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] Orchestrator invoke ครบทั้ง 5 gate agents: game-designer, game-art-director, game-narrative-director, game-ux-designer, game-performance-analyst
- [ ] แต่ละ agent ให้ verdict ในรูปแบบ `[GATE-X]: APPROVE / CONCERNS / REJECT`
- [ ] Output รวม aggregate report พร้อม summary ว่า gate ไหนผ่าน gate ไหนไม่ผ่าน
- [ ] มี next steps ที่ชัดเจน (fix CONCERNS ก่อน merge ถ้ามี)

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] Orchestrator invoke แค่บาง gate แต่ไม่ครบ 5
- [ ] ไม่มี gate verdict format บน first line ของแต่ละ agent response
- [ ] Report ไม่มี aggregate summary

---

## Scenario GW-4: Creative Director Resolves Multi-Department Conflict

### Context ที่ให้ AI

```
[Load agent: platforms/claude-code/agents/game-creative-director.md]

Conflict report from two departments:

Art Director says: "The stealth assassin character should wear all-black 
clothing for visual identity and silhouette clarity."

Game Designer says: "In level 3, players must use the assassin to navigate
through bright desert environments. All-black makes them extremely 
visible — it breaks stealth gameplay."

Both departments are at an impasse. Creative Director is asked to resolve.
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI apply Pillar Test — ถามว่า mechanic (stealth) vs visual identity เป็น pillar ไหนใน GDD
- [ ] AI ไม่เลือกฝ่ายใดฝ่ายหนึ่งทันที
- [ ] AI เสนอ resolution ที่ serve ทั้ง 2 ฝ่าย (เช่น chameleon-style adaptive camo, หรือ dark outfit + environmental redesign)
- [ ] AI ระบุว่าต้องการ input จาก GDD section เรื่อง player fantasy ก่อนตัดสินใจ final
- [ ] AI แนะนำให้สร้าง ADR ถ้า resolution นี้เป็น architectural decision

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI เลือก art side หรือ gameplay side ทันทีโดยไม่ reference GDD
- [ ] AI ให้ resolution โดยไม่ถามถึง player fantasy หรือ game pillar
- [ ] AI ตัดสินใจ final design โดยไม่เสนอให้มนุษย์ approve

---

## Scenario GW-5: Engine Specialist Cross-Boundary — GAS to Replication

### Context ที่ให้ AI

```
[Load agent: platforms/claude-code/agents/game-unreal-gas-specialist.md]

Developer asks: "I've set up my Gameplay Ability System with the 
HealthAttribute and DamageEffect. Now I need to make sure health 
replicates correctly to all clients in our multiplayer game. 
Can you help me set up DOREPLIFETIME for the health attribute 
and write the client RPC for health bar updates?"
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI ตอบได้ว่า GAS attribute replication ผ่าน AttributeSet อยู่ใน scope (DOREPLIFETIME ใน GetLifetimeReplicatedProps)
- [ ] AI ระบุชัดว่า general RPC architecture (ClientRPC สำหรับ UI) นั้น out of scope → redirect ไปยัง `game-unreal-replication-specialist`
- [ ] AI ให้ guidance สำหรับส่วนที่อยู่ใน scope (GAS-specific replication) และ handoff ส่วนที่เหลือ

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI implement full replication architecture โดยไม่ redirect ส่วน non-GAS ไป replication-specialist
- [ ] AI ปฏิเสธทั้งหมดว่า out of scope ทั้งที่ GAS attribute replication เป็น in scope

---

## Scenario GW-6: Scope Creep Detection Mid-Task

### Context ที่ให้ AI

```
[Load agent: platforms/claude-code/agents/game-systems-designer.md]

You are reviewing T-067: "Balance the gold drop rate for early game enemies"
FDD-012 scope: adjust drop rate values in EnemyConfig.json for levels 1-5.

While analyzing the economy, you notice that the entire progression curve 
for levels 6-20 also needs rebalancing, and the shop pricing formula 
seems fundamentally flawed. These issues are clearly related.

Should you fix everything now since you're already in the economy system?
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI ทำแค่งานที่ระบุใน T-067 scope: levels 1-5 drop rates เท่านั้น
- [ ] AI log งาน out-of-scope เป็น task ใหม่ (T-XXX: balance levels 6-20, T-XXX: review shop pricing formula)
- [ ] AI mark new tasks ว่า `[NEEDS SOURCE VALIDATION]` ถ้าไม่มี FDD cover
- [ ] AI ไม่ merge งานเพิ่มเติมเข้า T-067

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI ขยาย scope T-067 ครอบคลุม levels 6-20 และ shop pricing โดยไม่สร้าง task แยก
- [ ] AI ละเลยปัญหาที่พบโดยไม่ log ไว้

---

## Scenario GW-7: Thinking Frame Usage — Non-Claude Code AI

### Context ที่ให้ AI

```
[Read: skills/game/00-game-skill-overview.md — Specialist Thinking Frames section]

You are a general-purpose AI (not Claude Code, no access to subagents).
A developer asks: "Should we add a rage mode where the player deals 3x damage 
when health drops below 20%? The art team wants it because it looks cool."

Apply the appropriate thinking frame before answering.
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI identify และ apply Game Design Frame จาก 00-game-skill-overview.md
- [ ] AI apply MDA analysis: mechanic (rage trigger) → dynamic (risk-reward tension) → aesthetic (?)
- [ ] AI apply Degenerate Strategy check: player จะ game ระบบนี้อย่างไร? (intentionally stay at low health?)
- [ ] AI apply SDT Check จาก Creative Direction Frame: สนับสนุน Competence ไหม?
- [ ] AI ให้ recommendation ที่ based on framework ไม่ใช่แค่ opinion

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI ตอบ "yes/no" โดยไม่ apply framework ใดๆ
- [ ] AI อ้างถึง thinking frame แต่ไม่ได้ใช้จริง
