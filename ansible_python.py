from pathlib import Path
import yaml

PATCH_LIST_JSON = Path("~/fresh/patchlist.json").expanduser()


def create_patch_list(dots_dir: Path) -> list[dict[str, str]]:
    files_to_copy: list[dict[str, str]] = []

    if not dots_dir.is_dir():
        print(f"❌ Error: Source directory not found at {dots_dir.resolve()}")
        return files_to_copy

    print(f"--- Scanning {dots_dir.name} for files... ---")

    for src_file in dots_dir.rglob("*"):
        if src_file.is_file():
            rel_path = src_file.relative_to(dots_dir)

            if rel_path.parts[0] == "etc":
                src_path = str(Path("etc") / f"{rel_path}.diff"))
                dest_path = str(Path("/etc") / rel_path)
                files_to_copy.append({"src": src_path, "dest": dest_path})

    return files_to_copy


def main():
    dots_dir = Path("~/myproject/dots").expanduser()
    patch_list = create_patch_list(dots_dir)

    print(yaml.dump({"files_to_copy": patch_list}, default_flow_style=False))


if __name__ == "__main__":
    main()
