from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def touch_folders_file(dest_path: Path):
    """Creates the parent directory and ensures the destination file exists."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Creating {dest_path}.")
    dest_path.touch()
