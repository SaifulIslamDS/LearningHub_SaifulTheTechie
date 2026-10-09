"""Phase 3 · ETL/ELT · Replayable pipeline and change data capture (CDC).

Replays a small deterministic CDC log with create/update/delete events against
the 2025 order snapshot. The event sequence ends by restoring the source state,
so the shared known answers stay unchanged.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pandas as pd

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "data" / "orders_2025.csv"
EVENTS = HERE / "data" / "orders_cdc_events.jsonl"
RESULTS = HERE / "results" / "cdc_replay"
CHECKPOINT = RESULTS / "checkpoint.json"


def load_events() -> list[dict[str, Any]]:
    return [json.loads(line) for line in EVENTS.read_text(encoding="utf-8").splitlines() if line.strip()]


def base_state() -> dict[int, dict[str, Any]]:
    df = pd.read_csv(SOURCE)
    return {int(row["order_id"]): row for row in df.to_dict(orient="records")}


def apply_event(state: dict[int, dict[str, Any]], event: dict[str, Any]) -> None:
    order_id = int(event["key"]["order_id"])
    op = event["op"]
    if op in {"c", "u"}:
        state[order_id] = event["after"]
    elif op == "d":
        state.pop(order_id, None)
    else:
        raise ValueError(f"unsupported CDC op: {op}")


def replay(events: list[dict[str, Any]], stop_after: int | None = None) -> tuple[dict[int, dict[str, Any]], int]:
    state = base_state()
    last_sequence = 0
    for event in events:
        if stop_after is not None and int(event["sequence"]) > stop_after:
            break
        apply_event(state, event)
        last_sequence = int(event["sequence"])
    return state, last_sequence


def resume(state: dict[int, dict[str, Any]], events: list[dict[str, Any]], after_sequence: int) -> dict[int, dict[str, Any]]:
    for event in events:
        if int(event["sequence"]) > after_sequence:
            apply_event(state, event)
    return state


def to_frame(state: dict[int, dict[str, Any]]) -> pd.DataFrame:
    columns = pd.read_csv(SOURCE, nrows=0).columns.tolist()
    return pd.DataFrame(state.values(), columns=columns).sort_values("order_id").reset_index(drop=True)


def source_match(df: pd.DataFrame) -> bool:
    source = pd.read_csv(SOURCE).sort_values("order_id").reset_index(drop=True)
    # CDC JSON turns missing numeric values into None; normalise via pandas before comparison.
    return source.fillna("<NA>").astype(str).equals(df.fillna("<NA>").astype(str))


def net_revenue(df: pd.DataFrame) -> float:
    revenue = pd.to_numeric(df["revenue"])
    return round(revenue[df["status"] != "Cancelled"].sum(), 2)


def main() -> None:
    shutil.rmtree(RESULTS, ignore_errors=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    events = load_events()

    counts = {op: sum(e["op"] == op for e in events) for op in ("c", "u", "d")}
    print(f"CDC log: {len(events)} events | create {counts['c']} | update {counts['u']} | delete {counts['d']}")

    full_state, last = replay(events)
    full = to_frame(full_state)
    print(f"full replay: sequence {last} | rows {len(full)} | source match {source_match(full)} | net revenue {net_revenue(full):.2f}")

    crashed_state, checkpoint = replay(events, stop_after=3)
    CHECKPOINT.write_text(json.dumps({"last_sequence": checkpoint}, sort_keys=True) + "\n", encoding="utf-8")
    print(f"simulated crash: checkpoint {checkpoint} | rows {len(crashed_state)}")

    resumed = to_frame(resume(crashed_state, events, checkpoint))
    print(f"resume: rows {len(resumed)} | matches full replay {source_match(resumed)} | net revenue {net_revenue(resumed):.2f}")

    second_state, _ = replay(events)
    second = to_frame(second_state)
    print(f"replay again from immutable base: rows {len(second)} | identical result {source_match(second)}")


if __name__ == "__main__":
    main()
