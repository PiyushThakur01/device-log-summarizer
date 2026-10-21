"""Section 2: Device Log Summarizer CLI."""
import argparse
import csv
import json
import sys
from collections import defaultdict

VALID_STATUSES = {"ACTIVE", "WARNING", "ERROR"}


def read_records(path):
    """Yield (device_id, status, temperature); skip and count bad rows."""
    records, skipped = [], 0
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"device_id", "status", "temperature"}
        if not reader.fieldnames or not required <= set(reader.fieldnames):
            raise ValueError(f"CSV must contain columns: {sorted(required)}")
        for row in reader:
            device = (row["device_id"] or "").strip()
            status = (row["status"] or "").strip().upper()
            try:
                temp = float(row["temperature"])
            except (TypeError, ValueError):
                skipped += 1
                continue
            if not device or status not in VALID_STATUSES or temp != temp:
                skipped += 1
                continue
            records.append((device, status, temp))
    return records, skipped


def aggregate(records, max_avg_temp=80.0):
    groups = defaultdict(list)
    for device, status, temp in records:
        groups[device].append((status, temp))
    results = []
    for device, items in sorted(groups.items()):
        avg = sum(t for _, t in items) / len(items)
        if avg > max_avg_temp:
            continue
        results.append({
            "device_id": device,
            "total_records": len(items),
            "avg_temperature": round(avg, 2),
            "error_count": sum(1 for s, _ in items if s == "ERROR"),
        })
    return results


def print_table(results):
    print(f"{'Device':<10}{'Records':>9}{'Avg Temp':>11}{'Errors':>8}")
    print("-" * 38)
    for r in results:
        print(f"{r['device_id']:<10}{r['total_records']:>9}{r['avg_temperature']:>11.2f}{r['error_count']:>8}")


def main():
    p = argparse.ArgumentParser(description="Summarize device telemetry CSV.")
    p.add_argument("csv_path", nargs="?", default="device_telemetry.csv")
    p.add_argument("-o", "--output", default="summary.json")
    p.add_argument("--max-avg", type=float, default=80.0)
    args = p.parse_args()
    try:
        records, skipped = read_records(args.csv_path)
    except FileNotFoundError:
        sys.exit(f"Error: file not found: {args.csv_path}")
    except (ValueError, OSError) as e:
        sys.exit(f"Error: {e}")
    results = aggregate(records, args.max_avg)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print_table(results)
    print(f"\nSkipped {skipped} bad row(s). Saved {len(results)} device(s) to {args.output}")


if __name__ == "__main__":
    main()
