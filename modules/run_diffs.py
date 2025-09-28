import subprocess
from pathlib import Path

DIFFS_DIR = Path("~/dotcetera").expanduser()
ETC_DOTS_DIR = Path("~/Lit/dotfiles/etc").expanduser()


def run_diff(etc_file: Path, patch_file: Path) -> subprocess.CompletedProcess[str]:
    """Helper to run the 'diff -u' command."""
    if not etc_file.exists():
        raise FileNotFoundError(f"System file {etc_file} does not exist")
    if not patch_file.exists():
        raise FileNotFoundError(f"Reference file {patch_file} does not exist")
    return subprocess.run(
        ["diff", "-u", str(etc_file), str(patch_file)],
        capture_output=True,
        text=True,
        check=False,
    )


def diff_for_file(etc_file: Path, dotfile: Path, patch_file: Path) -> Path | None:
    """Compare a system file with a dotfile and create a patch if they differ."""
    try:
        result = run_diff(etc_file, dotfile)
        if result.returncode == 0:
            print(f"✅ No changes for {etc_file} (compared to {dotfile})")
            patch_file.unlink(missing_ok=True)
            return None
        elif result.returncode == 1:
            print(f"📄 Patch created for {etc_file} (compared to {dotfile})")
            patch_file.parent.mkdir(parents=True, exist_ok=True)
            _ = patch_file.write_text(result.stdout)
            return patch_file
        else:
            print(
                f"❌ Error during diff for {etc_file} (Code {result.returncode}). Stderr: {result.stderr.strip()}"
            )
            patch_file.unlink(missing_ok=True)
            return None
    except Exception as e:
        print(f"❌ Fatal error for {etc_file}: {type(e).__name__} - {e}")
        return None


def fresh_diffs(etc_file_locations: list[Path]) -> list[Path]:
    """Generate diff patches for a list of system files compared to dotfiles."""
    ETC_ROOT = Path("/etc")
    diff_file_paths: list[Path] = []

    for rel_path in etc_file_locations:
        etc_file = ETC_ROOT / rel_path  # System file, e.g., /etc/sshd_config
        dotfile = (
            ETC_DOTS_DIR / rel_path
        )  # Reference file, e.g., ~/Lit/dotfiles/etc/sshd_config
        patch_file = (
            DIFFS_DIR / f"{rel_path.name}.patch"
        )  # Patch file, e.g., ~/dotcetera/sshd_config.patch

        result = diff_for_file(etc_file, dotfile, patch_file)
        if result:
            diff_file_paths.append(result)

    return diff_file_paths
