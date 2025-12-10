from .disk import SimulationResult


def simulate_fcfs(requests, disk):
    """
    First-Come, First-Served disk scheduling.
    requests: list of track numbers
    disk: Disk object
    """
    positions = [disk.head]
    for r in requests:
        positions.append(r)
    return SimulationResult("FCFS", positions, requests)


def simulate_sstf(requests, disk):
    """
    Shortest Seek Time First.
    Always serve the closest pending request to the current head position.
    """
    pending = requests.copy()
    current = disk.head
    positions = [current]

    while pending:
        # Find request with minimum distance from current
        closest = min(pending, key=lambda r: abs(r - current))
        positions.append(closest)
        current = closest
        pending.remove(closest)

    return SimulationResult("SSTF", positions, requests)
