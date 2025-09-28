from pathlib import Path
import yaml

COPY_LIST_YAML = Path("~/Lit/dotfiles/patchlist.yml").expanduser()
DOTS_DIR = Path("~/Lit/dotfiles/etc").expanduser()


def create_patch_list(dots_dir: list[str]) -> list[str]:
    files_to_copy: list[dict[str, str]] = []

    for src_file in DOTS_DIR.rglob("*"):
        if src_file.is_file():
            rel_path = src_file.relative_to(DOTS_DIR)
            print(f"Found file: {rel_path}")
            src_path = str(Path("etc") / f"{rel_path}")
            dest_path = str(
                Path("/etc") / rel_path
            )  # Destination path remains the same
            files_to_copy.append({"src": src_path, "dest": dest_path})

    return files_to_copy


def main():
    if not DOTS_DIR.is_dir():
        print(f"❌ Error: Source directory not found at {DOTS_DIR.resolve()}")
        return
    print(f"--- Scanning {DOTS_DIR.name} for files... ---")
    copy_list = create_patch_list(DOTS_DIR)
    print(yaml.dump({"files_to_copy": copy_list}, default_flow_style=False))
    with COPY_LIST_YAML.open("w") as yaml_file:
        yaml.dump({"files_to_copy": copy_list}, yaml_file, indent=2)
        print(f"✅ Patch list saved to {COPY_LIST_YAML.resolve()}")


if __name__ == "__main__":
    main()
