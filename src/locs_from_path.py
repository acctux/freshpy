from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def list_to_rel_locs_lists(source_dir: Path) -> list[Path]:
    """
    Recursively glob directory and returns list to all files
    relative to source directory.
    """
    relative_file_locations: list[Path] = []
    # Path.rglob("*") finds all files and directories recursively
    for file in source_dir.rglob("*"):
        if file.is_file():
            relative_path = file.relative_to(source_dir)
            relative_file_locations.append(relative_path)
    logger.info("Successfully found %d files.", len(relative_file_locations))
    return relative_file_locations
