from pathlib import Path


def make_path_lists_from_rel_list(
    etc_file_locations: list[Path], dot_files: list[Path], DIFF_DIR: Path
) -> tuple[list[Path], list[Path], list[Path], list[dict[str, str]]]:
    etc_root = Path("/etc")
    etc_files: list[Path] = []
    patch_files: list[Path] = []
    files_to_yaml: list[dict[str, str]] = []

    for rel_path in etc_file_locations:
        etc_file = etc_root / rel_path
        dot_file = "etc" / rel_path
        patch_file = DIFF_DIR / f"{rel_path.name}.patch"

        etc_files.append(etc_file)
        dot_files.append(dot_file)
        patch_files.append(patch_file)
        files_to_yaml.append({"dest": str(etc_file), "src": str(dot_file)})

    return etc_files, dot_files, patch_files, files_to_yaml
