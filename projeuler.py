#!/usr/bin/env python3
# coding: utf-8


"""
Main entry, runner of all problem solutions.
"""


from __future__ import annotations

import os
import sys
import ctypes
import platform
import inspect
import importlib
import argparse
import time
import multiprocessing

from datetime import datetime
from typing import (
    cast,
    Callable,
    Iterable,
    Iterator,
    Mapping,
)


import data


if sys.platform == "win32":
    from ctypes import wintypes

    WIN_DLL = ctypes.LibraryLoader(ctypes.WinDLL)
else:
    WIN_DLL = None


PROBLEM_DIR = "problems"

OUTPUT_STREAM = sys.stdout


def _win_get_curse_position(handle) -> tuple[int, int]:
    if sys.platform != "win32":
        return 0, 0

    class _ScreenBufferInfo(ctypes.Structure):
        # pylint: disable=too-few-public-methods, protected-access, used-before-assignment
        _fields_ = [
            ("dwSize", wintypes._COORD),
            ("dwCursorPosition", wintypes._COORD),
            ("wAttributes", wintypes.WORD),
            ("srWindow", wintypes.SMALL_RECT),
            ("dwMaximumWindowSize", wintypes._COORD),
        ]

    win32api_get_screen_buffer_info = WIN_DLL.kernel32.GetConsoleScreenBufferInfo
    win32api_get_screen_buffer_info.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(_ScreenBufferInfo),
    ]
    win32api_get_screen_buffer_info.restype = wintypes.BOOL

    info = _ScreenBufferInfo()
    win32api_get_screen_buffer_info(handle, ctypes.byref(info))
    x = cast(int, info.dwCursorPosition.X)
    y = cast(int, info.dwCursorPosition.Y)
    return x, y


IS_WINDOWS_LEGACY_TERMINAL = False
if sys.platform == "win32":
    _Win32APIGetStdHandle = WIN_DLL.kernel32.GetStdHandle
    _Win32APIGetStdHandle.argtypes = [wintypes.DWORD]
    _Win32APIGetStdHandle.restype = wintypes.HANDLE

    _handle = cast(wintypes.HANDLE, _Win32APIGetStdHandle(-11))
    _x0, _ = _win_get_curse_position(_handle)
    print("\033[D", end="", flush=True)  # move cursor to left
    _x1, _ = _win_get_curse_position(_handle)
    if _x1 - _x0 > 1:
        IS_WINDOWS_LEGACY_TERMINAL = True
        print("\b" * (_x1 - _x0), end="", flush=True)


class ProblemId:
    """
    Problem ID.
    """

    pid: int
    method: str

    def __init__(self, pid: int | str):
        if isinstance(pid, str):
            if "." in pid:
                pid, method = pid.split(".")
                self.pid = int(pid)
                self.method = method
            else:
                self.pid = int(pid)
                self.method = None

        elif isinstance(pid, int):
            self.pid = pid
            self.method = None

    def __eq__(self, other: ProblemId | int) -> bool:
        if isinstance(other, int):
            return self.pid == other

        if isinstance(other, ProblemId):
            return self.pid == other.pid and self.method == other.method

        return False

    def problem_name(self) -> str:
        """
        Get the filename of this problem.
        """
        return f"p{self.pid:04d}"


class RunConfigure:
    """
    Run configuration.
    """

    check: bool
    strict: bool
    timeout: float
    preload: bool
    id_list: Iterable[ProblemId]

    def __init__(self):
        self.check = False
        self.strict = False
        self.timeout = 5000.0
        self.preload = True
        self.id_list = []

    @staticmethod
    def from_parser(result: argparse.Namespace) -> RunConfigure:
        """
        Create a run configuration from parser result.
        """
        conf = RunConfigure()
        conf.check = result.check
        conf.strict = result.strict
        conf.timeout = result.timeout
        conf.preload = not result.no_preload
        conf.id_list = result.id
        if result.no_timeout:
            conf.timeout = 0.0
        return conf


_default_run_configure = RunConfigure()


class _TimeSpanInMs(float):
    """
    Time span in milliseconds.
    """

    def __new__(cls, value: float | str):
        if isinstance(value, str):
            if value.endswith("ms"):
                value = float(value[0:-2])

            elif value.endswith("s"):
                value = float(value[0:-1]) * 1000.0

            else:
                value = float(value)

        return super().__new__(cls, value)


def _get_parser():
    parser = argparse.ArgumentParser(description="Project Euler problem runner")

    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    cmd_list = subparsers.add_parser("list", help="list all problems")
    cmd_list.add_argument(
        "-f", "--full", action="store_true", help="show full information"
    )
    cmd_list.add_argument(
        "id", nargs="*", type=ProblemId, help="show specific problem information"
    )

    cmd_create = subparsers.add_parser("create", help="create solutions of problems")
    cmd_create.add_argument("id", nargs="*", type=int, help="create specific problems")

    cmd_run = subparsers.add_parser("run", help="run problems")
    cmd_run.add_argument(
        "-c", "--check", action="store_true", help="check the solution answer"
    )
    cmd_run.add_argument(
        "--strict",
        action="store_true",
        help="run check in strict mode, all methods MUST be correct",
    )
    cmd_run.add_argument(
        "--no-preload", action="store_true", help="do not preload data"
    )
    cmd_run.add_argument(
        "-t",
        "--timeout",
        type=_TimeSpanInMs,
        default=5000.0,
        help="timeout for each method of a problem, in milliseconds, "
        + "or with unit like 500ms, 10s, 1m",
    )
    cmd_run.add_argument("--no-timeout", action="store_true", help="disable timeout")
    cmd_run.add_argument("id", nargs="*", type=ProblemId, help="run specific problems")

    return parser


COLOUR_MAP = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    "brightblack": 90,
    "brightred": 91,
    "brightgreen": 92,
    "brightyellow": 93,
    "brightblue": 94,
    "brightmagenta": 95,
    "brightcyan": 96,
    "brightwhite": 97,
}


def _get_colour_str(s: str, colour: str, is_tty: bool) -> str:
    if not is_tty:
        return s

    if platform.system() == "Windows" and IS_WINDOWS_LEGACY_TERMINAL:
        # Legacy Windows command prompt does not support ANSI escape code
        return s

    if colour not in COLOUR_MAP:
        return s

    return f"\033[{COLOUR_MAP[colour]}m{s}\033[0m"


class _ColourOutMeta(type):
    """
    Colour output meta class.
    """

    def __getattr__(cls, colour):
        def _colour_print(s: str, is_tty: bool) -> None:
            return _get_colour_str(s, colour, is_tty)

        return _colour_print


class ClrOut(metaclass=_ColourOutMeta):
    """
    Colour output.
    """

    @staticmethod
    def write(s: str, colour: str, is_tty: bool) -> str:
        """
        Write a string with colour.
        """
        return _get_colour_str(s, colour, is_tty)


def _add_indent(s: str, indent: str) -> str:
    lines = s.split("\n")
    result = [indent + line for line in lines]
    return "\n".join(result)


class _NotRunResult:
    def __repr__(self) -> str:
        return "NOT RUN"


class _TimeoutResult:
    def __repr__(self) -> str:
        return "TIMEOUT"


class SolutionMethod:
    """
    Solution method
    """

    def __init__(
        self, module_name: str, func: Callable[[], int], name: str, note: str = ""
    ):
        self.module_name = module_name
        self.func = func
        self.name = name
        self.note = note or ""
        self.time_cost = 0.0
        self.result = _NotRunResult()
        self.finished = False

    def _proc_main(self, queue: multiprocessing.Queue):
        result = _NotRunResult()
        time_start = time.perf_counter()
        result = self.func()
        time_finish = time.perf_counter()
        dt = 1000.0 * (time_finish - time_start)

        queue.put((result, dt))

    def solve(self, runner: Runner, conf: RunConfigure, timeout: float = 0.0) -> None:
        """
        Run the solution method.
        """
        result, timeout, cost = runner.run_func(
            self.module_name, self.func, conf=conf, timeout=timeout
        )
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

    def print(
        self, title: str, suffix: str | None, answer: int = None, is_tty: bool = False
    ) -> str:
        """
        Print result of this method.
        """
        line = [f"{title}"]

        if self.result is None:
            r = "NO RESULT"
            c = "red"
        else:
            r = f"{self.result}"
            c = None

        line.append(ClrOut.write(f" {r:<15}", c, is_tty))

        if answer is not None:
            if self.is_timeout():
                rc = "timeout"
                cl = "yellow"

            elif self.result is None:
                rc = "NO ANSWER"
                cl = "yellow"

            elif answer == self.result:
                rc = "correct"
                cl = "green"

            else:
                rc = "wrong"
                cl = "red"

            line.append(ClrOut.write(f" {rc:10}", cl, is_tty))

        if self.time_cost < 200.0:
            cost_colour = "green"
        elif self.time_cost < 500.0:
            cost_colour = "cyan"
        elif self.time_cost < 2000.0:
            cost_colour = "yellow"
        else:
            cost_colour = "red"

        if not self.result:
            cost_colour = None

        line.append(ClrOut.write(f" {self.time_cost:10.3f}ms", cost_colour, is_tty))
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
    module_name: str = ""
    timeout_ext: float = 0.0
    has_extra_data: str = ""
    __doc__ = ""

    def __init__(self, pid: int, module_name: str):
        self.module_name = module_name
        self.pid = pid
        self.answer = None
        self._method_names = []
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

        method = SolutionMethod(self.module_name, func, name, note)
        self._method_names.append(name)
        self.methods[name] = method

    def each_methods(self) -> Iterator[tuple[str, SolutionMethod]]:
        """
        Iterate all methods.
        """
        for name in self._method_names:
            yield name, self.methods[name]

    def _is_correct(self) -> bool:
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
                result = result or False
                continue

            result = result or True

        return result

    def _is_all_correct(self) -> bool:
        """
        Is all methods correct.
        """
        for method in self.methods.values():
            if method.is_timeout():
                continue

            if method.result is None:
                continue

            if self.answer is not None and method.result != self.answer:
                return False

        return True

    def is_correct(self, strict: bool = False) -> bool:
        """
        Is the solution correct.
        """
        if strict:
            return self._is_all_correct()

        return self._is_correct()

    def find_best_solution(self, check: bool = False) -> str:
        """
        Find the best solution.
        """
        cost = None
        best = None
        for name, method in self.each_methods():
            if method.is_timeout():
                continue

            if method.result is None:
                continue

            if check and self.answer is not None and method.result != self.answer:
                continue

            if cost is None or method.time_cost < cost:
                cost = method.time_cost
                best = name

        return best

    def print(
        self, check: bool = False, strict: bool = False, is_tty: bool = False
    ) -> str:
        """
        Print result of a problem solver.
        """
        lines = []

        answer = self.answer
        if not check:
            answer = None
        header = f"{self.pid:<5} {self.title:.<40}"
        if len(self.methods) > 1:
            best = self.find_best_solution(check=check)
            total_cost = 0.0
            for name, method in self.each_methods():
                suffix = "*BEST" if name == best else None
                title = f"      + {method.title:.<38}"
                line = method.print(title, suffix, answer=answer, is_tty=is_tty)
                lines.append(line)
                total_cost += method.time_cost

            placeholder = ""
            note = ""
            if self.timeout_ext > 0.0:
                note = f"[+{self.timeout_ext:.2f}ms]"

            if check:
                correct = (
                    ClrOut.green("correct   ", is_tty)
                    if self.is_correct(strict=strict)
                    else ClrOut.red("wrong     ", is_tty)
                )
                header += f" {placeholder:15} {correct} {total_cost:10.3f}ms {note}"
                lines.insert(0, header)
            else:
                header += f" {placeholder:15} {total_cost:10.3f}ms {note}"
                lines.insert(0, header)

        elif len(self.methods) == 1:
            method = list(self.methods.values())[0]
            line = method.print(header, None, answer=answer, is_tty=is_tty)
            if self.timeout_ext > 0.0:
                line += f" [+{self.timeout_ext:.2f}ms]"
            lines.append(line)

        else:
            header += " NO SOLUTION"
            lines.append(header)

        return "\n".join(lines)

    def solve(self, runner: Runner, conf: RunConfigure, name: str = None) -> None:
        """
        Solve the problem.
        """
        for key, method in self.each_methods():
            if name is not None and key != name:
                continue

            params = {}
            if conf.timeout > 0.0:
                params["timeout"] = conf.timeout + self.timeout_ext
            method.solve(runner, conf=conf, **params)

        data.reset()


def _return_zero() -> int:
    return 0


class Job:
    """
    Run job
    """

    def __init__(self, module_name: str, func: Callable[[], int]):
        self.func = func
        self.module_name = module_name
        self.preload = True

    def run(self) -> (int, float):
        """
        Run function
        """
        data.try_preload(f"data.{self.module_name}")
        if not self.preload:
            data.reset()

        result = _NotRunResult()
        time_start = time.perf_counter()
        try:
            result = self.func()
            time_finish = time.perf_counter()
            dt = 1000.0 * (time_finish - time_start)
            return result, dt

        except KeyboardInterrupt:
            return result, 0.0


class Runner:
    """
    Runner of all problem solvers, with managed process pool.
    """

    pool: multiprocessing.Pool

    def __init__(self):
        self.pool = None

    def close(self) -> None:
        """
        Close the process pool.
        """
        if self.pool is not None:
            self.pool.terminate()
            self.pool.close()
            self.pool = None

    def reset_pool(self) -> None:
        """
        Reset the process pool.
        """
        self.close()
        self.pool = multiprocessing.Pool(processes=1)
        self.run_func(
            "", _return_zero, _default_run_configure
        )  # warm up worker process

    def run_func(
        self, name: str, func, conf: RunConfigure, timeout: float = 0.0
    ) -> tuple[int, bool, float]:
        """
        Run a function.
        """
        job = Job(name, func)
        job.preload = conf.preload

        is_timeout = False
        result = _NotRunResult()
        time_start = time.perf_counter()
        get_params = {}
        if timeout > 0.0:
            get_params["timeout"] = timeout / 1000.0

        try:
            r = self.pool.apply_async(job.run)
            result, dt = r.get(**get_params)

        except multiprocessing.TimeoutError:
            time_finish = time.perf_counter()
            result = _TimeoutResult()
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


def import_solver(module_name: str, base_name: str) -> ProblemSolver:
    """
    Import a problem solver.
    """
    mod = importlib.import_module(f"{module_name}")
    try:
        pid = int(base_name[1:])

    except ValueError as ex:
        raise ValueError(
            f"Invalid problem name: '{base_name}', "
            + "should be pXXXX which XXXX is a number"
        ) from ex

    solver = ProblemSolver(pid, base_name)
    solver.set_document(mod.__doc__)

    if hasattr(mod, "ANSWER"):
        solver.answer = mod.ANSWER

    if hasattr(mod, "TIMEOUT_EXT"):
        solver.timeout_ext = mod.TIMEOUT_EXT

    for name, func in inspect.getmembers(mod, inspect.isfunction):
        # inspect.getmembers() returns all members sorted by name
        if name == "solve":
            solver.add_method(func, "", func.__doc__)

        elif len(name) > 6 and name.startswith("solve_"):
            solver.add_method(func, name[6:], func.__doc__)

        else:
            continue

    return solver


def check_extra_data(module_name: str) -> bool:
    """
    Check if there is extra data for a problem.
    """
    try:
        mod = importlib.import_module(f"{module_name}")
        if not hasattr(mod, "load"):
            return False

        return True

    except ImportError:
        return False


def find_problem_solvers(
    dirname: str, id_list: Iterable[ProblemId] = None
) -> Iterator[tuple[ProblemId | None, ProblemSolver]]:
    """
    Find all problem solvers in given directory.
    """
    target_dir = f"{dirname}"

    id_map = {pid.pid: pid for pid in (id_list or [])}
    if id_list is not None and len(id_list) > 0:
        file_list = [f"{pid.problem_name()}.py" for pid in id_list]
    else:
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
        data_name = f"data.{base_name}"

        try:
            solver = import_solver(module_name, base_name)
            if len(id_map) > 0 and solver.pid not in id_map:
                continue

            pid = id_map.get(solver.pid)
            if check_extra_data(data_name):
                solver.has_extra_data = data_name

            yield pid, solver

        except ImportError as ex:
            print(f"Failed to import {module_name}: {ex}")

        except SyntaxError as ex:
            print(f"Syntax error in {module_name}/{filename}: {ex}")


def do_list(id_list: Iterable[ProblemId], full: bool):
    """
    List problems.
    """
    for _, problem in find_problem_solvers(PROBLEM_DIR, id_list=id_list):
        print(f"{problem.pid:<5d} {problem.title}")
        if full:
            print(_add_indent(problem.content, "      "))
            print()


def do_create(id_list: Iterable[int]):
    """
    Create solution of a problem.
    """
    for pid in id_list:
        filename = f"p{pid:04d}.py"
        filepath = os.path.join(PROBLEM_DIR, filename)
        if os.path.exists(filepath):
            print(f"File {filepath} already exists")
            continue

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(
                "#!/usr/bin/env python3\n"
                "# coding: utf-8\n"
                "\n"
                "\n"
                '"""\n'
                "Problem title\n"
                "\n"
                "Problem description\n"
                '"""\n'
                "\n"
                "\n"
                "ANSWER = None\n"
                "\n"
                "\n"
                "def solve() -> int:\n"
                "    return 0\n"
            )


def _return_zero() -> int:
    return 0


def do_run(conf: RunConfigure):
    """
    Run problems.
    """
    runner = Runner()
    runner.reset_pool()

    retcode = 0
    success, count, methods = 0, 0, 0
    time_start = datetime.now()
    is_tty = sys.stdout.isatty()
    try:
        for pid, problem in find_problem_solvers(PROBLEM_DIR, id_list=conf.id_list):
            name = None
            if pid is not None:
                name = pid.method

            problem.solve(runner, conf=conf, name=name)
            line = problem.print(check=conf.check, strict=conf.strict, is_tty=is_tty)
            if conf.check:
                if problem.is_correct(strict=conf.strict):
                    success += 1
                else:
                    retcode = 1

            print(line)
            count += 1
            methods += len(problem.methods)

        time_finish = datetime.now()
        dt = (time_finish - time_start).total_seconds()
        if conf.check:
            print(f"Solved {success}/{count} problems in {dt:.3f}s")
        else:
            print(f"Solved {count} problems solved in {dt:.3f}s")

    except KeyboardInterrupt:
        print("Interrupted by user")
        retcode = 1

    finally:
        runner.close()

    sys.exit(retcode)


def main():
    """
    Main entry.
    """
    parser = _get_parser()
    args = parser.parse_args()

    if args.command == "list":
        do_list(args.id, args.full)

    elif args.command == "create":
        do_create(args.id)

    elif args.command == "run":
        conf = RunConfigure.from_parser(args)
        do_run(conf)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
