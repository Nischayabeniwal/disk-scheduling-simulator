# Algorithm Comparisons

This document compares the four implemented algorithms on the basis of:
efficiency, fairness, and real-world usage.

---

## 1. Total Seek Time (Efficiency)

| Algorithm | Efficiency | Notes |
|----------|------------|-------|
| FCFS     | Low        | No optimization of head movement |
| SSTF     | High       | Always picks nearest request |
| SCAN     | Medium-High| Balanced movement pattern |
| CSCAN    | Medium-High| Very predictable performance |

---

## 2. Fairness

| Algorithm | Fairness | Notes |
|----------|----------|-------|
| FCFS     | High     | Serves all requests in order |
| SSTF     | Low      | Far requests may starve |
| SCAN     | High     | Elevator-like fairness |
| CSCAN    | Very High| Eliminates direction bias |

---

## 3. Real-World Use Cases

### FCFS
Used in simple systems where fairness matters more than speed.

### SSTF
Used in older hard disks where performance was critical.

### SCAN
Inspired many modern disk scheduling policies.

### CSCAN
Used in real-time and time-critical storage environments.

---

## 4. Summary Table

| Algorithm | Good For | Bad For |
|----------|----------|---------|
| FCFS | Simplicity, fairness | Efficiency |
| SSTF | Fast access, low seek time | Starvation, fairness |
| SCAN | Balanced performance | Edge delays |
| CSCAN | Predictable timing | Jump from end to start |
