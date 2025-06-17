"""
Concurrent File Stats Processor – Python stub.

Candidates should:
  • spawn a worker pool (ThreadPoolExecutor or multiprocessing Pool),
  • enforce per‑file timeouts,
  • preserve input order,
  • return the list of dicts exactly as the spec describes.
"""
from __future__ import annotations, print_function
from typing import List, Dict

import pathlib, time
_DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
_FILELIST = _DATA_DIR / "filelist.txt"


def process_file(path: str) -> Dict:
    try:
        curr_file = pathlib.Path(path).read_text()
        lines = curr_file.splitlines()
        words = sum(len(line.strip().split()) for line in lines)
        return {"path": path, "lines": len(lines), "words": words, "status": "ok"}
    except TimeoutError:
        return {"path": path, "status": "timeout"}


def aggregate(filelist_path: str, workers: int = 4, timeout: int = 2) -> List[Dict]:
    """
    Process every path listed in *filelist_path* concurrently.

    Returns a list of dictionaries in the *same order* as the incoming paths.

    Each dictionary must contain:
        {"path": str, "lines": int, "words": int, "status": "ok"}
    or, on timeout:
        {"path": str, "status": "timeout"}

    Parameters
    ----------
    filelist_path : str
        Path to text file containing one relative file path per line.
    workers : int
        Maximum number of concurrent worker threads.
    timeout : int
        Per‑file timeout budget in **seconds**.
    """
    print("Starting aggregation...")
    filelist = open(filelist_path).read().splitlines()
    base_dir = pathlib.Path(filelist_path).parent

    for rel_path in filelist:
        full_path = (base_dir / rel_path).resolve()
        result = process_file(str(full_path))
        print(result)

aggregate(str(_FILELIST), workers=8, timeout=2)
