from pathlib import Path
import logging
from src.etc_missing_exists_list import missing_exists_list
from src.relative_f_locations import get_relative_f_locations

ETC_DOTS_DIR = Path("~/Lit/dotfiles/etc/ly").expanduser()
BACKUP_DIR = Path("~/dotcetera").expanduser()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    if not ETC_DOTS_DIR.is_dir():
        logger.info(f"You have no dots at {ETC_DOTS_DIR}!")
        return
    if not BACKUP_DIR.is_dir():
        logger.info(f"Creating directory: {BACKUP_DIR}")
        BACKUP_DIR.parent.mkdir(parents=True, exist_ok=True)
    rel_locations = get_relative_f_locations(ETC_DOTS_DIR)

    existing_files, missing_files = missing_exists_list(rel_locations)

    for location in existing_files:
        logger.info("Files to replace: %s", location)
    for missing in missing_files:
        logger.info("Files to create: %s", missing)
    # shutil.copy2(target_path, backup_path)


if __name__ == "__main__":
    main()
    # backup_etc_file(location, location.name)

# import shutil

# from src.etc_backup import backup_etc_file
# for rel_location in rel_locations:

#     if rel_location.is_file():

# diff_file_paths = create_multiple_diffs(etc_file_locations)
# print(f"check out{diff_file_paths} and {etc_file_locations}")

# ensure_file_ready()
# """Main execution function to load the config, loop through, and apply patches."""
# if os.geteuid() != 0:
#     print("\n[CRITICAL] This script must be run with root privileges (sudo).\n")
#     exit(1)
# else:
# create_patch_list
# ensure_file_ready
# process_patches
