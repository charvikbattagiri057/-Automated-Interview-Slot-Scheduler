"""
agents.py — SchedulerAgent (CO1)
PEAS Model:
  Performance : Maximize valid, conflict-free scheduled interviews
  Environment : Interviewers (availability), Candidates (preferences), Rounds
  Actuators   : Assign slots, flag conflicts, output schedule
  Sensors     : Read interviewer/candidate data, detect overlaps
"""

from models import Candidate, Interviewer, InterviewRound
from typing import List


class SchedulerAgent:
    def __init__(
        self,
        interviewers: List[Interviewer],
        candidates: List[Candidate],
        rounds: List[InterviewRound]
    ):
        self.interviewers = interviewers
        self.candidates = candidates
        self.rounds = rounds
        self.state = {}   # current world state
        self.trace = []   # reasoning log

    # ── SENSOR: perceive the environment ──────────────────────────
    def perceive(self):
        print("\n[Agent] Perceiving environment...")

        total_slots = set()
        for iv in self.interviewers:
            total_slots.update(iv.available_slots)
        for cd in self.candidates:
            total_slots.update(cd.preferred_slots)

        self.state = {
            "interviewers": len(self.interviewers),
            "candidates": len(self.candidates),
            "rounds": len(self.rounds),
            "unique_slots": len(total_slots),
            "slot_universe": sorted(total_slots),
        }

        print(f"  Interviewers : {self.state['interviewers']}")
        print(f"  Candidates   : {self.state['candidates']}")
        print(f"  Rounds       : {self.state['rounds']}")
        print(f"  Unique Slots : {self.state['unique_slots']}")
        print(f"  Slot Universe: {self.state['slot_universe']}")

        self.trace.append("PERCEIVE: environment read successfully.")

    # ── FORMULATE: define state space and goals ────────────────────
    def formulate_problem(self):
        print("\n[Agent] Formulating problem as state space...")

        print(f"\n  State       : (candidate, round) → (interviewer, slot)")
        print(f"  Actions     : assign_slot(candidate, round, interviewer, slot)")
        print(f"  Goal        : All (candidate, round) pairs assigned, no conflicts")
        print(f"  Cost        : Minimize backtracks; maximize preference alignment")

        total_vars = sum(len(c.required_rounds) for c in self.candidates)
        print(f"\n  CSP Variables (total assignments needed): {total_vars}")

        for c in self.candidates:
            print(f"    {c.name}: needs rounds {c.required_rounds}, prefers {c.preferred_slots}")

        self.trace.append(f"FORMULATE: {total_vars} assignments to schedule as CSP.")
