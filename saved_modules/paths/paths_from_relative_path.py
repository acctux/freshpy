from pathlib import Path

from main import ETC_DOTS_DIR
from main import DIFFS_DIR


def make_lists_paths_from_rel(
    etc_file_locations: list[Path],
) -> tuple[list[Path], list[Path], list[Path]]:
    """Generate three lists of paths for system files, dotfiles, and their diff patches."""
    etc_root = Path("/etc")
    etc_files: list[Path] = []
    dotfiles: list[Path] = []
    patch_files: list[Path] = []

    for rel_path in etc_file_locations:
        etc_file = etc_root / rel_path
        dotfile = ETC_DOTS_DIR / rel_path
        patch_file = DIFFS_DIR / f"{rel_path.name}.patch"

        etc_files.append(etc_file)
        dotfiles.append(dotfile)
        patch_files.append(patch_file)

    return etc_files, dotfiles, patch_files
