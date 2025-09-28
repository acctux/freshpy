from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parent_dir_touch(dest_path: Path):
    """Creates the parent directory and ensures the destination file exists."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created {dest_path}.")
