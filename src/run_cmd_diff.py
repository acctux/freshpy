import subprocess
from pathlib import Path


def run_cmd_one_diff(
    etc_file: Path, dot_file: Path, diff_file: Path
) -> subprocess.CompletedProcess[str]:
    """Helper to run the 'diff -u' command"""
    with open(diff_file, "w") as f:
        return subprocess.run(
            ["diff", "-u", etc_file, dot_file],
            capture_output=True,
            text=True,
            check=False,
            stdout=f,
        )
