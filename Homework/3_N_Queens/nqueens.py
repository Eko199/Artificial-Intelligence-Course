import argparse
import os
import random
import time

def knight_init_board(n: int) -> list[int]:
    return list(range(1, n, 2)) + list(range(0, n, 2))

def knight_init_board2(n: int) -> list[int]:
    base = n
    while base % 6 in (2, 3):
        base -= 1
    return list(range(1, base, 2)) + list(range(0, base, 2)) + list(range(base, n))

def print_board(queens_rows, n):
    for row in queens_rows:
        print(" ".join(["_" if i != row else "*" for i in range(n)]))

def main():
    n = int(input())
    start: float = time.perf_counter()
    random.seed(time.time_ns())

    if n == 2 or n == 3:
        length: float = (time.perf_counter() - start) * 1000
        print(f"# TIMES_MS: alg={length}")
        print(-1)
        return

    queens_rows: list[int] = knight_init_board2(n)
    queens_per_col = [1] * n
    queens_per_d1 = [0] * (2 * n - 1)
    queens_per_d2 = [0] * (2 * n - 1)

    for row, col in enumerate(queens_rows):
        queens_per_d1[row - col + n - 1] += 1
        queens_per_d2[row + col] += 1

    while True:
        i = 0
        while i < max(10000, n):
            max_conflicts = 0
            conflicting_queens = []

            for row, col in enumerate(queens_rows):
                conflicts = queens_per_col[col] - 1 + queens_per_d1[row - col + n - 1] - 1 + queens_per_d2[row + col] - 1

                if conflicts >= max_conflicts:
                    if conflicts > max_conflicts:
                        conflicting_queens = []
                        max_conflicts = conflicts

                    conflicting_queens.append(row)

            if max_conflicts == 0:
                break

            conflicting_queen = conflicting_queens[int(random.random() * len(conflicting_queens))]
            curr_col = queens_rows[conflicting_queen]

            min_conflicts = n
            best_cols = []

            for new_col in range(n):
                if new_col == curr_col:
                    continue

                conflicts = queens_per_col[new_col] + queens_per_d1[conflicting_queen - new_col + n - 1] + queens_per_d2[conflicting_queen + new_col]

                if conflicts <= min_conflicts:
                    if conflicts < min_conflicts:
                        best_cols = []
                        min_conflicts = conflicts

                    best_cols.append(new_col)

            best_col = best_cols[int(random.random() * len(best_cols))]

            queens_rows[conflicting_queen] = best_col
            queens_per_col[curr_col] -= 1
            queens_per_col[best_col] += 1
            queens_per_d1[conflicting_queen - curr_col + n - 1] -= 1
            queens_per_d1[conflicting_queen - best_col + n - 1] += 1
            queens_per_d2[conflicting_queen + curr_col] -= 1
            queens_per_d2[conflicting_queen + best_col] += 1
            i += 1

        if i < max(10000, n):
            break

        queens_rows = knight_init_board(n)
        queens_per_col = [1] * n
        queens_per_d1 = [0] * (2 * n - 1)
        queens_per_d2 = [0] * (2 * n - 1)
    
        for row, col in enumerate(queens_rows):
            queens_per_d1[row - col + n - 1] += 1
            queens_per_d2[row + col] += 1

    length: float = (time.perf_counter() - start) * 1000
    print(f"# TIMES_MS: alg={length}")

    time_only = os.getenv("FMI_TIME_ONLY")
    if not time_only or time_only != "1":
        queens_cols = [row for row, _ in sorted(enumerate(queens_rows), key=lambda rowcol: rowcol[1])]
        print(queens_cols)

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action='store_true')
    args = parser.parse_args()

    if args.p:
        print_board(queens_rows, n)

if __name__ == "__main__":
    main()