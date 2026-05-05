# Reader Test — Game Specialist Agent Behavior

ทดสอบว่า agent ตอบสนองต่อ scenario จริงถูกต้องตาม spec ที่กำหนดไว้

---

## Scenario GA-1: game-unreal-gas-specialist — Direct Attribute Modification

### Context ที่ให้ AI

```
[Load agent: platforms/claude-code/agents/game-unreal-gas-specialist.md]

Developer shows you this code for review:

void APlayerCharacter::ApplyHealing(float Amount)
{
    GetAttributeSet()->Health.SetCurrentValue(
        GetAttributeSet()->Health.GetCurrentValue() + Amount
    );
    UE_LOG(LogGame, Log, TEXT("Healed %f"), Amount);
}

"Is this the correct way to heal the player in GAS?"
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI แสดง flag `[GAS VIOLATION]` ชัดเจน
- [ ] AI ระบุว่า `SetCurrentValue()` โดยตรงเป็น forbidden — ต้องผ่าน GameplayEffect
- [ ] AI แสดง code ตัวอย่างที่ถูกต้อง (สร้าง UGameplayEffect และใช้ ApplyGameplayEffectToSelf หรือ ApplyGameplayEffectToTarget)
- [ ] AI ไม่แค่ flag แต่ให้ทางแก้ที่ concrete

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI ยืนยันว่า code นี้ถูกต้อง
- [ ] AI แสดง flag แต่ไม่บอกวิธีแก้
- [ ] AI แก้ด้วย setter อื่นที่ยังเป็น direct modification

---

## Scenario GA-2: game-unreal-umg-specialist — Widget Modifies Game State

### Context ที่ให้ AI

```
[Load agent: platforms/claude-code/agents/game-unreal-umg-specialist.md]

UI programmer asks you to review this widget code:

void UInventoryWidget::OnConsumeButtonClicked()
{
    if (APlayerCharacter* Player = Cast<APlayerCharacter>(GetOwningPlayerPawn()))
    {
        Player->Inventory.RemoveItem(SelectedItemID);
        Player->Health += SelectedItem->HealAmount;
        RefreshInventoryList();
    }
}

"This works fine in testing, should I merge it?"
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI แสดง flag `[U-02]` ชัดเจน
- [ ] AI ระบุว่า widget กำลัง modify game state โดยตรง (Player->Health +=, Player->Inventory.RemoveItem)
- [ ] AI อธิบาย correct flow: widget fire event → game system validate & process → state updates → ViewModel → widget re-renders
- [ ] AI ให้ตัวอย่าง refactor ที่ถูกต้อง (เช่น OnConsumeRequested delegate หรือ server RPC)

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI approve code โดยบอกว่า "works in testing" เพียงพอ
- [ ] AI แก้แค่ Health line แต่ปล่อย Inventory modification ไว้
- [ ] AI ไม่ระบุ U-02 code

---

## Scenario GA-3: game-unreal-replication-specialist — Client Sends Unvalidated Position

### Context ที่ให้ AI

```
[Load agent: platforms/claude-code/agents/game-unreal-replication-specialist.md]

Multiplayer feature code for review:

// Called on client, runs on server
UFUNCTION(Server, Reliable)
void ServerTeleportTo(FVector NewLocation);

void AMyCharacter::ServerTeleportTo_Implementation(FVector NewLocation)
{
    SetActorLocation(NewLocation);
    ClientConfirmTeleport();
}

"We need fast teleport for our ability system. This looks correct?"
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI แสดง flag `[SECURITY]` ชัดเจน
- [ ] AI ระบุว่า client ส่ง FVector มาและ server apply โดยไม่ validate — เปิดช่องให้ client teleport ไปที่ใดก็ได้
- [ ] AI ระบุว่าต้อง validate: distance from current position, is target location valid/reachable, ability cooldown, server-side authority check
- [ ] AI แสดง code ที่ถูกต้องพร้อม validation

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI approve โดยไม่ตั้งคำถามเรื่อง validation
- [ ] AI แนะนำให้ validate แค่ distance แต่ไม่พูดถึง ability authorization

---

## Scenario GA-4: game-godot-gdscript-specialist — Untyped Code Review

### Context ที่ให้ AI

```
[Load agent: platforms/claude-code/agents/game-godot-gdscript-specialist.md]

Code review request for player health system:

extends Node

var health = 100
var max_health = 100
var is_dead = false

func take_damage(amount):
    health -= amount
    if health <= 0:
        is_dead = true
        emit_signal("player_died")

func heal(amount):
    health = min(health + amount, max_health)

"Ready to merge to main branch?"
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI flag `[TYPING VIOLATION]` สำหรับทุก untyped declaration
- [ ] AI ระบุบรรทัดที่มีปัญหา: `var health = 100`, `var max_health = 100`, `var is_dead = false`, `func take_damage(amount):`, `func heal(amount):`
- [ ] AI แสดง corrected code พร้อม type annotations ครบ
- [ ] AI ระบุว่า `emit_signal("player_died")` ควรใช้ typed signal: `signal player_died()` และ `player_died.emit()`

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI approve code โดยบอกว่า "works correctly"
- [ ] AI แก้เฉพาะบางบรรทัด ปล่อยบรรทัดอื่นไม่ typed

---

## Scenario GA-5: game-narrative-director — Dialogue Function Test

### Context ที่ให้ AI

```
[Load agent: platforms/claude-code/agents/game-narrative-director.md]

Writer submits this dialogue for Scene 3 — player meets the merchant for the first time:

MERCHANT: "Hello there, traveler."
PLAYER: [nod]
MERCHANT: "It's a nice day, isn't it?"
PLAYER: [nod]
MERCHANT: "The weather has been quite pleasant."
MERCHANT: "I've been selling goods here for 20 years."
MERCHANT: "My father sold goods here before me."

"Does this dialogue work for the introduction scene?"
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI ใช้ Dialogue Function Test กับทุกบรรทัด
- [ ] AI ระบุ lines ที่ล้มเลหลว ("nice day", "pleasant weather" — ไม่ reveal character, ไม่ advance plot, ไม่ deliver info, ไม่ create mood)
- [ ] AI ชี้ให้เห็นว่า Player ไม่มี meaningful choice
- [ ] AI เสนอ alternative dialogue direction พร้อมตัวอย่าง 2-3 ตัวเลือก voice

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI approve dialogue โดยไม่ apply dialogue function test
- [ ] AI แค่บอกว่า "feels generic" โดยไม่ reference framework

---

## Scenario GA-6: game-unity-dots-specialist — Managed Type in Burst

### Context ที่ให้ AI

```
[Load agent: platforms/claude-code/agents/game-unity-dots-specialist.md]

Performance optimization code for review:

[BurstCompile]
public partial struct SpawnEnemySystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        var enemies = new List<EnemyData>();
        
        foreach (var (transform, health) in 
            SystemAPI.Query<RefRW<LocalTransform>, RefRO<HealthComponent>>())
        {
            if (health.ValueRO.Current <= 0)
            {
                string deathMessage = $"Enemy died at {transform.ValueRO.Position}";
                Debug.Log(deathMessage);
                enemies.Add(new EnemyData { Position = transform.ValueRO.Position });
            }
        }
    }
}

"This uses Burst for performance, right?"
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI แสดง flag `[BURST INCOMPATIBLE]` สำหรับ `List<EnemyData>` (managed type)
- [ ] AI flag `string deathMessage` และ `Debug.Log` ว่า managed type ใน Burst context
- [ ] AI อธิบาย: ต้องใช้ `NativeList<EnemyData>` แทน `List<>`; ย้าย Debug.Log ออกไปนอก Burst context
- [ ] AI แสดง corrected code ที่ Burst-compatible

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI ยืนยันว่า code นี้ Burst-compatible เพราะมี `[BurstCompile]` attribute
- [ ] AI แก้แค่ List เป็น NativeList แต่ปล่อย Debug.Log ไว้

---

## Scenario GA-7: Cross-Agent Boundary — UMG Specialist Asked About Art Style

### Context ที่ให้ AI

```
[Load agent: platforms/claude-code/agents/game-unreal-umg-specialist.md]

"I need help with the visual styling of our inventory widget — 
what color palette should we use, and what font size looks good 
for the item names? Also can you create the pixel art icons for 
the items?"
```

### สิ่งที่ต้องเกิดขึ้น (ผ่าน)

- [ ] AI ระบุชัดเจนว่า visual styling, color palette, และ art asset creation อยู่นอก scope ของ UMG specialist
- [ ] AI redirect ไปยัง `game-art-director` สำหรับ color palette และ visual style
- [ ] AI redirect ไปยัง `game-ux-designer` สำหรับ typography/font decisions
- [ ] AI อธิบายสิ่งที่ตัวเองทำได้: widget hierarchy, data binding, CommonUI input routing

### สิ่งที่ต้องไม่เกิดขึ้น (fail ถ้าเกิด)

- [ ] AI ตอบคำถามเรื่อง color palette หรือ font เอง
- [ ] AI พยายาม create art assets
- [ ] AI ไม่ redirect ไปยัง agent ที่ถูกต้อง
