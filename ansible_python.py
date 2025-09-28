from pathlib import Path
import yaml
import json  # Added for JSON writing

PATCH_LIST_JSON = Path("~/fresh/patchlist.json").expanduser()
DOTS_DIR = Path("~/Lit/dotfiles/etc").expanduser()


def create_patch_list(dots_dir: Path) -> list[dict[str, str]]:
    files_to_copy: list[dict[str, str]] = []

    if not dots_dir.is_dir():
        print(f"❌ Error: Source directory not found at {dots_dir.resolve()}")
        return files_to_copy

    print(f"--- Scanning {dots_dir.name} for files... ---")

    for src_file in dots_dir.rglob("*"):
        if src_file.is_file():
            rel_path = src_file.relative_to(dots_dir)
            print(f"Found file: {rel_path}")
            src_path = str(
                Path("etc") / f"{rel_path}.diff"
            )  # Append .diff for source file
            dest_path = str(
                Path("/etc") / rel_path
            )  # Destination path remains the same
            files_to_copy.append({"src": src_path, "dest": dest_path})

    return files_to_copy


def main():
    patch_list = create_patch_list(DOTS_DIR)

    # Print the output in YAML format
    print(yaml.dump({"files_to_copy": patch_list}, default_flow_style=False))

    # Write the output to the PATCH_LIST_JSON file as JSON
    with PATCH_LIST_JSON.open("w") as json_file:
        json.dump({"files_to_copy": patch_list}, json_file, indent=2)
        print(f"✅ Patch list saved to {PATCH_LIST_JSON.resolve()}")


if __name__ == "__main__":
    main()
