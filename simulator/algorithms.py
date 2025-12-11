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


def simulate_scan(requests, disk):
    """
    SCAN (Elevator) algorithm.
    We assume the head initially moves towards higher track numbers.

    Approach:
    - Split requests into:
        left  = requests < head
        right = requests >= head
    - Serve 'right' in ascending order (moving up),
      then 'left' in descending order (moving down).
    """
    current = disk.head
    positions = [current]

    left = sorted([r for r in requests if r < current])
    right = sorted([r for r in requests if r >= current])

    # Move up (increasing tracks)
    for r in right:
        positions.append(r)
        current = r

    # Then move down (decreasing tracks)
    for r in reversed(left):
        positions.append(r)
        current = r

    return SimulationResult("SCAN", positions, requests)


def simulate_cscan(requests, disk):
    """
    C-SCAN (Circular SCAN) algorithm.
    We assume the head moves in one direction (upwards), then jumps
    back to the lowest request and continues upwards again.

    Approach:
    - Split into left (requests < head) and right (requests >= head)
    - Serve 'right' in ascending order,
      then 'left' in ascending order (after a logical jump).
    """
    current = disk.head
    positions = [current]

    left = sorted([r for r in requests if r < current])
    right = sorted([r for r in requests if r >= current])

    # Move up and serve right side
    for r in right:
        positions.append(r)
        current = r

    # Logical jump to the lowest request (we don't add the jump itself
    # as intermediate positions; only serviced requests are recorded)
    for r in left:
        positions.append(r)
        current = r

    return SimulationResult("C-SCAN", positions, requests)
