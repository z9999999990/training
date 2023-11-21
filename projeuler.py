#!/usr/bin/env python3
# coding: utf-8


"""
Main entry, runner of all problem solutions.
"""


import os
import sys
import inspect
import importlib
import argparse
import math
from typing import (
    Callable,
    Generator,
    List,
    Mapping,
)
from datetime import datetime
from threading import Thread


PROBLEM_DIR = "problems"


def _get_parser():
    parser = argparse.ArgumentParser(description="Project Euler problem runner")

    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    cmd_list = subparsers.add_parser("list", help="list all problems")
    cmd_list.add_argument(
        "-f", "--full", action="store_true", help="show full information"
    )
    cmd_list.add_argument(
        "id", nargs="*", type=int, help="show specific problem information"
    )

    cmd_run = subparsers.add_parser("run", help="run problems")
    cmd_run.add_argument(
        "-c", "--check", action="store_true", help="check the solution answer"
    )
    cmd_run.add_argument(
        "-t", "--timeout", type=float, default=1000.0, help="timeout in milliseconds"
    )
    cmd_run.add_argument("id", nargs="*", type=int, help="run specific problems")

    return parser


def _add_indent(s: str, indent: str) -> str:
    lines = s.split("\n")
    result = [indent + line for line in lines]
    return "\n".join(result)


class _TimeOutResult:
    pass


class Result:
    """
    Result of a problem solution.
    """

    def __init__(self, result: int, time: float):
        self.result = result
        self.time = time

    def __repr__(self) -> str:
        return f"<{self.result}, {self.time}>"

    def is_timeout(self) -> bool:
        """
        Check if this result is a timeout.
        """
        return self.time < 0.0


def find_best_result(
    default_result: Result, result_map: Mapping[str, Result]
) -> tuple([bool, str]):
    """
    Find best result.
    """
    best_key = ""
    best_result = -1.0

    if default_result is not None:
        if not default_result.is_timeout():
            best_result = default_result.time

    for key, result in result_map.items():
        if result.is_timeout():
            continue

        if best_result < 0 or result.time < best_result:
            best_key = key
            best_result = result.time

    if best_result < 0:
        return False, ""

    return True, best_key


def run_solver(solver: Callable[[], int], timeout: float = 1000.0) -> Result:
    """
    Run a solver function.
    """
    result = _TimeOutResult()

    def wrapper():
        nonlocal result
        result = solver()

    thread = Thread(target=wrapper)
    time_start = datetime.now()
    thread.start()
    thread.join(timeout=timeout / 1000)
    time_finish = datetime.now()
    if isinstance(result, _TimeOutResult):
        return None, -timeout

    dt = 1000.0 * (time_finish - time_start).total_seconds()
    return result, dt


class ProblemSolver:
    """
    Base class of problem solution.
    """

    solvers: Mapping[str, Callable[[], int]]
    __doc__ = ""

    def __init__(self, pid: int, answer: int):
        self.pid = pid
        self.answer = answer
        self.solvers = {}
        self.title = ""
        self.content = ""

    def set_document(self, doc: str):
        """
        Set document of this problem.
        """
        self.__doc__ = doc
        lines = doc.strip().split("\n")
        if len(lines) < 2:
            raise RuntimeError("Invalid document format")

        self.title = lines[0].strip()
        self.content = "\n".join(lines[1:]).strip()

    def add_solver(self, name: str, func: Callable[[], int]):
        """
        Add a solver function.
        """
        if name in self.solvers:
            raise RuntimeError(f"Solver {name} already exists")

        self.solvers[name] = func

    def print(self, key: str, result: Result, check: bool = False) -> str:
        """
        Print result of a solver.
        """
        pid = self.pid
        r = ""
        if result is not None:
            r = result.result
            if result.is_timeout():
                r = "timeout"
            elif result.result is None:
                r = "no answer returned"

        if key != "":
            line = [f"{'':<5} {key:<40} {r:<10}"]
        else:
            line = [f"{pid:<5} {self.title:.<40} {r:<10}"]

        if check:
            if self.answer is None:
                rc = "not set"

            elif result is None:
                rc = ""

            elif result.is_timeout():
                rc = "timeout"

            elif self.answer == result.result:
                rc = "correct"

            else:
                rc = "wrong"

            line.append(f" {rc:8}")

        if result is not None:
            line.append(f" {math.fabs(result.time):10.3f}ms")
        else:
            line.append("             ")

        return "".join(line)

    def solve(
        self, name: str = None, timeout: float = 1000.0
    ) -> tuple[Result, Mapping[str, Result]]:
        """
        Solve the problem.
        """
        default_result = None
        result_map = {}

        for key, solver in self.solvers.items():
            if name is not None and key != name:
                continue

            result, time_cost = run_solver(solver, timeout=timeout)
            item = Result(result, time_cost)
            if key == "":
                default_result = item
            else:
                result_map[key] = item

        return default_result, result_map


def find_problem_solvers(
    dirname: str, id_list: List[int] = None
) -> Generator[ProblemSolver, None, None]:
    """
    Find all problem solvers in given directory.
    """
    target_dir = f"{dirname}"

    id_set = set(id_list or [])
    file_list = os.listdir(target_dir)
    file_list.sort()
    for filename in file_list:
        if not filename.endswith(".py"):
            continue

        base_name = filename[0:-3]
        if base_name == "__init__":
            continue

        package_name = dirname.replace("/", ".")
        module_name = f"{package_name}.{base_name}"

        try:
            mod = importlib.import_module(f"{module_name}")
            attrs = ["PID", "ANSWER"]
            for attr in attrs:
                if not hasattr(mod, attr):
                    raise RuntimeError(f"Missing attribute {attr} in {module_name}")

            solver = ProblemSolver(mod.PID, mod.ANSWER)
            solver.set_document(mod.__doc__)
            for name, func in inspect.getmembers(mod, inspect.isfunction):
                if name == "solve":
                    solver.add_solver("", func)

                elif len(name) > 6 and name.startswith("solve_"):
                    solver.add_solver(name[6:], func)

                else:
                    continue

            if len(id_set) > 0 and solver.pid not in id_set:
                continue

            yield solver

        except ImportError as ex:
            print(f"Failed to import {module_name}: {ex}")

        except SyntaxError as ex:
            print(f"Syntax error in {module_name}/{filename}: {ex}")


def do_list(id_list: List[int], full: bool):
    """
    List problems.
    """
    for problem in find_problem_solvers(PROBLEM_DIR, id_list=id_list):
        print(f"{problem.pid:<5d} {problem.title}")
        if full:
            print(_add_indent(problem.content, "      "))
            print()


def do_run(id_list: List[int], timeout: float, check: bool):
    """
    Run problems.
    """
    retcode = 0
    for problem in find_problem_solvers(PROBLEM_DIR, id_list=id_list):
        default_solver, other_solvers = problem.solve(timeout=timeout)
        if default_solver is None and len(other_solvers) <= 0:
            print(f"{problem.pid:<5d} {problem.title:.<30} no answer returned")
            return

        has_best, best_result = find_best_result(default_solver, other_solvers)
        total_time = 0.0
        header_line = ""
        lines = []

        header_line = problem.print("", default_solver, check=check)
        if default_solver is not None:
            total_time += math.fabs(default_solver.time)

        for key, solver in other_solvers.items():
            line = problem.print(key, solver, check=check)
            if has_best and key == best_result:
                line = line + " *[BEST]"
            lines.append(line)
            total_time += math.fabs(solver.time)

        header_line += f" total={total_time:.3f}ms"
        print(header_line)
        for line in lines:
            print(line)

    sys.exit(retcode)


def main():
    """
    Main entry.
    """
    parser = _get_parser()
    args = parser.parse_args()

    if args.command == "list":
        do_list(args.id, args.full)

    elif args.command == "run":
        do_run(args.id, args.timeout, args.check)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
