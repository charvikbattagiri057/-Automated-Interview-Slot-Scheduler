"""
search.py — BFS Slot Finder (CO2)
Uses BFS to explore the state space of possible interviewer-slot combinations.
Counts node expansions and measures reachability before CSP assignment.
"""

from collections import deque
from models import Interviewer, Candidate
from typing import List, Dict, Set


class BFSSlotFinder:
    def __init__(self, interviewers: List[Interviewer], candidates: List[Candidate]):
        self.interviewers = interviewers
        self.candidates = candidates
        self.nodes_explored = 0
        self.reachable = {}   # round_type -> set of (interviewer_id, slot) pairs

    def find_all_reachable_slots(self) -> Dict[str, Set]:
        """
        BFS: For each round type, explore which (interviewer, slot) pairs
        are reachable from the initial state (no assignments made).
        """
        print("\n[BFS] Exploring reachable (interviewer, slot) pairs per round...")

        round_types = set()
        for c in self.candidates:
            round_types.update(c.required_rounds)

        for rtype in sorted(round_types):
            visited = set()
            queue = deque()

            # Initial frontier: all interviewers matching this round type
            eligible = [iv for iv in self.interviewers if iv.expertise == rtype]

            for iv in eligible:
                for slot in iv.available_slots:
                    start_node = (iv.interviewer_id, slot)
                    if start_node not in visited:
                        queue.append(start_node)
                        visited.add(start_node)

            # BFS expansion (simulates exploring neighboring time slots)
            while queue:
                node = queue.popleft()
                self.nodes_explored += 1
                iv_id, slot = node

                # Neighbors: same interviewer, adjacent slots (simple model)
                iv = next((x for x in self.interviewers if x.interviewer_id == iv_id), None)
                if iv:
                    for neighbor_slot in iv.available_slots:
                        neighbor = (iv_id, neighbor_slot)
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)

            self.reachable[rtype] = visited
            print(f"  [{rtype}] reachable pairs: {len(visited)} | nodes explored: {self.nodes_explored}")

        return self.reachable
