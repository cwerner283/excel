"""Incident summarizer for Harrison County Sheriff's Academy."""

import argparse
import csv
from collections import Counter
from typing import List, Tuple

try:
    from tabulate import tabulate
except ImportError:  # fallback if tabulate is unavailable
    tabulate = None


def load_incidents(csv_path: str) -> List[dict]:
    """Load incident records from a CSV file."""
    with open(csv_path, newline='', encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def breakdown_by_type(incidents: List[dict]) -> List[Tuple[str, int]]:
    """Return a list of (IncidentType, count) sorted by count descending."""
    counts = Counter(inc["IncidentType"] for inc in incidents)
    return sorted(counts.items(), key=lambda item: item[1], reverse=True)


def average_officers(incidents: List[dict]) -> float:
    """Calculate the average number of officers per incident."""
    officers = []
    for inc in incidents:
        try:
            officers.append(int(inc.get("Officers", 0)))
        except ValueError:
            continue
    return round(sum(officers) / len(officers), 2) if officers else 0.0


def busiest_day(incidents: List[dict]) -> Tuple[str, List[str]]:
    """Return the busiest day and a list of incident types that occurred."""
    day_counts = Counter(inc["Date"] for inc in incidents)
    busiest = day_counts.most_common(1)[0][0]
    types = sorted(
        {
            inc["IncidentType"]
            for inc in incidents
            if inc["Date"] == busiest
        }
    )
    return busiest, types


def format_table(headers: List[str], rows: List[Tuple]) -> str:
    """Format rows as a table. Use tabulate if available."""
    if tabulate:
        return tabulate(rows, headers=headers, tablefmt="github")

    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    header = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    separator = "-+-".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        line = " | ".join(
            str(cell).ljust(widths[i]) for i, cell in enumerate(row)
        )
        lines.append(line)
    return "\n".join(lines)


def main() -> None:
    """Script entry point."""
    parser = argparse.ArgumentParser(
        description="Summarize incidents for Harrison County Sheriff's Academy"
    )
    parser.add_argument(
        "csv_file",
        nargs="?",
        default="incidents.csv",
        help="Path to the CSV file (default: incidents.csv)",
    )
    args = parser.parse_args()

    incidents = load_incidents(args.csv_file)

    print(f"Total incidents: {len(incidents)}")

    breakdown = breakdown_by_type(incidents)
    print("\nIncident Type Breakdown:")
    print(format_table(["IncidentType", "Count"], breakdown))

    avg = average_officers(incidents)
    print(f"\nAverage officers per incident: {avg:.2f}")

    day, types = busiest_day(incidents)
    print(f"\nBusiest day: {day}")
    print("Incident types:")
    for t in types:
        print(f" - {t}")


if __name__ == "__main__":
    main()
