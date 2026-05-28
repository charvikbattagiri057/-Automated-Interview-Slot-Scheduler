"""
utility.py — Utility Scorer (CO4)
Scores each interview assignment based on:
  1. Preference alignment  (+4) — slot is in candidate's preferred list
  2. Expertise match       (+3) — interviewer expertise = round type (always true here)
  3. Early slot bonus      (+2) — earlier in week = higher score
  4. Load balance          (+1) — interviewer with fewer assignments scores higher
"""

from typing import List, Dict


DAYS_ORDER = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4}
TIMES_ORDER = {"9AM": 0, "10AM": 1, "11AM": 2, "12PM": 3, "2PM": 4}


class UtilityScorer:
    def __init__(self):
        self.interviewer_load: Dict[str, int] = {}

    def slot_rank(self, slot: str) -> int:
        """Lower rank = earlier slot = higher utility."""
        parts = slot.split("-")
        if len(parts) != 2:
            return 99
        day, time = parts
        return DAYS_ORDER.get(day, 9) * 10 + TIMES_ORDER.get(time, 9)

    def score(self, entry: dict, all_entries: List[dict]) -> float:
        total = 0.0

        # 1. Preference alignment
        if entry.get("preferred", False):
            total += 4.0

        # 2. Expertise match (always true from CSP constraints, give base score)
        total += 3.0

        # 3. Early slot bonus (scale 0–2)
        rank = self.slot_rank(entry.get("slot", ""))
        early_score = max(0, 2.0 - rank * 0.1)
        total += round(early_score, 1)

        # 4. Load balance — fewer assignments to this interviewer = +1
        iv_id = entry.get("interviewer_id", "")
        load = sum(1 for e in all_entries if e.get("interviewer_id") == iv_id)
        if load <= 2:
            total += 1.0

        return round(min(total, 10.0), 1)

    def score_all(self, schedule: List[dict]) -> List[dict]:
        print("\n[Utility] Scoring all assignments...")
        for entry in schedule:
            entry["score"] = self.score(entry, schedule)
            pref_label = "✓ preferred" if entry["preferred"] else "  not preferred"
            print(f"  {entry['candidate']:<10} | {entry['round']:<12} | "
                  f"Slot: {entry['slot']:<10} | {pref_label} | Score: {entry['score']}/10")
        return schedule
