def create_multiple_diffs():
    """Loops through all files and creates patches."""
    if not ETC_DOTS_DIR.is_dir():
        print(f"Error: Source not found at {ETC_DOTS_DIR.resolve()}")
        return

    DIFFS_DIR.mkdir(exist_ok=True)
    print(f"--- Scanning {ETC_DOTS_DIR} ---")

    for src_file in ETC_DOTS_DIR.rglob("*"):
        if src_file.is_file():
            rel_path = str(src_file.relative_to(ETC_DOTS_DIR))
            diff_for_file(src_file, rel_path)

    print("--- Complete ---")