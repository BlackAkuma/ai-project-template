# Game Development Skill Pack

เปิดใช้งานเมื่อโปรเจ็กต์เป็น game หรือ web game
อ่านไฟล์ทั้งหมดในโฟลเดอร์นี้ต่อจาก core templates

---

## เมื่อไหร่ที่ควรใช้ skill pack นี้

ใช้เมื่อโปรเจ็กต์มีลักษณะอย่างน้อย 1 ข้อ:
- มี gameplay loop (win/lose condition, scoring, progression)
- มี real-time updates หรือ game loop (update per frame)
- มี physics หรือ collision detection
- มี player input → game state → render cycle
- เป็น web game, browser game, mobile game, desktop game

**ครอบคลุมทุก platform:** Unity, Godot, Phaser, Three.js, HTML5 Canvas, WebGL, PixiJS, native mobile game

---

## ไฟล์ในชุดนี้

| ไฟล์ | หน้าที่ |
|------|--------|
| `00-game-skill-overview.md` | ภาพรวม (ไฟล์นี้) |
| `01-fdd-template.md` | Feature Design Document — ออกแบบ feature ก่อนโค้ด |
| `02-game-coding-standards.md` | มาตรฐานโค้ดสำหรับ game โดยเฉพาะ |
| `03-asset-protocol.md` | การจัดการ assets — naming, structure, validation |
| `04-compliance-codes.md` | Compliance codes G-01–G-10, A-01–A-07, N-01–N-04 ฯลฯ |
| `05-game-session-end-template.md` | Session end protocol สำหรับ game project |
| `06-narrative-standards-template.md` | มาตรฐานการเขียน narrative, dialogue, localization |
| `07-gdd-template.md` | Game Design Document template |
| `08-difficulty-curve-template.md` | Difficulty curve และ Sawtooth pattern template |
| `09-art-bible-template.md` | Art bible — visual direction, color palette, style guide |
| `10-ux-hud-template.md` | UX/HUD design spec template |
| `11-level-design-template.md` | Level design document template |

---

## Specialist Thinking Frames

สำหรับ AI tools ที่ไม่ใช่ Claude Code (ChatGPT, Gemini, Copilot ฯลฯ) ใช้ thinking frame เหล่านี้เมื่อต้องการ perspective จาก specialist:

### 🎮 Game Design Frame
ก่อนประเมิน mechanic ใดๆ ให้ถามตัวเองว่า:
- **MDA:** mechanic นี้สร้าง dynamic อะไร → player จะรู้สึก aesthetic อะไร?
- **Degenerate Strategy:** player จะ exploit อะไรจาก mechanic นี้?
- **Player Fantasy:** mechanic นี้ serve fantasy ที่ระบุใน GDD section 2 ไหม?
- **Sawtooth Pattern:** challenge spike นี้มี recovery window ไหม?

### 🎨 Art Direction Frame
ก่อน review/recommend asset ใดๆ:
- **Silhouette Test:** ถ้า fill สีดำทึบ ยังบอก character/object ได้ไหม?
- **Emotional Color:** สีที่ใช้ตรงกับ emotional meaning ใน art bible ไหม?
- **Visual Hierarchy:** player attention ไหลไป: threat → interactive → ambient ถูกต้องไหม?
- **A11y Check:** มี icon + color ไม่ใช่แค่ color เพื่อสื่อความหมาย?

### 📖 Narrative Frame
ก่อน review/เขียน dialogue หรือ story:
- **Dialogue Function Test:** บรรทัดนี้ทำอย่างน้อย 1 ใน 4: reveal character / advance plot / deliver info / create mood?
- **Character Knowledge:** ณ scene นี้ character รู้อะไรได้บ้าง ยังไม่ควรรู้อะไร?
- **Ludonarrative Check:** mechanic กับ story บอกสิ่งเดียวกัน หรือขัดแย้งกัน?
- **Arc Catalyst:** ถ้า character เปลี่ยนใจ — catalyst ชัดพอไหม?

### 🖥️ UX Frame
ก่อน design หรือ review screen:
- **Mental Model:** player expect อะไรจาก screen นี้ ก่อนที่จะเห็น?
- **Cognitive Load:** screen นี้ให้ตัดสินใจกี่อย่างพร้อมกัน? ลดได้ไหม?
- **FTUX Test:** new player เข้าใจ core loop ภายใน 5 นาทีโดยไม่อ่าน manual?
- **State Coverage:** loading / empty / error / disabled states ถูก design ครบไหม?

### ⚡ Performance Frame
ก่อน implement หรือ optimize:
- **Profile First:** วัด actual bottleneck ก่อน — อย่า assume
- **Frame Budget:** 60fps = 16.67ms; feature นี้กินเท่าไร? เหลือเท่าไร?
- **Allocation Rate:** loop นี้ create object ต่อ frame ไหม? → pool แทน
- **Complexity:** complexity scale กับอะไร? entity count? player count? level size?

---

### 🎯 Creative Direction Frame
ก่อนตัดสินใจ creative direction หรือแก้ conflict ระหว่าง department:
- **Pillar Test:** feature นี้ serve GDD pillar ไหน? อันไหนชัดที่สุด?
- **Player Fantasy:** player จะรู้สึกอะไร? ตรงกับ fantasy ที่ระบุไหม?
- **Ludonarrative Consonance:** mechanic และ story บอกสิ่งเดียวกันไหม?
- **Pressure Cut:** ถ้าต้องตัด 1 feature — ตัดอะไรก่อน? (ตัดที่ห่าง pillar มากที่สุด)
- **SDT Check:** feature นี้สนับสนุน Autonomy / Competence / Relatedness ไหม?

### 🏗️ Technical Direction Frame
ก่อนตัดสินใจ architecture หรือ technology:
- **Five Criteria:** correctness, simplicity, performance, maintainability, testability, reversibility cost — คะแนนแต่ละข้อ?
- **ADR Required?:** เป็น non-obvious decision ไหม? → ต้องสร้าง ADR ก่อน implement
- **Reversibility:** ถ้า decision นี้ผิด เปลี่ยนกลับยากแค่ไหน? cost เท่าไร?
- **Budget Impact:** decision นี้กระทบ performance budget ไหน? (frame/memory/load/bandwidth)
- **Technical Debt:** debt นี้ intentional ไหม? กำหนด repayment plan แล้วไหม?

### 📋 Production Frame
ก่อน plan sprint หรือ negotiate scope:
- **Capacity Math:** available days − 20% reserve = actual capacity; commit เกินไหม?
- **Task Window:** task ไหนใช้เวลา >3 วัน? → split ก่อน
- **Blocker Scan:** task ไหน blocked? blocked มานานแค่ไหน? unblock ด้วยอะไร?
- **Risk Registry:** probability × impact สูงสุดตอนนี้คืออะไร? มี mitigation ไหม?
- **Scope Pressure:** ถ้า capacity ไม่พอ — cut scope (preferred) / extend time / reduce quality?

---

### 💻 Lead Programmer Frame
ก่อน design หรือ review code structure:
- **Interface First:** depend on abstraction ไม่ใช่ concrete? มี singleton ที่ไม่ควรมีไหม?
- **Complexity:** method นี้ cyclomatic complexity เท่าไร? เกิน 10 ไหม?
- **Method Length:** method ยาวเกิน 40 lines ไหม? → extract
- **Test Surface:** public API นี้ testable ไหม? mock ง่ายไหม?
- **Pattern Consistency:** code ใหม่ match pattern ที่มีอยู่ไหม? ถ้าไม่ — อธิบายทำไม

### 🎲 Gameplay Code Frame
ก่อน implement gameplay feature:
- **FDD Exists?:** มี approved FDD ก่อน implement ไหม? ถ้าไม่มี → STOP
- **Data-Driven:** ค่า config ทั้งหมดอยู่ใน data file ไหม? ไม่มี hardcode?
- **State Machine:** interactive system นี้มี explicit state transition table ไหม?
- **FDD Fidelity:** implement ตรงกับ FDD spec ไหม? ถ้าเบี่ยง → amend FDD ก่อน
- **Unit Test:** public function มี test สำหรับ normal case + edge case ไหม?

### ⚙️ Engine Systems Frame
ก่อน design engine-level system:
- **Zero-Alloc Hot Path:** game loop code allocate memory per frame ไหม? → pool
- **Threading Model:** system นี้ thread-safe ไหม? ระบุ threading contract ชัดเจนไหม?
- **API Stability:** เปลี่ยน API นี้จะ break กี่ call sites? มี deprecation plan ไหม?
- **Platform Abstraction:** platform-specific code isolated อยู่ใน platform module ไหม?
- **ADR Needed?:** นี่เป็น architecture decision ที่ต้องบันทึกไหม?

### 🤖 AI/NPC Frame
ก่อน design behavior system:
- **Architecture Choice:** behavior tree / state machine / utility — เลือกอะไร ทำไม?
- **2ms Budget:** AI ทั้งหมดใน scene ใช้เกิน 2ms/frame ไหม?
- **Tunable Params:** parameter ทุกตัว (range, speed, cooldown) อยู่ใน data file ไหม?
- **Emergent Risk:** behavior combination สร้าง unexpected behavior อะไรได้บ้าง?
- **Player Perception:** player จะ "อ่าน" behavior นี้ถูกต้องไหม? predictable พอไหม?

### 🌐 Network Frame
ก่อน design feature ที่มี multiplayer:
- **Server Authority:** อะไรที่ client ส่ง? อะไรที่ server validate?
- **Zero Trust:** ถ้า client ส่งค่า malicious — worst case คืออะไร?
- **Lag Compensation:** prediction ใช้ที่ไหน? reconciliation เกิดตอนไหน?
- **Bandwidth Cost:** feature นี้เพิ่ม ~N bytes/tick ที่ Hz เท่าไร? เกิน 10KB/s/client ไหม?
- **Rate Limit:** มี rate limit สำหรับ message ที่ client spam ได้ไหม?

### 🖼️ UI Code Frame
ก่อน implement screen หรือ HUD:
- **UX Spec Exists?:** มี UX spec ก่อน implement ไหม? ถ้าไม่มี → สร้างก่อน (U-01)
- **Unidirectional Flow:** UI อ่าน state → fire events เท่านั้น; ห้าม mutate game state ตรง (U-02)
- **Input Complete?:** keyboard nav / gamepad nav / touch ครบไหม? (U-03)
- **String System:** text ทั้งหมดผ่าน string system ไหม? ไม่มี hardcode? (N-01)
- **Reactive Binding:** UI subscribe to state changes ไหม? หรือ poll ทุก frame?

### 🔧 Tools Frame
ก่อน build tool หรือ pipeline:
- **Purpose Clear?:** tool ทำอะไร? input/output/failure mode ระบุชัดไหม?
- **Test Before Deploy:** ทดสอบกับ representative data ก่อน team ใช้ไหม?
- **Runtime Safe?:** tool ทำงานที่ edit/build time ไม่ใช่ runtime ไหม?
- **Extend vs. Build:** มี tool เดิมที่ extend ได้ไหม? สร้างใหม่จำเป็นจริงๆ ไหม?
- **Documentation:** มี README: ทำอะไร, input, output, failure modes ไหม?

### 🚀 DevOps Frame
ก่อน configure pipeline หรือ branching:
- **Main Always Shippable:** main/master ผ่าน all tests ตลอดเวลาไหม?
- **CI on Every Push?:** feature branches รัน full CI ไหม?
- **No Skip Rule:** มีเหตุผลที่จะ skip CI step ไหม? → ไม่มี fix pipeline แทน
- **Rollback Path:** ถ้า deploy fail — rollback ทำยังไง? ใช้เวลาเท่าไร?
- **Branch Strategy:** commit นี้ควรอยู่ branch ไหน? (feature / develop / release / hotfix)

### 🔒 Security Frame
ก่อน implement feature ที่รับ client input:
- **Attack Surface:** client ส่งอะไรได้บ้าง? attacker exploit อะไรได้?
- **Server Validate ALL:** validate ทุก client field server-side ไหม? ไม่มี trust client?
- **Rate Limit Applied?:** spam ได้ไหม? → rate limit
- **Privacy Check:** feature เก็บ PII ไหม? มี consent + deletion pathway ไหม?
- **Anomaly Monitor:** behavioral outlier (speed, position, frequency) detect ได้ไหม?

---

### 🗺️ Level Design Frame
ก่อน design หรือ review level:
- **Spatial Flow:** player movement มี natural path ไหม? dead end มี reward ไหม?
- **Three Paths:** critical path / optional path / secret path — ทั้ง 3 intentional ไหม?
- **Pacing Chart:** intensity เพิ่มลดตาม sawtooth ไหม? peak มี valley ตาม?
- **Encounter Intro:** mechanic นี้ intro safe ก่อน → test under pressure ไหม?
- **Exit Criteria:** เกณฑ์ผ่าน level มาจาก playtest ไหม? ไม่ใช่ designer opinion?

### 📐 Systems Design Frame
ก่อน design formula หรือ game system:
- **Formula Complete?:** มี variable table + output range + worked example ไหม?
- **Loop Type:** reinforcing loop (runaway risk) หรือ balancing loop? intentional ไหม?
- **Interaction Matrix:** system A กับ system B กระทบกันยังไง? documented ไหม?
- **Sensitivity:** doubling key variable → result เปลี่ยนเท่าไร? acceptable ไหม?
- **Output Bounded?:** formula มี min/max output ไหม? ไม่มี unbounded value?

### 💰 Economy Frame
ก่อน design economy หรือ loot system:
- **Source/Sink Balance:** resource เข้าเร็วกว่าออกไหม? → inflation risk
- **Drop Rate Explicit?:** loot table แสดง % จริง (ไม่ใช่แค่ weight) ไหม?
- **Progression Cliff?:** requirement เพิ่มขึ้น 3x+ จาก level ก่อนหน้าไหม?
- **Pay-to-Win?:** purchased content ให้ competitive advantage ไหม? → ห้าม
- **Reward Psychology:** variable/fixed ratio reward — เลือก intentionally ไหม?

### 📅 Live Ops Frame
ก่อน design event หรือ season:
- **Player Motivation:** event นี้ target Achiever/Explorer/Socializer/Killer motivation ไหน?
- **Retention Cohort:** feature นี้ improve D1/D7/D30/D90 ไหน?
- **FOMO Proportionate?:** time pressure reasonable ไหม? ไม่ใช่ manipulation?
- **No Pay-to-Win:** paid event content ให้ advantage ไหม? → ห้าม
- **Ethics Check:** dark pattern ไหนในนี้? escalate ถ้าพบ

---

### 🎵 Audio Direction Frame
ก่อนกำหนด audio direction หรือ review audio:
- **Sonic Palette:** acoustic vs. synthetic? reference tracks ที่ capture the feel คืออะไร?
- **MDA Audio:** audio mechanics (layers/triggers) → dynamics (adaptive response) → aesthetics (feeling)?
- **Mix Hierarchy:** gameplay audio audible ตลอดไหม? priority order ชัดไหม?
- **Adaptive Logic:** music respond to game state ยังไง? decision tree defined ไหม?
- **Bartle Fit:** audio serve Achiever (triumph) / Explorer (mystery) / Socializer (character) / Killer (impact)?

### 🔊 Sound Design Frame
ก่อน spec SFX หรือ audio event:
- **Spec Complete?:** มี duration, volume range, spatial props, bus assignment ไหม?
- **Variation Strategy:** min 3 variations per event + pitch range ±5-15% ไหม?
- **Repetition Risk:** listener จะ fatigue ใน N นาทีไหม? variation plan ครอบคลุมไหม?
- **Naming Convention:** ตามรูปแบบ `[category]_[context]_[name]_[variant].[ext]` ไหม?
- **Max Simultaneous:** กำหนด max instances + cooldown ต่อ event ไหม?

---

### 🌍 World Building Frame
ก่อน design lore หรือ world element:
- **Canon Level:** Established / Implied / Speculative — ระบุชัดไหม?
- **Consistency Check:** detail นี้ขัดแย้ง established canon ไหน?
- **Player Visibility:** player รู้ fact นี้ได้ตอนไหน? ผ่าน mechanism อะไร?
- **Cross-Reference:** fact นี้ link กับ faction/timeline/geography อื่นไหม?
- **Mystery Layer:** fact นี้เปิดคำถามอะไรเพิ่มเติม? world รู้สึก deep ไหม?

### ✍️ Writing Frame
ก่อนเขียน dialogue หรือ game text:
- **Voice Profile:** บรรทัดนี้ match speaking style ของ character ไหม? ใช้ forbidden phrase ไหม?
- **Localization Ready?:** มี named placeholder ({player_name}) ไม่ใช่ concatenation ไหม?
- **Line Length:** ≤120 chars per line ไหม? voice-actor friendly rhythm ไหม?
- **Function Test:** บรรทัดนี้ reveal character / advance plot / deliver info / create mood — อย่างน้อย 1?
- **Speaker Tag:** dialogue node มี unique ID และ speaker ID ที่ register แล้วไหม?

### 🌏 Localization Frame
ก่อน implement หรือ audit string system:
- **Key Hierarchy:** ใช้ dot notation `category.subcategory.key` ไหม?
- **Hardcoded Strings?:** string ที่ player เห็น hardcode ใน code ไหม? (N-01)
- **Concatenation?:** ต่อ string แทนที่จะใช้ template ไหม? (N-02)
- **Length Variance:** German/Finnish อาจยาวกว่า English 30-40% — UI รองรับไหม?
- **Fallback Chain:** raw key โชว์ถึง player ได้ไหม? → fallback chain ป้องกัน

---

### 🔍 QA Strategy Frame
ก่อน define test strategy หรือ evaluate release readiness:
- **Story Type:** Logic/Integration (BLOCKING tests) หรือ Visual/Feel (ADVISORY human review)?
- **S1 Count:** มี S1 bug (game-breaking) อยู่ไหม? → block release จนกว่าจะ 0
- **Acceptance Criteria:** FDD section 8 มี criteria ชัดเจนก่อน task เข้า in_progress ไหม?
- **Regression Coverage:** fixed bug ทุกตัวมี regression test ไหม?
- **Go Criteria:** S1=0, S2 plan exists, regression >90% — ครบไหม?

### 🐛 QA Testing Frame
ก่อนเขียน test case หรือ bug report:
- **Coverage Matrix:** normal / zero / max / negative / GDD edge cases ครบไหม?
- **Reproduced 3x?:** bug reproduce ได้ 3 ครั้งก่อน report ไหม?
- **Severity Assigned?:** S1 crash/data-loss / S2 major broken / S3 minor / S4 cosmetic?
- **Subjective Criteria?:** acceptance criteria วัดได้จริงไหม? เช่น "feels responsive" → ระบุ threshold (Nms)
- **Regression Scoped?:** regression checklist scope ถึง affected systems เท่านั้น ไม่ใช่ทั้งหมด?

### 📦 Release Frame
ก่อน manage release หรือ plan certification:
- **Pipeline Stage:** อยู่ที่ Build/Test/Cert/Submit/Verify/Launch ไหน? pass criteria อะไร?
- **S1 Zero?:** release gate ต้องการ S1=0 — ครบไหม?
- **Platform Cert:** TRC/TCR/Lotcheck requirements ครบไหม? มี known blockers ไหม?
- **Rollback Ready?:** ถ้า launch fail — hotfix process เตรียมไว้ไหม? target <48h?
- **Post-Launch Watch:** crash rate <0.1% target, D1 retention tracked ไหม?

### 📢 Community Frame
ก่อนเขียน player communication:
- **Before/After Values:** balance change แสดง "ก่อน X → หลัง Y" ไหม? ไม่ใช่ "increased"?
- **Crisis Response?:** acknowledge ก่อน 30 นาที / update ทุก 30-60 นาที ไหม?
- **Tone Check:** combative / dismissive ไหม? → empathetic แต่ professional
- **Player as Partner:** สื่อสารเสมือน player คือ partner ไม่ใช่ complainer?
- **Specific, not Vague:** "กำลังตรวจสอบ" → "ทีมตรวจพบ X กำลังแก้ด้วย Y คาดว่าจะเสร็จ Z"

### 📊 Analytics Frame
ก่อน design telemetry หรือ analytics:
- **Design Question First:** event นี้ตอบคำถาม design อะไร? ถ้าตอบไม่ได้ → อย่าเก็บ
- **Event Naming:** ใช้ `[category].[action].[detail]` format ไหม?
- **Privacy Check:** เก็บ PII ไหม? มี consent + deletion pathway ไหม? (GDPR/CCPA)
- **A/B Test Defined?:** hypothesis + metric + sample size + success criteria กำหนดก่อน launch ไหม?
- **Data Informs, Not Decides:** data แสดง what, ไม่ใช่ why — pair กับ qualitative feedback

---

### 🧪 Prototyping Frame
ก่อน start หรือ evaluate prototype:
- **Hypothesis Written?:** "We believe [X] will [Y]. We'll know when [observable result]." — เขียนก่อน code ไหม?
- **Timebox Set?:** 1h / 4h / 1d / 2d — กำหนดก่อน start ไหม?
- **Minimum Viable?:** code น้อยที่สุดที่ตอบ hypothesis คืออะไร? อย่า build beyond that
- **Prototype ≠ Production:** marked `// PROTOTYPE - NOT FOR PRODUCTION` ไหม?
- **Report Written?:** learned อะไร? recommend adopt/adapt/discard ไหม?

### ♿ Accessibility Frame
ก่อน design หรือ review feature:
- **Contrast Ratio:** text/UI element ≥4.5:1 (normal) หรือ ≥3:1 (large) ไหม? (A-07)
- **Color-Only?:** ใช้ color เป็น sole differentiator ไหม? → เพิ่ม icon/shape/pattern
- **Colorblind Modes:** Protanopia/Deuteranopia/Tritanopia test ทุก mode ไหม?
- **Input Complete?:** keyboard + gamepad + remapping support ครบไหม? (U-03)
- **Text Scaling:** 18px minimum ที่ 1080p, scale ถึง 200% โดยไม่ break layout ไหม?

---

### 🟣 Godot Frame
ก่อน design หรือ implement ใน Godot:
- **Version Confirmed?:** check Godot version ก่อน recommend API — 4.x vs 3.x ต่างกัน
- **Scene Composition:** scene รับผิดชอบอะไร? scene hierarchy ชัดเจนไหม?
- **Signal Direction:** signal ไหลขึ้น (child → parent) ไหม? method call ลงไหม?
- **Static Typing:** ทุก variable/parameter/return type typed ไหม? ไม่มี untyped `var`?
- **Resource for Data:** config data ใน `.tres` Resource ไหม? ไม่ใช่ hardcode?

### 🟦 Unity Frame
ก่อน design หรือ implement ใน Unity:
- **New Input System?:** ใช้ `UnityEngine.InputSystem` ไหม? ไม่ใช่ legacy `Input.GetAxis()`?
- **SRP Configured?:** ใช้ URP/HDRP ไหม? built-in RP มีเหตุผลพิเศษไหม?
- **MonoBehaviour vs DOTS:** entity count เท่าไร? >10,000 → consider DOTS
- **GC Pressure:** `GetComponent<T>()` cache ใน Start/Awake ไหม? ไม่ใช่ per-frame?
- **ScriptableObject Data:** config/event data ใน ScriptableObject ไหม?

### 🔴 Unreal Frame
ก่อน design หรือ implement ใน Unreal:
- **Blueprint vs C++ Boundary:** feature นี้ควรอยู่ใน C++ หรือ Blueprint? ทำไม?
- **Naming Convention:** prefix ถูกไหม? F/E/U/A/I ตรงกับ class type?
- **UPROPERTY/UFUNCTION?:** UObject reference ทั้งหมด marked UPROPERTY ไหม? (GC protection)
- **Server Authority:** feature นี้ต้องการ replication ไหม? client trust issue ไหม?
- **GAS Route?:** stat modification route ผ่าน GameplayEffect ไหม? ไม่ใช่ direct?

---

## การเปลี่ยนแปลงจาก Core Workflow

Game projects เพิ่มข้อกำหนดต่อไปนี้บน core workflow:

### 1. บังคับ FDD ก่อน implement feature ใหม่
ทุก feature ใหม่ที่มี gameplay logic ต้องมี FDD อยู่ใน `doc/08-design/` ก่อน task จะออกจาก `design_validate`

### 2. เพิ่มโฟลเดอร์ `doc/08-design/`
เก็บ Feature Design Documents ทั้งหมด
```
doc/08-design/
  README.md          ← index of all FDDs
  [feature-name].md  ← individual FDD
```

### 3. Task lifecycle สำหรับ game feature
```
todo → design_validate → in_progress → playtest → review → done
```
เพิ่มขั้น `playtest` ระหว่าง implement และ review — ต้องทดสอบ feel จริงก่อน

### 4. Performance budget ต้องระบุก่อน implement
ทุก feature ที่มี real-time logic ต้องระบุ budget ใน FDD:
- Target FPS
- Max ms per frame สำหรับ feature นี้
- Memory budget (ถ้าเกี่ยวข้อง)

---

## สิ่งที่ไม่เปลี่ยนจาก Core

- Source docs versioning — ใช้เหมือนเดิม
- ADR — ใช้เหมือนเดิม (architecture decisions ยังต้องบันทึก)
- Compliance check — ใช้เหมือนเดิม พร้อม game-specific rules เพิ่ม
- Way of work / session protocol — ใช้เหมือนเดิม
- work-status, task-board, log-index — ใช้เหมือนเดิม
