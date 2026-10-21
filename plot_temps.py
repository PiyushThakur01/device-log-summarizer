"""Section 3: bar chart of average temperature per device."""
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main(json_path="summary.json", out_path="avg_temperature.png"):
    try:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        sys.exit(f"Error reading {json_path}: {e}")
    if not data:
        sys.exit("No devices to plot.")

    devices = [d["device_id"] for d in data]
    temps = [d["avg_temperature"] for d in data]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(devices, temps, color="steelblue")
    ax.bar_label(bars, fmt="%.1f", padding=3)
    ax.set_title("Average Temperature per Device")
    ax.set_xlabel("Device ID")
    ax.set_ylabel("Average Temperature (°C)")
    ax.set_ylim(0, max(temps) * 1.15)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    print(f"Saved chart to {out_path}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
