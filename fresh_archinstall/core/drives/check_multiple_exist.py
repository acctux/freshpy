import os
from pathlib import Path


def list_exists_in_dir(key_files: list[Path], key_dir: Path):
    """Check if key files exist in KEY_DIR."""
    return all(os.path.isfile(os.path.join(key_dir, f)) for f in key_files)
