from pathlib import Path
import logging
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def backup_etc_file(
    backup_dir: Path,
):
    """
    Initializes backup_dir with files from /etc, copying missing files.
    """
    backup_path = backup_dir / f"{filename}.bak"
    copy_status = shutil.copy2(target_path, backup_path)
    logger.info(
        f"Backed up {target_path} to {backup_path} with status of {copy_status}"
    )
