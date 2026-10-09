---
title: Replayable Pipelines and Change Data Capture
order: 2
summary: Capture inserts, updates and deletes as ordered events, then replay or resume them without losing the source-of-truth
  sequence.
level: Intermediate
time: 45 min
topics:
- Replayability
- CDC
prerequisites:
- phase-3/etl-elt/01-modular-idempotent-incremental
keywords:
- replayable pipeline
- replayability
- cdc
- change data capture
- event log
- checkpoint
- logical decoding
- debezium
reviewed: 2026-10-09
files:
- phase-3/data-engineering-scripts.zip
- phase-3/orders_cdc_events.jsonl
resources:
- title: Debezium documentation
  url: https://debezium.io/documentation/reference/stable/
  source: Debezium
  note: Official Debezium 3.6 documentation for row-level change event streams.
- title: Debezium connector for PostgreSQL
  url: https://debezium.io/documentation/reference/stable/connectors/postgresql.html
  source: Debezium
  note: Explains snapshots, logical decoding, replication slots and insert/update/delete events.
- title: Logical Decoding Concepts
  url: https://www.postgresql.org/docs/current/logicaldecoding-explanation.html
  source: PostgreSQL
  note: Official PostgreSQL 18 explanation of turning WAL changes into a replayable logical stream.
- title: Change data capture in dbt
  url: https://docs.getdbt.com/best-practices/how-we-handle-cdc/1-intro
  source: dbt Developer Hub
  note: Shows how new, updated and deleted source rows relate to incremental models and snapshots.
youtube:
  title: Change Data Capture and Debezium with Gunnar Morling
  creator: 'The GeekNarrator (guest: Gunnar Morling)'
  url: https://www.youtube.com/watch?v=VGH6TlhEJpM&t=500s
  video_id: VGH6TlhEJpM
  start_seconds: 500
  language: English
  level: Intermediate
  reviewed: '2026-10-09'
  why_recommended: Gunnar Morling explains the CDC mental model and Debezium architecture. Use it to understand how database
    changes become an ordered event stream, then return to this lesson to practise deterministic replay and checkpoint/resume
    behaviour locally.
  timestamps:
  - label: What is Change Data Capture?
    time: 08:20
    url: https://www.youtube.com/watch?v=VGH6TlhEJpM&t=500s
  - label: What is Debezium and how does it approach CDC?
    time: '12:20'
    url: https://www.youtube.com/watch?v=VGH6TlhEJpM&t=740s
  - label: Debezium architecture
    time: '18:00'
    url: https://www.youtube.com/watch?v=VGH6TlhEJpM&t=1080s
---

## What is it?

A pipeline is **replayable** when you can rebuild the same state from a known starting point plus the same ordered inputs. This is useful after a bad deployment, a corrupted target, a changed transformation rule, or a partial failure.

**Change data capture (CDC)** records row-level changes such as:

- `c` — create / insert
- `u` — update
- `d` — delete

Instead of repeatedly scanning an entire source table, a CDC system reads the change stream and applies those events downstream in order.

!!! job "Why it matters at work"
    Incremental timestamps can miss deletes and can miss updates when the source does not maintain a reliable `updated_at`. CDC captures the operations themselves. Production systems such as Debezium can read database transaction logs and publish change events for downstream pipelines. A data engineer must also know how to recover: keep an ordered offset/checkpoint, make consumers safe to resume, and preserve enough raw history to replay.

The practice files are `15_cdc_replay.py` and `data/orders_cdc_events.jsonl`. The tiny event log is generated deterministically by `tools/make_phase3b_etl_data.py` with seed **2026**.

## Step 1: understand a CDC event

Our practice events use a simplified shape inspired by production CDC envelopes:

```json
{
  "event_id": "evt-001",
  "sequence": 1,
  "op": "u",
  "key": {"order_id": 10521},
  "before": {"status": "Delivered", "...": "..."},
  "after": {"status": "Cancelled", "...": "..."}
}
```

The full practice event stores the complete before/after row. The important fields are:

| Field | Why it exists |
|---|---|
| `event_id` | Stable identity for deduplication/auditing |
| `sequence` | Ordered position used for replay/checkpointing |
| `op` | What happened: create, update or delete |
| `key` | Which business row changed |
| `before` / `after` | Old and new row images |
| `ts_ms` | Source/event time metadata |

Real CDC formats vary. Debezium events similarly carry operation metadata plus `before` and `after` row data for changes.

## Step 2: apply each event deterministically

The consumer applies events by key:

```python
def apply_event(state, event):
    order_id = int(event["key"]["order_id"])
    op = event["op"]

    if op in {"c", "u"}:
        state[order_id] = event["after"]
    elif op == "d":
        state.pop(order_id, None)
    else:
        raise ValueError(f"unsupported CDC op: {op}")
```

Our generated log contains all three operations:

```text
CDC log: 6 events | create 1 | update 4 | delete 1
```

The six events are intentionally reversible: two temporary business-row changes are later restored, and one temporary row is inserted then deleted. That lets the final state reconcile exactly to the shared 2025 source.

## Step 3: replay from an immutable starting point

A replay starts from the same base snapshot and applies events in sequence:

```python
def replay(events):
    state = base_state()
    for event in events:
        apply_event(state, event)
    return state
```

Real output:

```text
full replay: sequence 6 | rows 4246 | source match True | net revenue 5478357.79
```

This is the key property: given the same base snapshot and same ordered event log, we can rebuild the same result. The known answers still hold: **4,246 orders and BDT 5,478,357.79 net revenue**.

Do not confuse **replayability** with blindly applying old events to any current table. A replay needs a defined starting state and event range. In production, that might be a snapshot plus a Kafka offset, database log sequence number (LSN), or another durable position.

## Step 4: checkpoint only completed progress

Now the script simulates a failure after event 3. At that moment the temporary inserted order exists:

```text
simulated crash: checkpoint 3 | rows 4247
```

The checkpoint says: *events 1–3 were applied successfully*. On restart, the consumer applies only events with a larger sequence:

```python
def resume(state, events, after_sequence):
    for event in events:
        if int(event["sequence"]) > after_sequence:
            apply_event(state, event)
    return state
```

Real output:

```text
resume: rows 4246 | matches full replay True | net revenue 5478357.79
```

The resumed result equals the full replay. This is why checkpoints belong **after successful processing**, just like the watermark in the previous lesson.

## Step 5: prove the run is replayable

The script discards the rebuilt state, starts again from the immutable base snapshot, and replays the same six events:

```text
replay again from immutable base: rows 4246 | identical result True
```

A production-quality replay design normally keeps:

- immutable raw/snapshot inputs for the required retention period;
- ordered change events or a source log position;
- deterministic transformation code/version;
- a checkpoint/offset committed after successful writes;
- idempotent target writes or processed-event tracking;
- reconciliation checks after recovery.

## CDC in a real PostgreSQL pipeline

PostgreSQL can expose committed row changes through **logical decoding** of its write-ahead log (WAL). A tool such as Debezium can take an initial consistent snapshot and then continuously capture inserts, updates and deletes, tracking its position with PostgreSQL replication/log offsets.

A common architecture is:

```text
PostgreSQL WAL
    ↓ logical decoding
Debezium connector
    ↓ change events
Kafka topic / durable event stream
    ↓ consumer
warehouse / lakehouse / search index / cache
```

This architecture is **shown for reference; not executed for this lesson**. The local exercise focuses on the core mechanics—ordered change events, replay and checkpoint recovery—without requiring Kafka or a database replication slot.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Treating CDC as "only new rows" | Updates and deletes are ignored | Handle create, update and delete operations explicitly |
| Saving a checkpoint before target writes finish | A restart skips uncommitted events | Commit the checkpoint only after successful processing |
| Replaying events without a defined starting snapshot | Results depend on whatever target state happens to exist | Pair replay with a known snapshot/base and event range |
| Losing event order for the same business key | Older values can overwrite newer ones | Preserve source ordering/offset semantics |
| Dropping the raw event history too early | You cannot reconstruct or audit past state | Set a retention policy based on recovery and audit needs |

## Try it yourself

**Task:** Extend `15_cdc_replay.py` with a `processed_event_ids` set. Before applying an event, skip it if its `event_id` was already processed. This models an extra idempotency layer for a consumer that can receive duplicate deliveries.

<details markdown="1">
<summary>Show a hint</summary>

Check `event["event_id"]` before `apply_event(...)`, then add the ID only after the event has been applied successfully.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```python
processed_event_ids = set()

for event in events:
    event_id = event["event_id"]
    if event_id in processed_event_ids:
        continue
    apply_event(state, event)
    processed_event_ids.add(event_id)
```

In a real service, store this state durably or use a transactional sink/offset design; an in-memory set disappears on restart.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What does CDC capture that a simple "new rows after this date" filter may miss?

1. Updates and deletes
2. Python package versions
3. Dashboard colours

<details markdown="1"><summary>Show answer</summary>
**A.** CDC represents row-level changes, including updates and deletes.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What makes a pipeline replayable?

1. It can rebuild a deterministic result from a known starting point and ordered inputs
2. It runs only once
3. It never stores checkpoints

<details markdown="1"><summary>Show answer</summary>
**A.** Replay requires defined inputs, ordering and deterministic processing.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. When should a CDC consumer commit its checkpoint or offset?

1. Before applying the event
2. After the corresponding target work succeeds
3. Once per year

<details markdown="1"><summary>Show answer</summary>
**B.** Otherwise the consumer can skip work after a crash.
</details>
</div>

## Summary

- **CDC** captures row-level creates, updates and deletes instead of repeatedly scanning a whole source.
- A **replayable** pipeline can rebuild the same state from a known base plus the same ordered change events.
- Store a durable **checkpoint/offset** only after downstream work succeeds.
- Preserve event order, stable keys and enough immutable history to recover.
- The local replay and crash/resume both reconcile back to 4,246 orders and BDT 5,478,357.79 net revenue.

!!! job "Job-ready check"
    **Interview question:** *"What is CDC, and how would you recover a CDC consumer after a failure?"*

    **Strong answer:** "CDC captures source row changes—insert, update and delete—from a change-tracking mechanism or transaction log. I would consume events in source order, write them idempotently to the target by business key, and commit the source offset only after the target write succeeds. If the consumer fails, it resumes from the last committed offset. For a full rebuild, I need a known base snapshot plus retained events from the corresponding log position, then I replay deterministically and reconcile the result."

    **Mini project:** Run PostgreSQL locally, enable logical replication, configure a Debezium PostgreSQL connector and capture changes from an `orders` table into Kafka. Insert, update and delete one order, then show the three CDC operations. This extension is not required for the local lesson because it needs PostgreSQL, Kafka Connect and a broker.
