import os
import time

def solve(frogs: str, goal: str, idx: int) -> list[str] | None:
    if frogs == goal:
        return [frogs]

    res: list[str] | None = None

    if idx - 1 >= 0 and frogs[idx-1] == ">":
        new_frogs = frogs[:idx-1] + "_>" + frogs[idx+1:]
        res = solve(new_frogs, goal, idx - 1)

    if not res and idx - 2 >= 0 and frogs[idx-2] == ">":
        new_frogs = frogs[:idx-2] + "_" + frogs[idx-1] + ">" + frogs[idx+1:]
        res = solve(new_frogs, goal, idx - 2)

    if not res and idx + 1 < len(frogs) and frogs[idx+1] == "<":
        new_frogs = frogs[:idx] + "<_" + frogs[idx+2:]
        res = solve(new_frogs, goal, idx + 1)

    if not res and idx + 2 < len(frogs) and frogs[idx+2] == "<":
        new_frogs = frogs[:idx] + "<" + frogs[idx+1] + "_" + frogs[idx+3:]
        res = solve(new_frogs, goal, idx + 2)

    if res:
        res.append(frogs)
        return res

def solve_linear(frogs: str, show: bool = True):
    if show:
        print(frogs)

    i: int = len(frogs) // 2
    right = True
    jumps = 0

    while i > 0 and i < len(frogs) - 1:
        if right:
            frogs = frogs[:i-1] + "_>" + frogs[i+1:]
            i -= 1
        else:
            frogs = frogs[:i] + "<_" + frogs[i+2:]
            i += 1

        if show:
            print(frogs)

        jumps += 1
        right = not right

        for _ in range(jumps):
            if right:
                frogs = frogs[:i-2] + "_" + frogs[i-1] + ">" + frogs[i+1:]
                i -= 2
            else:
                frogs = frogs[:i] + "<" + frogs[i+1] + "_" + frogs[i+3:]
                i += 2

            if show:
                print(frogs)

    while jumps > 0:
        right = not right
        jumps -= 1

        if right:
            frogs = frogs[:i-1] + "_>" + frogs[i+1:]
            i -= 1
        else:
            frogs = frogs[:i] + "<_" + frogs[i+2:]
            i += 1

        if show:
            print(frogs)

        for _ in range(jumps):
            if right:
                frogs = frogs[:i-2] + "_" + frogs[i-1] + ">" + frogs[i+1:]
                i -= 2
            else:
                frogs = frogs[:i] + "<" + frogs[i+1] + "_" + frogs[i+3:]
                i += 2

            if show:
                print(frogs)

def main():
    n: int = int(input())
    frogs: str = ">" * n + "_" + "<" * n
    goal: str = "<" * n + "_" + ">" * n

    time_only = os.getenv("FMI_TIME_ONLY")
    start: float = time.perf_counter()
    result: list[str] | None = solve(frogs, goal, n)
    #solve_linear(frogs, not time_only or time_only != "1")
    length: float = (time.perf_counter() - start) * 1000
    print(f"# TIMES_MS: alg={length}")


    if result and (not time_only or time_only != "1"):
        result.reverse()
        print("\n".join(result))

if __name__ == "__main__":
    main()