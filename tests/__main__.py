import sys
from pathlib import Path
from tqdm import tqdm
from importlib import import_module

from . import Test
from .__logger__ import Logger

tests: list[str] = []

for test in Path(__file__).parent.glob("*.py"):
    if not test.is_file() or test.name.startswith("__"):
        continue
    tests.append(test.stem)

tests.sort()

progress = tqdm(
    tests, desc="Running tests", unit="test", dynamic_ncols=True, leave=False
)
with Logger.use(progress.write):
    for test in progress:
        title = f" {test} "
        pad = "=" * (80 - len(title))
        progress.write(pad[: len(pad) // 2] + title + pad[len(pad) // 2 :])
        progress.write("")
        import_module(f".{test}", package="tests")

sys.exit(Test.summary())
