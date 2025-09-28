from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_relative_f_locations(source_dir: Path) -> list[Path]:
    """
    Globs a directory recursively and returns a list of all file paths
    relative to the source directory.
    """
    if not source_dir.is_dir():
        # Use logger.error for critical failure/missing resource
        logger.error("Source directory not found: %s", source_dir.resolve())
        raise ValueError(f"Source directory not found: {source_dir.resolve()}")

    logger.info("Starting file scan in directory: %s", source_dir)
    relative_file_locations: list[Path] = []

    try:
        # Path.rglob("*") finds all files and directories recursively
        for file in source_dir.rglob("*"):
            if file.is_file():
                relative_path = file.relative_to(source_dir)
                relative_file_locations.append(relative_path)
                # logger.debug is good for per-file processing, but INFO is also fine
                # if you want to see every file (keeping it simple here)
                # logger.debug("Found file: %s", relative_path)

        logger.info("Successfully found %d files.", len(relative_file_locations))
        return relative_file_locations

    except PermissionError as e:
        # Use logger.exception or logger.error for exceptions, including the exception object
        logger.error("Permission denied accessing %s: %s", source_dir, e)
        raise PermissionError(f"Permission denied accessing {source_dir}") from e
