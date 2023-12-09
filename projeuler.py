#!/usr/bin/env python3
# coding: utf-8


"""
Main entry, runner of all problem solutions.
"""


from __future__ import annotations

import os
import sys
import inspect
import importlib
import argparse
import time
import multiprocessing

from typing import (
    Callable,
    Generator,
    Iterable,
    Mapping,
)

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
        "-t", "--timeout", type=float, default=5000.0, help="timeout in milliseconds"
    )
    cmd_run.add_argument("id", nargs="*", type=int, help="run specific problems")

    return parser


def _add_indent(s: str, indent: str) -> str:
    lines = s.split("\n")
    result = [indent + line for line in lines]
    return "\n".join(result)


class _TimeoutResult:
    def __repr__(self) -> str:
        return "TIMEOUT"


class SolutionMethod:
    """
    Solution method
    """

    def __init__(self, func: Callable[[], int], name: str, note: str = ""):
        self.func = func
        self.name = name
        self.note = note or ""
        self.time_cost = 0.0
        self.result = _TimeoutResult()
        self.finished = False

    def _proc_main(self, queue: multiprocessing.Queue):
        result = _TimeoutResult()
        time_start = time.perf_counter()
        result = self.func()
        time_finish = time.perf_counter()
        dt = 1000.0 * (time_finish - time_start)

        queue.put((result, dt))

    def solve(self, runner: Runner, timeout: float = 1000.0) -> None:
        """
        Run the solution method.
        """
        result, timeout, cost = runner.run_func(self.func, timeout=timeout)
        self.finished = not timeout
        self.time_cost = cost
        if not timeout:
            self.result = result

        else:
            self.result = None

    @property
    def title(self) -> str:
        """
        Title of this method.
        """
        result = self.name
        if self.note != "":
            result = self.note.strip().split("\n")[0]

        return result

    def is_timeout(self) -> bool:
        """
        Is solution method timeout
        """
        return not self.finished

    def print(self, title: str, suffix: str | None, answer: int = None) -> str:
        """
        Print result of this method.
        """
        line = [f"{title}"]

        if self.result is None:
            r = "NO RESULT"
        else:
            r = f"{self.result}"

        line.append(f" {r:<15}")

        if answer is not None:
            if self.is_timeout():
                rc = "timeout"

            elif self.result is None:
                rc = "NO ANSWER"

            elif answer == self.result:
                rc = "correct"

            else:
                rc = "wrong"

            line.append(f" {rc:10}")

        line.append(f" {self.time_cost:10.3f}ms")
        if suffix is not None:
            line.append(f" {suffix}")

        return "".join(line)


class ProblemSolver:
    """
    Base class of problem solution.
    """

    methods: Mapping[str, SolutionMethod]
    pid: int
    answer: int | None = None
    timeout_ext: float = 0.0
    __doc__ = ""

    def __init__(self, pid: int):
        self.pid = pid
        self.answer = None
        self.methods = {}
        self.title = ""
        self.content = ""
        self.timeout_ext = 0.0

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

    def add_method(self, func: Callable[[], int], name: str, note: str = ""):
        """
        Add a solution method.
        """
        if name in self.methods:
            raise RuntimeError(f"Method {name} already exists")

        method = SolutionMethod(func, name, note)
        self.methods[name] = method

    def is_correct(self) -> bool:
        """
        Is the solution correct, should have at less one correct result.
        """
        result = False
        for method in self.methods.values():
            if method.is_timeout():
                continue

            if method.result is None:
                continue

            if self.answer is not None and method.result != self.answer:
                result = False
                continue

            result = True

        return result

    def find_best_solution(self) -> str:
        """
        Find the best solution.
        """
        cost = None
        best = None
        for name, method in self.methods.items():
            if method.is_timeout():
                continue

            if method.result is None:
                continue

            if cost is None or method.time_cost < cost:
                cost = method.time_cost
                best = name

        return best

    def print(self, check: bool = False) -> str:
        """
        Print result of a problem solver.
        """
        pid = self.pid
        lines = []

        answer = self.answer
        if not check:
            answer = None
        header = f"{pid:<5} {self.title:.<40}"
        if len(self.methods) > 1:
            best = self.find_best_solution()
            total_cost = 0.0
            for name, method in self.methods.items():
                suffix = "*BEST" if name == best else None
                title = f"      {method.title:.<40}"
                line = method.print(title, suffix, answer=answer)
                lines.append(line)
                total_cost += method.time_cost

            placeholder = ""
            note = ""
            if self.timeout_ext > 0.0:
                note = f"[+{self.timeout_ext:.2f}ms]"
            if check:
                correct = "correct" if self.is_correct() else "wrong"
                lines.insert(
                    0,
                    header
                    + f" {placeholder:15} {correct:10} {total_cost:10.3f}ms {note}",
                )
            else:
                lines.insert(
                    0, header + f" {placeholder:15} {total_cost:10.3f}ms {note}"
                )

        elif len(self.methods) == 1:
            method = list(self.methods.values())[0]
            line = method.print(header, None, answer=answer)
            if self.timeout_ext > 0.0:
                line += f" [+{self.timeout_ext:.2f}ms]"
            lines.append(line)

        else:
            header += " NO SOLUTION"
            lines.append(header)

        return "\n".join(lines)

    def solve(self, runner: Runner, name: str = None, timeout: float = 1000.0) -> None:
        """
        Solve the problem.
        """
        for key, method in self.methods.items():
            if name is not None and key != name:
                continue

            method.solve(runner, timeout=timeout + self.timeout_ext)


def _return_zero() -> int:
    return 0


class Job:
    """
    Run job
    """

    def __init__(self, func: Callable[[], int]):
        self.func = func

    def run(self) -> (int, float):
        """
        Run function
        """
        result = _TimeoutResult()
        time_start = time.perf_counter()
        result = self.func()
        time_finish = time.perf_counter()
        dt = 1000.0 * (time_finish - time_start)
        return result, dt


class Runner:
    """
    Runner of all problem solvers, with managed process pool.
    """

    pool: multiprocessing.Pool

    def __init__(self):
        self.pool = None

    def reset_pool(self) -> None:
        """
        Reset the process pool.
        """
        if self.pool is not None:
            self.pool.terminate()
            self.pool.close()

        self.pool = multiprocessing.Pool(processes=1)
        self.run_func(_return_zero)  # warm up worker process

    def run_func(self, func, timeout: float = 1000.0) -> tuple[int, bool, float]:
        """
        Run a function.
        """
        job = Job(func)
        is_timeout = False
        result = _TimeoutResult()
        time_start = time.perf_counter()

        try:
            r = self.pool.apply_async(job.run)
            result, dt = r.get(timeout=timeout / 1000.0)

        except multiprocessing.TimeoutError:
            time_finish = time.perf_counter()
            dt = 1000.0 * (time_finish - time_start)
            self.reset_pool()
            is_timeout = True

        return result, is_timeout, dt


def _natural_filename(filename: str) -> Iterable[str | int]:
    parts = []
    i = 0
    buf, flag = [], "char"
    while i < len(filename):
        c = filename[i]
        cf = "digit" if c.isdigit() else "char"
        if cf != flag:
            n = "".join(buf)
            if flag == "digit":
                n = int(n)

            parts.append(n)
            flag = cf
            buf = []

        buf.append(c)
        i += 1

    if len(buf) > 0:
        n = "".join(buf)
        if flag == "digit":
            n = int(n)

        parts.append(n)

    return parts


def import_solver(module_name: str) -> ProblemSolver:
    """
    Import a problem solver.
    """
    mod = importlib.import_module(f"{module_name}")
    required_attrs = ["PID"]
    for attr in required_attrs:
        if not hasattr(mod, attr):
            raise RuntimeError(f"Missing attribute {attr} in {module_name}")

    solver = ProblemSolver(mod.PID)
    solver.set_document(mod.__doc__)

    if hasattr(mod, "ANSWER"):
        solver.answer = mod.ANSWER

    if hasattr(mod, "TIMEOUT_EXT"):
        solver.timeout_ext = mod.TIMEOUT_EXT

    for name, func in inspect.getmembers(mod, inspect.isfunction):
        if name == "solve":
            solver.add_method(func, "", func.__doc__)

        elif len(name) > 6 and name.startswith("solve_"):
            solver.add_method(func, name[6:], func.__doc__)

        else:
            continue

    return solver


def find_problem_solvers(
    dirname: str, id_list: Iterable[int] = None
) -> Generator[ProblemSolver, None, None]:
    """
    Find all problem solvers in given directory.
    """
    target_dir = f"{dirname}"

    id_set = set(id_list or [])
    file_list = os.listdir(target_dir)
    file_natural_list = [
        (filename, _natural_filename(filename)) for filename in file_list
    ]
    file_natural_list.sort(key=lambda x: x[1])
    for filename, _ in file_natural_list:
        if not filename.endswith(".py"):
            continue

        base_name = filename[0:-3]
        if base_name == "__init__":
            continue

        package_name = dirname.replace("/", ".")
        module_name = f"{package_name}.{base_name}"

        try:
            solver = import_solver(module_name)
            if len(id_set) > 0 and solver.pid not in id_set:
                continue

            yield solver

        except ImportError as ex:
            print(f"Failed to import {module_name}: {ex}")

        except SyntaxError as ex:
            print(f"Syntax error in {module_name}/{filename}: {ex}")


def do_list(id_list: Iterable[int], full: bool):
    """
    List problems.
    """
    for problem in find_problem_solvers(PROBLEM_DIR, id_list=id_list):
        print(f"{problem.pid:<5d} {problem.title}")
        if full:
            print(_add_indent(problem.content, "      "))
            print()


def _return_zero() -> int:
    return 0


def do_run(id_list: Iterable[int], timeout: float, check: bool):
    """
    Run problems.
    """
    runner = Runner()
    runner.reset_pool()

    retcode = 0
    for problem in find_problem_solvers(PROBLEM_DIR, id_list=id_list):
        problem.solve(runner, timeout=timeout)
        line = problem.print(check=check)
        if check and not problem.is_correct():
            retcode = 1

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
