# Project Architecture

This project simulates four disk scheduling algorithms used in Operating Systems:
FCFS, SSTF, SCAN and CSCAN.

The goal was to understand how the disk head moves and how different algorithms
affect the total seek time.

---

## 1. Folder Structure
```text
disk-scheduling-simulator/
├── simulator/
│ ├── __init__.py
│ ├── disk.py # Disk and result data models
│ └── algorithms.py # Disk scheduling algorithms
├── run_sim.py # CLI entry point
├── docs/                            
├── requirements.txt # Python dependencies
└── README.md
```
---

---

## 2. How the Program Works

### Step 1: Input
The program takes:
- Initial head position  
- List of disk requests  
- Selected scheduling algorithm  

These inputs can be passed through the command line.

### Step 2: Processing  
The scheduler computes the order in which the disk head will move based on the
chosen algorithm.

### Step 3: Output  
The program outputs:
- The sequence of head movements  
- Total seek time  
- (Optional) Plot of head movement  

---

## 3. Python Modules Used

- **argparse** — for command-line arguments  
- **matplotlib** (optional) — for visualization  
- **pytest** — for testing  

---

## 4. Why This Architecture?

The project is divided into small modules so each algorithm is easy to understand,
test, and maintain.  
This structure also mimics real-world software engineering practices.
