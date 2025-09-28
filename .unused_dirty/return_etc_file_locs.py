from pathlib import Path

from src.setup.relative_file_locations import get_relative_file_locations


def get_existing_file_locations(
    source_dir: Path, base_dir: Path
) -> tuple[list[Path], list[Path]]:
    relative_paths = get_relative_file_locations(source_dir)
    existing_locations: list[Path] = []
    missing_locations: list[Path] = []
    for relative_path in relative_paths:
        target_path = base_dir / relative_path
        # Check if path exists and is a file (not a symlink or directory)
        if target_path.exists() and target_path.is_file():
            existing_locations.append(target_path)
        else:
            missing_locations.append(target_path)
    return existing_locations, missing_locations
