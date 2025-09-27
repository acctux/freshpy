from src.patch_creator import create_patches


def main():
    create_patches()


if __name__ == "__main__":
    main()

    # """Main execution function to load the config, loop through, and apply patches."""
    # if os.geteuid() != 0:
    #     print("\n[CRITICAL] This script must be run with root privileges (sudo).\n")
    #     exit(1)
    # else:
    # create_patch_list
    # ensure_file_ready
    # process_patches
