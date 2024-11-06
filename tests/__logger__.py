# ==============================================================================
# Author: Yuxuan Zhang (robotics@z-yx.cc)
# License: MIT
# ==============================================================================
import sys
from pathlib import Path
from termcolor import colored
from typing import Callable, Any
from contextlib import contextmanager

HOME = Path(__file__).parent.parent

class Logger:
    kwargs = {}

    @staticmethod
    def print(msg: str, end="\n", **kwargs):
        sys.stderr.write(msg + end)
        sys.stderr.flush()

    def __init__(self, src: str, **kwargs):
        """
        Usage: logger = Logger(__file__)
        """
        try:
            ID = str(Path(src).relative_to(HOME))
        except:
            ID = src
        self.debug = Logger.create(ID, "DEBUG", "blue", "cyan", self)
        self.verbose = Logger.create(ID, "VERBOSE", "light_grey", "light_grey", self)
        self.info = Logger.create(ID, "INFO", "green", "white", self)
        self.warn = Logger.create(ID, "WARN", "yellow", "light_yellow", self)
        self.error = Logger.create(ID, "ERROR", "red", "light_red", self)

    def __call__(self, other_logger):
        """
        Use provided logger for levels defined by it.
        """
        for key in ["debug", "verbose", "info", "warn", "error"]:
            if hasattr(other_logger, key):
                other = getattr(other_logger, key)
                if callable(other):
                    setattr(self, key, other)

    @contextmanager
    @staticmethod
    def use(alternative_print: Callable[[str], Any]):
        """
        Temporarily use a different print function.
        """
        print = Logger.print
        Logger.print = alternative_print
        yield
        Logger.print = print

    @staticmethod
    def compose(
        level: str,
        ID: str | None,
        msgs: list[str],
        sep: str,
        level_color: str | None,
        msg_color: str | None,
        print: Callable[[str], Any],
        print_kw: dict[str, Any],
    ):
        if ID is None:
            ID = ""
        else:
            ID = colored(f" {ID}:", "light_grey")

        if level is None:
            level = ""
        else:
            level = f"[{level.upper().center(6)}]"
            if level_color is not None:
                level = colored(level, level_color)

        msg = sep.join(map(str, msgs))
        if msg_color is not None:
            msg = colored(msg, msg_color)
        print(f"{level}{ID} {msg}", **print_kw)

    @staticmethod
    def create(
        ID: str | None,
        level: str | None,
        level_color: str | None = None,
        msg_color: str | None = None,
        logger: "Logger" = None,
    ):

        def log(
            *msgs: str, ID=ID, print: Callable[[str], Any] = None, sep=" ", **kwargs
        ):
            if print is None:
                # Mutable default argument cannot initialize in argument list
                print = Logger.print
            # Compose kwargs
            kw = dict(logger.kwargs) if logger is not None else dict()
            kw.update(kwargs)
            return Logger.compose(
                level=level,
                ID=ID,
                msgs=msgs,
                level_color=level_color,
                msg_color=msg_color,
                print=print,
                print_kw=kw,
                sep=sep,
            )

        return log
