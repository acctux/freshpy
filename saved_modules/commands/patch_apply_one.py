import subprocess
from pathlib import Path


def apply_one_patch(
    src_diff: str | Path, dest_file: str | Path
) -> subprocess.CompletedProcess[str] | None:
    """
    Applies the diff file to the destination file using the 'patch' command.
    Returns the subprocess.CompletedProcess result object on execution, or None if skipped.
    """
    src_path = Path(src_diff)
    dest_path = Path(dest_file)

    if not src_path.is_file():
        print(f"  [SKIPPED] Patch source file not found: {src_diff}")
        return None

    cmd: list[str] = [
        "sudo",
        "patch",
        "-p0",  # Strip level 0
        "-N",  # Ignore if already applied
        "-i",
        str(src_path),
        str(dest_path),
    ]

    result = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
    )
    return result
