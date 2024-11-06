import sys
from pathlib import Path
from importlib import import_module

# Merge stderr into stdout
sys.stderr = sys.stdout

from . import Test

tests: list[str] = []

for test in Path(__file__).parent.glob("*.py"):
    if not test.is_file() or test.name.startswith("__"):
        continue
    tests.append(test.stem)

tests.sort()

# with Logger.use(progress.write):
for test in tests:
    title = f" {test} "
    pad = "=" * (60 - len(title))
    print(pad[: len(pad) // 2] + title + pad[len(pad) // 2 :])
    import_module(f".{test}", package="tests")

sys.exit(Test.summary())
