from pathlib import Path
import logging
import yaml

from etc_home.ansible_player import run_ansible_playbook
from etc_home.location_lists_from_rel import make_path_lists_from_rel_list
from etc_home.locs_from_path import list_to_rel_locs_lists
from etc_home.run_cmd_diff import run_cmd_one_diff


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DOTS_DIR = Path("~/Lit/dotfiles").expanduser()
ETC_DOTS_DIR = DOTS_DIR / "etc"
DIFFS_DIR = Path("~/dotceta").expanduser()
COPY_LIST_YAML = DOTS_DIR / "playbook.yml"


def main(rel_locations_list: list[Path]):
    if not DIFFS_DIR.exists():
        DIFFS_DIR.mkdir()

    # Generate list of relative locations from ETC_DOTS_DIR
    rel_locations_list = list_to_rel_locs_lists(ETC_DOTS_DIR)
    etc_files, dot_files, diff_files, files_to_yaml = make_path_lists_from_rel_list(
        DIFFS_DIR,
        rel_locations_list,
    )

    # Save files_to_yaml to COPY_LIST_YAML
    logger.info(f"Saving files_to_yaml to {COPY_LIST_YAML}")
    with COPY_LIST_YAML.open("w") as yaml_file:
        yaml.dump({"files_to_yaml": files_to_yaml}, yaml_file, indent=2)
        print(f"✅ Patch list saved to {COPY_LIST_YAML.resolve()}")
    # Ensure the lengths match and the files exist
    if (
        etc_files
        and dot_files
        and diff_files
        and len(etc_files) == len(dot_files) == len(diff_files)
    ):
        for etc_file, dot_file, diff_file in zip(etc_files, dot_files, diff_files):
            if not etc_file.exists():
                etc_file.touch()

            # Run diff command and log the result
            _ = run_cmd_one_diff(etc_file, dot_file, diff_file)
            logger.info(f"Diff file for {etc_file} created at {diff_file}")

    run_ansible_playbook(COPY_LIST_YAML, files_to_yaml)


if __name__ == "__main__":
    main([])
