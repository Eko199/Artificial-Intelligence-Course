import os
import time
from math import sqrt

def manhattan_dist(x: int, y: int, table: list[list[int]], solution: dict[int, tuple[int, int]]) -> int:
    x_solved, y_solved = solution[table[y][x]]
    return abs(x - x_solved) + abs(y - y_solved)

def table_str(table: list[list[int]]) -> str:
    return "".join([str(x) for x in sum(table, [])])

def solve(
    table: list[list[int]],
    solution: dict[int, tuple[int, int]],
    path: list[str],
    g: int,
    h: int,
    bound: float,
    blank_x: int,
    blank_y: int,
    visited: set[str]
) -> float:
    f = g + h

    if f > bound:
        return f

    if h == 0:
        # Solution found
        return -1

    min = float("inf")
    directions = [(-1, 0, "right"), (1, 0, "left"), (0, -1, "down"), (0, 1, "up")]
    visited.add(table_str(table))

    for dx, dy, dir in directions:
        new_blank_x, new_blank_y = blank_x + dx, blank_y + dy

        if new_blank_x < 0 or new_blank_x >= len(table) or new_blank_y < 0 or new_blank_y >= len(table):
            continue

        old_mh = manhattan_dist(new_blank_x, new_blank_y, table, solution)
        table[blank_y][blank_x], table[new_blank_y][new_blank_x] = table[new_blank_y][new_blank_x], table[blank_y][blank_x]

        if table_str(table) in visited:
            table[blank_y][blank_x], table[new_blank_y][new_blank_x] = table[new_blank_y][new_blank_x], table[blank_y][blank_x]
            continue

        new_h = h - old_mh + manhattan_dist(blank_x, blank_y, table, solution)

        path.append(dir)
        res = solve(table, solution, path, g + 1, new_h, bound, new_blank_x, new_blank_y, visited)

        if res == -1:
            return res

        path.pop()

        if res < min:
            min = res

        table[blank_y][blank_x], table[new_blank_y][new_blank_x] = table[new_blank_y][new_blank_x], table[blank_y][blank_x]

    return min


def main():
    n = int(input())
    pos_0 = int(input())

    if pos_0 == -1:
        pos_0 = n

    side = int(sqrt(n+1))
    table = []
    for _ in range(side):
        table.append([int(x) for x in input().split()])

    start: float = time.perf_counter()
    solution = {}

    for y in range(side):
        for x in range(side):
            i = x + y * side

            if i == pos_0:
                number = 0
            elif i < pos_0:
                number = i + 1
            else:
                number = i

            solution[number] = (x, y)

    #Detect unsolvable puzzle
    inversions = 0

    for i in range(n+1):
        x = i % side
        y = i // side

        if table[y][x] == 0:
            blank_y = y
            blank_x = x
            continue

        for j in range(i+1, n+1):
            x2 = j % side
            y2 = j // side

            if table[y2][x2] == 0:
                continue

            if table[y][x] > table[y2][x2]:
                inversions += 1

    if (side % 2 == 1 and inversions % 2 == 1) or (side % 2 == 0 and (inversions + blank_y) % 2 == 0):
        length: float = (time.perf_counter() - start) * 1000
        print(f"# TIMES_MS: alg={length}")
        print(-1)
        return

    # IDA*
    h = 0
    for y in range(side):
        for x in range(side):
            if table[y][x] != 0:
                h += manhattan_dist(x, y, table, solution)

    path = []
    bound = float(h)
    while True:
        bound = solve(table, solution, path, 0, h, bound, blank_x, blank_y, set())

        if bound == -1:
            break

        # Bound should not be infinity (unsolvable), I would raise an exception here, but won't bother
    
    length: float = (time.perf_counter() - start) * 1000
    print(f"# TIMES_MS: alg={length}")

    time_only = os.getenv("FMI_TIME_ONLY")
    if not time_only or time_only != "1":
        print(len(path))
        for move in path:
            print(move)
        

if __name__ == "__main__":
    main()
