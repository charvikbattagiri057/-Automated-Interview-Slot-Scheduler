"""
AISS - Automated Interview Slot Scheduler
Course: Computational Foundations for AI (25SC1306E)
Concepts: Agent Model (CO1), BFS/Search (CO2), CSP + Backtracking (CO3), Utility Functions (CO4)
"""

from dataclasses import dataclass, field
from typing import Optional
import json
import csv
import os
from collections import deque

from agents import SchedulerAgent
from csp import CSPScheduler
from search import BFSSlotFinder
from utility import UtilityScorer
from models import Candidate, Interviewer, InterviewRound, TimeSlot

# ─────────────────────────────────────────
#  SAMPLE DATA
# ─────────────────────────────────────────

def load_sample_data():
    interviewers = [
        Interviewer("I001", "Dr. Rao",    "Technical", ["Mon-9AM", "Mon-11AM", "Tue-10AM", "Wed-9AM"]),
        Interviewer("I002", "Ms. Priya",  "HR",        ["Mon-10AM", "Tue-9AM", "Tue-11AM", "Thu-10AM"]),
        Interviewer("I003", "Mr. Arjun",  "Technical", ["Mon-9AM", "Wed-10AM", "Thu-9AM", "Fri-11AM"]),
        Interviewer("I004", "Ms. Kavya",  "Managerial",["Tue-10AM", "Wed-11AM", "Thu-10AM", "Fri-9AM"]),
    ]

    candidates = [
        Candidate("C001", "Charvik",   ["HR", "Technical"],          ["Mon-9AM", "Mon-10AM", "Tue-10AM"]),
        Candidate("C002", "Aditya",    ["HR", "Technical"],          ["Mon-11AM", "Tue-9AM", "Wed-9AM"]),
        Candidate("C003", "Riya",      ["HR", "Managerial"],         ["Tue-10AM", "Wed-10AM", "Thu-10AM"]),
        Candidate("C004", "Sai",       ["Technical", "Managerial"],  ["Mon-9AM", "Wed-11AM", "Fri-9AM"]),
        Candidate("C005", "Meena",     ["HR", "Technical"],          ["Tue-11AM", "Thu-9AM", "Fri-11AM"]),
    ]

    rounds = [
        InterviewRound("R1", "HR",         30),
        InterviewRound("R2", "Technical",  45),
        InterviewRound("R3", "Managerial", 30),
    ]

    return interviewers, candidates, rounds


# ─────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────

def main():
    print("=" * 60)
    print("  AISS — Automated Interview Slot Scheduler")
    print("  CFAI Project | KL University")
    print("=" * 60)

    interviewers, candidates, rounds = load_sample_data()

    # CO1: Agent perceives environment and formulates problem
    agent = SchedulerAgent(interviewers, candidates, rounds)
    agent.perceive()
    agent.formulate_problem()

    # CO2: BFS to find reachable valid slots
    bfs = BFSSlotFinder(interviewers, candidates)
    reachable_slots = bfs.find_all_reachable_slots()
    print(f"\n[BFS] Reachable slot combinations explored: {bfs.nodes_explored}")

    # CO3: CSP backtracking to assign slots
    csp = CSPScheduler(interviewers, candidates, rounds)
    schedule = csp.solve()

    if not schedule:
        print("\n[CSP] No valid schedule found. Check availability constraints.")
        return

    print(f"\n[CSP] Solution found after {csp.backtracks} backtracks.\n")

    # CO4: Score each assignment with utility function
    scorer = UtilityScorer()
    scored = scorer.score_all(schedule)

    # Print final schedule
    print("\n" + "=" * 60)
    print("  FINAL INTERVIEW SCHEDULE")
    print("=" * 60)
    for entry in scored:
        print(f"  {entry['candidate']:<12} | {entry['round']:<12} | {entry['interviewer']:<14} | "
              f"Slot: {entry['slot']:<12} | Score: {entry['score']}/10")

    print("\n[Reasoning Trace]")
    csp.print_trace()

    # Export outputs
    export_json(scored)
    export_csv(scored)
    print("\n[Output] schedule.json and schedule.csv saved.")


def export_json(data):
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/schedule.json", "w") as f:
        json.dump(data, f, indent=2)


def export_csv(data):
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/schedule.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    main()
