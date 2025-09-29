import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def touch_folders_file(dest_file: Path):
    """Creates the parent directory and ensures the destination file exists."""
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Creating {dest_file}.")
    dest_file.touch()
