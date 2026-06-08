# Gate YAML Grammar (P1-1)

gate = `trigger → requires[predicate] → effect` · evaluated against **real state** (git/file/test), ไม่เชื่อ agent claim

```yaml
id: string                    # required, unique (เช่น task_close_gate)
version: int                  # rule version (pin per entity, ADR migration)
description: string
trigger:                      # อะไรกระตุ้น gate
  action: string              # เช่น commit | task.transition | tool:mark_task_done
  to: string?                 # target state (transition เท่านั้น)
risk_level: 0|1|2|3           # ADR-008 — กำหนด effect default ถ้าไม่ override
requires:                     # predicate list (AND) — ทั้งหมดต้องผ่าน
  - check: string             # ชื่อ predicate ใน resolver vocabulary
    <args>: ...               # args ของ predicate นั้น
    class: machine|attested   # machine=Engine ตรวจ deterministic · attested=ตรวจ presence (ADR-009 D2)
on_fail:
  effect: warn|block|decision-inbox|hard-stop   # map กับ risk: L1→warn/log, L2→inbox, L3→hard-stop
  message: string             # remediation — บอก agent ว่าขาดอะไร (กัน thrash)
on_pass:                      # optional side-effects (P2+)
  - do: string
```

## Predicate vocabulary (resolver) — vetted, fixed set (ขยายโดย engineer)
| check | args | class | ตรวจอะไร |
|-------|------|-------|---------|
| `file_exists` | path | machine | ไฟล์มีอยู่ |
| `placeholder_absent` | patterns[] | machine | ไม่มี `<PLACEHOLDER>` ค้าง |
| `secret_absent` | patterns[] | machine | ไม่มี hardcoded secret (C-11) |
| `git_staged_clean_of` | glob | machine | staged diff ไม่มีไฟล์ตาม glob (เช่น docs dirty) |
| `git_committed` | — | machine | มี commit สำหรับ change |
| `entry_exists` | file, key | machine | grep key ในไฟล์ (เช่น work-log มี task id) |
| `evidence_count_gte` | task, n | machine | evidence ≥ n |
| `human_signoff` | ref | attested | มี sign-off record (presence) |

> args ใช้ `$args.x` อ้าง trigger args · resolver = Python function ที่ test แล้ว (P1-2)
