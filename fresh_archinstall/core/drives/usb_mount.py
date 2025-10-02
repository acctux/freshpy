from pathlib import Path
from sys import exit
import sys
import subprocess
import os
import shutil
import tempfile

from fresh_archinstall.core.drives.list_umounted_partitions import list_partitions

# Global variables
DEVICE = ""
KEYS_MNT = tempfile.mkdtemp(prefix="keys_mnt_")
KEY_DIR = os.path.expanduser("~/.ssh")
KEY_FILES = ["id_rsa", "id_rsa.pub"]


def mount_partition():
    """Mount the selected partition."""
    os.makedirs(KEYS_MNT, exist_ok=True)
    _ = subprocess.run(["sudo", "mount", DEVICE, KEYS_MNT], check=True)


def copy_keys():
    """Copy key files from mounted partition."""
    os.makedirs(KEY_DIR, exist_ok=True)
    src_ssh_dir = os.path.join(KEYS_MNT, ".ssh")
    if not os.path.isdir(src_ssh_dir):
        print(f"No .ssh directory found on {KEYS_MNT}")
        sys.exit(1)
    for key_file in KEY_FILES:
        src = os.path.join(src_ssh_dir, key_file)
        dst = os.path.join(KEY_DIR, key_file)
        if not os.path.isfile(dst) and os.path.isfile(src):
            _ = shutil.copy2(src, dst)


def unmount_partition(KEYS_MNT: Path):
    """Unmount and clean up."""
    if os.path.ismount(KEYS_MNT):
        _ = subprocess.run(["sudo", "umount", KEYS_MNT], check=True)
    try:
        os.rmdir(KEYS_MNT)
    except OSError:
        pass


def main():
    """Main function."""
    try:
        if not keys_exist():
            select_partition()
            if not os.path.isblk(DEVICE):
                print(f"Invalid device: {DEVICE}")
                sys.exit(1)
            mount_partition()
            copy_keys()
            print("Keys copied.")
        else:
            print("Keys already exist. Skipping.")
    finally:
        unmount_partition()


if __name__ == "__main__":
    main()
