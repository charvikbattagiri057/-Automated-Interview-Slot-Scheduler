# AISS — Automated Interview Slot Scheduler
**Course:** Computational Foundations for AI (25SC1306E)  
**Institution:** KL University, Bachupally  
**Academic Year:** 2025–2026, Term 3

---

## 📌 Project Overview
AISS is a Python-based intelligent scheduling system that automatically assigns interview slots to candidates by matching their availability with interviewers across multiple round types (HR, Technical, Managerial). It combines four core CFAI concepts into a unified pipeline.

---

## 🧠 CFAI Concepts Demonstrated

| Module      | File           | CO  | Concept                              |
|-------------|----------------|-----|--------------------------------------|
| Agent Model | `agents.py`    | CO1 | PEAS framework, state formulation    |
| BFS Search  | `search.py`    | CO2 | Breadth-first slot reachability scan |
| CSP Solver  | `csp.py`       | CO3 | Backtracking + MRV heuristic         |
| Utility     | `utility.py`   | CO4 | Multi-criteria scoring function      |

---

## 📁 Project Structure
```
AISS/
├── index.html          ← Web UI (frontend showcase)
└── AISS/
    ├── main.py         ← Entry point
    ├── models.py       ← Data models (Candidate, Interviewer, etc.)
    ├── agents.py       ← CO1: SchedulerAgent (PEAS)
    ├── search.py       ← CO2: BFS slot finder
    ├── csp.py          ← CO3: CSP backtracking solver
    ├── utility.py      ← CO4: Utility scorer
    ├── requirements.txt
    └── outputs/
        ├── schedule.json
        └── schedule.csv
```

---

## ▶️ How to Run
```bash
cd AISS
python main.py
```
No external libraries required — pure Python 3.9+.

---

## ⚙️ System Design

### Problem Formulation (CO1)
- **State:** `(candidate, round_type) → (interviewer, slot)`
- **Actions:** Assign a valid (interviewer, slot) pair
- **Goal:** All required (candidate, round) pairs scheduled, no conflicts
- **Cost:** Minimize backtracks; maximize preference alignment

### Search (CO2)
BFS explores the space of (interviewer, slot) pairs per round type before the CSP runs, measuring reachability and counting node expansions.

### CSP (CO3)
- **Variables:** All `(candidate, round_type)` pairs
- **Domains:** Valid `(interviewer, slot)` combinations
- **Constraints:**
  1. Interviewer expertise must match round type
  2. Slot must be in interviewer's availability
  3. No interviewer double-booked at the same slot
  4. No candidate assigned two interviews at the same slot
- **Heuristic:** MRV (Minimum Remaining Values) for variable ordering

### Utility Scoring (CO4)
Each assignment is scored out of 10 based on:
- Preference alignment (+4)
- Expertise match (+3)
- Early slot bonus (+2)
- Interviewer load balance (+1)

---

## 📤 Outputs
- Terminal: formatted schedule + reasoning trace
- `outputs/schedule.json` — machine-readable schedule
- `outputs/schedule.csv` — spreadsheet-compatible
- `index.html` — visual dashboard
