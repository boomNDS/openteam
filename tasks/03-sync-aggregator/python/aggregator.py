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
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
import time

def process_file(path: str) -> Dict:
    with open(path, 'r', buffering=1024*1024) as curr_file:
        lines = curr_file.readlines()
    if lines and lines[0].strip().startswith("#sleep="):
        seconds = float(lines[0].strip().split("=", 1)[1])
        time.sleep(seconds)
        lines = lines[1:]

    path_obj = pathlib.Path(path)
    rel_path = f"{path_obj.parent.name}/{path_obj.name}"
    word_count = sum(len(line.split()) for line in lines)

    return {"path": rel_path,
            "lines": len(lines),
            "words": word_count,
            "status": "ok"
    }

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
    base_dir = pathlib.Path(filelist_path).parent
    filelist = base_dir.joinpath(filelist_path).read_text().splitlines()
    results = [{} for _ in filelist]
    

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = []
        for i, rel_path in enumerate(filelist):
            full_path = base_dir / rel_path
            future = executor.submit(process_file, str(full_path))
            futures.append((future, i))

        for future, idx in futures:
            try:
                result = future.result(timeout=timeout)
            except FuturesTimeout:
                result = {"path": filelist[idx], "status": "timeout"}
            results[idx] = result

    return results
