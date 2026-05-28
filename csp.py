"""
csp.py — CSP Scheduler with Backtracking (CO3)
Variables   : (candidate, round_type) pairs
Domains     : valid (interviewer, slot) combinations
Constraints :
  - Interviewer must match round type
  - Slot must be in interviewer's availability
  - No interviewer double-booked at same slot
  - Slot must be in candidate's preferred slots (soft)
Heuristics  : MRV (minimum remaining values) for variable ordering
"""

from models import Candidate, Interviewer, InterviewRound
from typing import List, Optional, Dict, Tuple


class CSPScheduler:
    def __init__(
        self,
        interviewers: List[Interviewer],
        candidates: List[Candidate],
        rounds: List[InterviewRound]
    ):
        self.interviewers = interviewers
        self.candidates = candidates
        self.rounds = rounds
        self.backtracks = 0
        self.trace_log = []

        # assignment: (candidate_id, round_type) -> (interviewer_id, slot)
        self.assignment: Dict[Tuple[str, str], Tuple[str, str]] = {}

        # Build variables: all (candidate, round) pairs
        self.variables = []
        for c in candidates:
            for r in c.required_rounds:
                self.variables.append((c.candidate_id, r))

    # ── CONSTRAINT CHECK ────────────────────────────────────────────
    def is_consistent(self, cand_id: str, round_type: str, iv_id: str, slot: str) -> bool:
        """Check all hard constraints for a proposed assignment."""

        iv = next((x for x in self.interviewers if x.interviewer_id == iv_id), None)
        if not iv:
            return False

        # C1: interviewer expertise must match round
        if iv.expertise != round_type:
            return False

        # C2: slot must be in interviewer's availability
        if slot not in iv.available_slots:
            return False

        # C3: no two assignments share same interviewer + slot
        for (c2, r2), (iv2, s2) in self.assignment.items():
            if iv2 == iv_id and s2 == slot:
                return False

        # C4: no candidate assigned same slot twice (different rounds)
        for (c2, r2), (iv2, s2) in self.assignment.items():
            if c2 == cand_id and s2 == slot:
                return False

        return True

    # ── DOMAIN for a variable ───────────────────────────────────────
    def get_domain(self, cand_id: str, round_type: str) -> List[Tuple[str, str]]:
        """Return all valid (interviewer, slot) pairs for this variable."""
        cand = next((c for c in self.candidates if c.candidate_id == cand_id), None)
        domain = []
        for iv in self.interviewers:
            if iv.expertise != round_type:
                continue
            for slot in iv.available_slots:
                # Soft: prefer candidate's preferred slots first
                domain.append((iv.interviewer_id, slot))

        # Sort: preferred slots first (MRV-like ordering)
        preferred = cand.preferred_slots if cand else []
        domain.sort(key=lambda x: (0 if x[1] in preferred else 1))
        return domain

    # ── MRV: pick variable with smallest domain ─────────────────────
    def select_unassigned_variable(self) -> Optional[Tuple[str, str]]:
        unassigned = [v for v in self.variables if v not in self.assignment]
        if not unassigned:
            return None
        # MRV heuristic
        return min(unassigned, key=lambda v: len(self.get_domain(v[0], v[1])))

    # ── BACKTRACKING SEARCH ─────────────────────────────────────────
    def backtrack(self) -> bool:
        var = self.select_unassigned_variable()
        if var is None:
            return True   # all variables assigned → solution found

        cand_id, round_type = var
        domain = self.get_domain(cand_id, round_type)

        self.trace_log.append(
            f"  Try ({cand_id}, {round_type}) — domain size: {len(domain)}"
        )

        for (iv_id, slot) in domain:
            if self.is_consistent(cand_id, round_type, iv_id, slot):
                self.assignment[var] = (iv_id, slot)
                self.trace_log.append(
                    f"    ✓ Assigned ({cand_id}, {round_type}) → ({iv_id}, {slot})"
                )

                if self.backtrack():
                    return True

                # backtrack
                del self.assignment[var]
                self.backtracks += 1
                self.trace_log.append(
                    f"    ✗ Backtrack from ({cand_id}, {round_type}) ← ({iv_id}, {slot})"
                )

        return False

    # ── SOLVE ───────────────────────────────────────────────────────
    def solve(self) -> Optional[List[dict]]:
        print("\n[CSP] Starting backtracking search...")
        success = self.backtrack()

        if not success:
            return None

        # Build result list
        results = []
        for (cand_id, round_type), (iv_id, slot) in self.assignment.items():
            cand = next(c for c in self.candidates if c.candidate_id == cand_id)
            iv   = next(i for i in self.interviewers if i.interviewer_id == iv_id)
            results.append({
                "candidate":   cand.name,
                "candidate_id": cand_id,
                "round":       round_type,
                "interviewer": iv.name,
                "interviewer_id": iv_id,
                "slot":        slot,
                "preferred":   slot in cand.preferred_slots,
                "score":       0   # filled by utility scorer
            })

        return results

    # ── TRACE PRINT ─────────────────────────────────────────────────
    def print_trace(self):
        for line in self.trace_log:
            print(line)
