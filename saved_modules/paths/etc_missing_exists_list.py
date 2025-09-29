from pathlib import Path


def missing_exists_list(relative_paths: list[Path]) -> tuple[list[Path], list[Path]]:
    existing_files: list[Path] = []
    missing_files: list[Path] = []
    for relative_path in relative_paths:
        target_path = Path("/etc") / relative_path
        # Check if path exists and is a file (not a symlink or directory)
        if target_path.exists() and target_path.is_file():
            existing_files.append(target_path)
        else:
            missing_files.append(target_path)
    return existing_files, missing_files
