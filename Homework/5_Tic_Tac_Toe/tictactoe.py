import math
from itertools import product
from typing import Generator
import time
import os

N = 3

sym_to_player = {
    "O": 1,
    "X": -1,
    "_": 0
}

player_sym = {
    1: "O",
    -1: "X",
    0: "_"
}

def get_moves(table: list[list[int]]) -> Generator[tuple[int, int]]:
    return ((x, y) for x, y in product(range(N), range(N)) if table[x][y] == 0)

def winner(table: list[list[int]]) -> int | None:
    is_full = True

    for i in range(N):
        if table[i][0] != 0 and table[i] == [table[i][0]] * N:
            return table[i][0]

        if table[0][i] != 0 and [table[j][i] for j in range(N)] == [table[0][i]] * N:
            return table[0][i]

        if any(table[i][j] == 0 for j in range(N)):
            is_full = False

    if table[0][0] != 0 and [table[i][i] for i in range(N)] == [table[0][0]] * N:
        return table[0][0]
    
    if table[0][N-1] != 0 and [table[i][N-1-i] for i in range(N)] == [table[0][N-1]] * N:
        return table[0][N-1]

    if is_full:
        return 0

    return None

def negamax(table: list[list[int]], player: int, alpha: float, beta: float, depth: int) -> float:
    win = winner(table)

    if win == player:
        return (N * N + 1) - depth
    if win == -player:
        return depth - (N * N + 1)
    if win == 0:
        return 0

    score = -math.inf

    for x, y in get_moves(table):
        table[x][y] = player
        score = max(score, -negamax(table, -player, -beta, -alpha, depth + 1))
        table[x][y] = 0

        if score >= beta:
            return score

        alpha = max(alpha, score)

    return score

def next_move(table: list[list[int]], player: int) -> tuple[int, int]:
    if winner(table):
        return (-1, -1)
    
    val: float = -math.inf
    best_move = (-1, -1)

    for x, y in get_moves(table):
        table[x][y] = player
        score = -negamax(table, -player, -math.inf, -val, 1)
        table[x][y] = 0

        if score > val:
            val = score
            best_move = x, y

    return best_move

def table_input() -> list[list[int]]:
    table: list[list[int]] = [[0] * N for _ in range(N)]
    input()
    
    for y in range(N):
        row = [sym_to_player[c] for cell in input().split("|") if (c := cell.strip()) in sym_to_player]

        for x in range(N):
            table[x][y] = row[x]

        input()

    return table

def print_table(table: list[list[int]]):
    print("+---+---+---+")

    for y in range(N):
        print(f"| {" | ".join([player_sym[table[x][y]] for x in range(N)])} |")
        print("+---+---+---+")

def main():
    mode = input()
    turn = input().split()[1]

    player: int = sym_to_player[turn]

    if mode.lower() == "judge":
        table: list[list[int]] = table_input()
        start: float = time.perf_counter()

        x, y = next_move(table, player)
        length: float = (time.perf_counter() - start) * 1000
        print(f"# TIMES_MS: alg={length}")

        time_only = os.getenv("FMI_TIME_ONLY")
        if not time_only or time_only != "1":
            print("-1" if x == -1 else f"{y + 1} {x + 1}")
    elif mode.lower() == "game":
        human = input().split()[1]
        human_turn = player == sym_to_player[human]
        table: list[list[int]] = table_input()

        while True:
            win = winner(table)

            if win is not None:
                print("DRAW" if win == 0 else f"WINNER: {player_sym[win]}")
                break

            if human_turn:
                row, col = input().split()
                x = int(col) - 1
                y = int(row) - 1

                while table[x][y] != 0:
                    print("Invalid input, try again: ", end="")
                    row, col = input().split()
                    x = int(col) - 1
                    y = int(row) - 1
            else:
                x, y = next_move(table, player)

            table[x][y] = player
            player = -player
            human_turn = not human_turn
            print_table(table)


if __name__ == "__main__":
    main()