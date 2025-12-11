import argparse
from tabulate import tabulate

from simulator.disk import Disk
#from simulator.algorithms import simulate_fcfs, simulate_sstf
from simulator.algorithms import (
    simulate_fcfs,
    simulate_sstf,
    simulate_scan,
    simulate_cscan,
)


def parse_requests(s):
    """
    Parse a comma-separated list of integers, e.g., "82,170,43"
    """
    if not s:
        return []
    return [int(x.strip()) for x in s.split(",") if x.strip()]


def main():
    parser = argparse.ArgumentParser(
        description="Disk Scheduling Simulator"
    )
    parser.add_argument(
        "--algorithm",
        "-a",
        choices=["fcfs", "sstf","scan","cscan"],
        default="fcfs",
        help="Scheduling algorithm to use",
    )
    parser.add_argument(
        "--disk-size", "-d", type=int, default=200,
        help="Number of tracks on disk (0..size-1)",
    )
    parser.add_argument(
        "--head", "-H", type=int, default=50,
        help="Starting head position",
    )
    parser.add_argument(
        "--requests", "-r", type=str, required=True,
        help='Comma-separated list of track requests, e.g. "82,170,43,140,24,16,190"',
    )

    args = parser.parse_args()

    requests = parse_requests(args.requests)
    disk = Disk(size=args.disk_size, head=args.head)

    # Basic validation
    for req in requests:
        if req < 0 or req >= disk.size:
            raise ValueError(f"Request {req} out of disk range 0..{disk.size-1}")

    if args.head < 0 or args.head >= disk.size:
        raise ValueError(f"Head position {args.head} out of disk range 0..{disk.size-1}")

    # Choose algorithm
    if args.algorithm == "fcfs":
        result = simulate_fcfs(requests, disk)
    elif args.algorithm == "sstf":
        result = simulate_sstf(requests, disk)
    elif args.algorithm == "scan":
        result = simulate_scan(requests, disk)
    elif args.algorithm == "cscan":
        result = simulate_cscan(requests, disk)
    else:
        raise ValueError("Unsupported algorithm")


    # Print results
    print(f"\nAlgorithm: {result.algorithm_name}")
    print(f"Requests: {requests}")
    print(f"Head start: {disk.head}")
    print(f"Positions visited: {result.positions}")
    print(f"Seek distances: {result.seek_distances}")
    print(f"Total seek: {result.total_seek}")
    print(f"Average seek: {result.average_seek:.2f}")

    # Simple table of steps
    rows = []
    for i in range(1, len(result.positions)):
        rows.append([
            i,
            result.positions[i - 1],
            result.positions[i],
            abs(result.positions[i] - result.positions[i - 1])
        ])

    print("\nStep-by-step movement:")
    print(tabulate(rows, headers=["Step", "From", "To", "Seek"], tablefmt="github"))


if __name__ == "__main__":
    main()
