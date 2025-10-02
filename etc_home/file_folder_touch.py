from pathlib import Path


def touch_folders_file(dest_file: Path):
    """Creates the parent directory and ensures the destination file exists."""
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    dest_file.touch()
