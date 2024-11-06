# Type check tests
from type_check import TypeCheckResult, TypeCheckError, type_check
from .__logger__ import Logger

reason = Logger.create(None, "REASON", level_color="blue", msg_color="grey")
passed = Logger.create(None, "PASS", level_color="green", msg_color="white")
failed = Logger.create(None, "FAIL", level_color="red", msg_color="yellow")

total_tests = 0
failed_tests = 0


class ReprProxy:
    def __init__(self, repr):
        self.repr = repr

    def __repr__(self):
        return self.repr


class Test:
    def __init__(self, fn: callable, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def __rshift__(self, expected: bool):
        global total_tests, failed_tests
        total_tests += 1
        args = [repr(a) for a in self.args] + [f"{k}={repr(v)}" for k, v in self.kwargs.items()]
        type_rep = ReprProxy(f"{self.fn.__name__}({', '.join(args)})")
        try:
            result = self.fn(*self.args, **self.kwargs)
            if not isinstance(result, TypeCheckResult):
                # Normal termination of type guarded function
                orig = getattr(result, "__orig_class__", result.__class__)
                result = TypeCheckResult(type_rep, orig, True, None)
        except TypeCheckError as e:
            result = e.result
        except TypeError as e:
            type_error = e.with_traceback(None)
            raise type_error
        success = bool(result) == expected
        logger = passed if success else failed
        msg = [str(result)]
        if not success:
            msg.append(f"(expected {expected})")
        logger(*msg)
        if result.reason is not None:
            reason(result.reason)
        Logger.print("")  # White space
        if not success:
            failed_tests += 1
        return self

    @staticmethod
    def summary():
        global total_tests, failed_tests
        if failed_tests:
            failed(f"{failed_tests}/{total_tests} tests failed")
            return -1
        else:
            passed(f"All {total_tests} tests passed")
            return 0
