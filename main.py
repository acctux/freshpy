from pathlib import Path
import logging

from modules.etc_missing_exists_list import missing_exists_list
from modules.relative_f_locations import get_relative_f_locations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ETC_DOTS_DIR = Path("~/Lit/dotfiles/etc").expanduser()
DOTS_DIR = Path("~/Lit/dotfiles/etc").expanduser()


def main():
    new_copies, overwrite_copies = get_relative_f_locations(ETC_DOTS_DIR)
    missing_exists_list(ETC_DOTS_DIR)
    for path in rel_paths:
        if path.exists() and path.is_file():
            logger.info(f"{path} exists and will be overwritten, doing nothing.")
        else:
            logger.info(f"Creating necessary path, {path}.")
            parent_dir_touch(path)


if __name__ == "__main__":
    main()
