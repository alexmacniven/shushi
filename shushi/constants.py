import os
import pathlib

APPDATA = pathlib.Path(os.environ.get("appdata"), "shushi")

for p in [APPDATA]:
    p.mkdir(exist_ok=True)
