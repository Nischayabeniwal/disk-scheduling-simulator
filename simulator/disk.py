class Disk:
    def __init__(self, size, head=0, direction=1):
        """
        size: total number of tracks (0 to size-1)
        head: starting head position
        direction: 1 for increasing, -1 for decreasing (for SCAN/C-SCAN)
        """
        self.size = size
        self.head = head
        self.direction = direction


class SimulationResult:
    def __init__(self, algorithm_name, positions, requests):
        """
        algorithm_name: str, e.g., 'FCFS'
        positions: list of head positions visited, including starting head
        requests: original request list (for reference)
        """
        self.algorithm_name = algorithm_name
        self.positions = positions
        self.requests = requests
        self.seek_distances = self._compute_seek_distances()
        self.total_seek = sum(self.seek_distances)
        self.average_seek = (
            self.total_seek / len(requests) if requests else 0
        )

    def _compute_seek_distances(self):
        if len(self.positions) < 2:
            return []
        return [abs(self.positions[i] - self.positions[i - 1])
                for i in range(1, len(self.positions))]
