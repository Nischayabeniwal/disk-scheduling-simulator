# Disk Scheduling Simulator
```text
An interactive disk scheduling simulator that demonstrates and compares classic disk scheduling algorithms such as **FCFS, SSTF, SCAN, and C-SCAN**.
The project visualizes disk head movement and computes performance metrics like **total seek time**, **average seek time**, and **system throughput**.
This simulator is designed for **Operating Systems coursework**, **learning**, and **performance analysis**.
```
---
## 📌 Features
- Implements major disk scheduling algorithms:
  - First Come First Served (FCFS)
  - Shortest Seek Time First (SSTF)
  - SCAN (Elevator Algorithm)
  - C-SCAN (Circular SCAN)
- Accepts **custom disk request sequences**
- Configurable:
  - Disk size
  - Initial head position
  - Head movement direction (for SCAN variants)
- Calculates performance metrics:
  - Total seek distance
  - Average seek distance
  - Step-by-step head movement
  - (Optional) Throughput estimation
- Command-line interface (CLI)
- Modular design (easy to extend with GUI or visualization)
---
## 🧠 Project Structure
```text
disk-scheduling-simulator/
├── simulator/
│ ├── __init__.py
│ ├── disk.py # Disk and result data models
│ └── algorithms.py # Disk scheduling algorithms
├── run_sim.py # CLI entry point
├── tests/ # Unit tests (to be added)
├── requirements.txt # Python dependencies
└── README.md
```
---
## 🚀 Getting Started
### 1️ Clone the Repository
```bash
git clone https://github.com/Nischayabeniwal/disk-scheduling-simulator.git
```
```bash
cd disk-scheduling-simulator
```
### 2️ Install Dependencies
```bash
pip install -r requirements.txt
```
## ▶️ Usage
- Run the simulator using the command line:
```bash
python run_sim.py --algorithm fcfs --disk-size 200 --head 50 --requests 82,170,43,140,24,16,190
```
---

### Arguments
| Argument | Description |
|-----------------|-------------------------------------------------------|
| `--algorithm` | Scheduling algorithm (`fcfs`, `sstf`, `scan`, `cscan`) |
| `--disk-size` | Total number of disk tracks |
| `--head` | Initial head position |
| `--requests` | Comma-separated list of disk requests |
## Example (SSTF)
```bash
python run_sim.py -a sstf -d 200 -H 50 -r 82,170,43,140,24,16,190
```
---

## 📊 Sample Output
- Head movement sequence
- Seek distance per step
- Total seek distance
- Average seek distance
- Step-by-step movement table
### Example:
```bash
Algorithm: SSTF
Positions visited: [50, 43, 24, 16, 82, 140, 170, 190]
Total seek: 208
Average seek: 29.71
```
---

## 📈 Performance Metrics
  - Seek Distance
    |current_track − next_track|
  - Total Seek Time
    Sum of all seek distances
  - Average Seek Time
    Total seek / Number of requests
  - Throughput (optional)
    Requests serviced per unit seek time
🛠️ Technologies Used
  - Language: Python 3
  - Libraries:
      - tabulate (CLI tables)
  - Tools:
      - Git & GitHub
      - Kali Linux
---
## 📚 Educational Relevance
This project helps understand:
  - Disk I/O scheduling in Operating Systems
  - Trade-offs between fairness and performance
  - Seek time optimization
  - Algorithm comparison using real metrics
---
## 🔮 Future Enhancements
  - GUI / Web-based visualization (Streamlit or React)
  - Animated disk head movement
  - Support for arrival times of requests
  - Batch simulations and algorithm comparison graphs
  - Export results as CSV/JSON

---
## 📄 License
This project is open-source and available under the Apache-2.0 License.
