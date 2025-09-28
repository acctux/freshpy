from pathlib import Path

from src.diffs.diff_multiple_logic import create_multiple_diffs
from src.setup.organize_setup import create_necessary_env

ETC_DOTS_DIR = Path("~/Lit/dotfiles/etc").expanduser()


def main():
    if not ETC_DOTS_DIR.is_dir():
        print(f"Creating {ETC_DOTS_DIR.resolve()}")
        # # `exist_ok=True` prevents an error if the directory already exists.
        ETC_DOTS_DIR.mkdir(parents=True, exist_ok=True)
    etc_file_locations = create_necessary_env(ETC_DOTS_DIR)
    diff_file_paths = create_multiple_diffs(etc_file_locations)
    print(f"check out{diff_file_paths} and {etc_file_locations}")


if __name__ == "__main__":
    main()

    # ensure_file_ready()
    # """Main execution function to load the config, loop through, and apply patches."""
    # if os.geteuid() != 0:
    #     print("\n[CRITICAL] This script must be run with root privileges (sudo).\n")
    #     exit(1)
    # else:
    # create_patch_list
    # ensure_file_ready
    # process_patches
