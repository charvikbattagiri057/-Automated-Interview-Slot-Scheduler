"""
models.py — Core data structures for AISS
CO1: State representation using Python dataclasses
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TimeSlot:
    slot_id: str          # e.g. "Mon-9AM"
    day: str
    time: str

    def __repr__(self):
        return f"{self.day}-{self.time}"

    def __hash__(self):
        return hash(self.slot_id)

    def __eq__(self, other):
        return self.slot_id == other.slot_id


@dataclass
class Interviewer:
    interviewer_id: str
    name: str
    expertise: str                    # "HR" / "Technical" / "Managerial"
    available_slots: List[str]        # list of slot strings e.g. ["Mon-9AM"]
    assigned_slots: List[str] = field(default_factory=list)

    def is_available(self, slot: str) -> bool:
        return slot in self.available_slots and slot not in self.assigned_slots

    def assign(self, slot: str):
        self.assigned_slots.append(slot)

    def unassign(self, slot: str):
        if slot in self.assigned_slots:
            self.assigned_slots.remove(slot)

    def __repr__(self):
        return f"Interviewer({self.name}, {self.expertise})"


@dataclass
class Candidate:
    candidate_id: str
    name: str
    required_rounds: List[str]        # e.g. ["HR", "Technical"]
    preferred_slots: List[str]        # preferred slot strings
    scheduled: dict = field(default_factory=dict)  # round -> slot

    def needs_round(self, round_type: str) -> bool:
        return round_type in self.required_rounds

    def __repr__(self):
        return f"Candidate({self.name})"


@dataclass
class InterviewRound:
    round_id: str
    round_type: str     # "HR", "Technical", "Managerial"
    duration_min: int   # duration in minutes

    def __repr__(self):
        return f"Round({self.round_type}, {self.duration_min}min)"


@dataclass
class Assignment:
    candidate: Candidate
    interviewer: Interviewer
    round_type: str
    slot: str
    utility_score: float = 0.0

    def to_dict(self):
        return {
            "candidate": self.candidate.name,
            "interviewer": self.interviewer.name,
            "round": self.round_type,
            "slot": self.slot,
            "score": self.utility_score
        }
