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
import pathlib
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FuturesTimeout
import time

def process_file(path: str) -> Dict:
    curr_file = open(path).read()
    lines = curr_file.splitlines()
    if lines and lines[0].strip().startswith("#sleep="):
        seconds = float(lines[0].strip().split("=", 1)[1])
        print(f"[INFO] Sleeping {seconds}s for {path}")
        time.sleep(seconds)
        lines = lines[1:]

    words = sum(len(line.split()) for line in lines)
    return {"path": str(pathlib.Path(pathlib.Path(path).parent.name) / pathlib.Path(path).name),
            "lines": len(lines), "words": words, "status": "ok"}

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
    filelist = open(filelist_path).read().splitlines()
    base_dir = pathlib.Path(filelist_path).parent
    results = [{} for _ in range(len(filelist))]

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_map = {}
        for i, rel_path in enumerate(filelist):
            full_path = (base_dir / rel_path).resolve()
            result = executor.submit(process_file, str(full_path))
            future_map[result] = i
        for i in future_map:
                idx = future_map[i]
                try:
                    result = i.result(timeout=timeout)
                except FuturesTimeout:
                    result = {"path": filelist[idx], "status": "timeout"}
                results[idx] = result
    sort_results = sorted(
        results,
        key=lambda x: (pathlib.Path(x["path"]).name)
    )
    print(sort_results)

    return sort_results
