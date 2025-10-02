from pathlib import Path
import subprocess
import getpass
import os

from archinstall.default_profiles.minimal import MinimalProfile
from archinstall.lib.disk.device_handler import device_handler
from archinstall.lib.disk.filesystem import FilesystemHandler
from archinstall.lib.installer import Installer
from archinstall.lib.models.device import (
    DeviceModification,
    DiskLayoutConfiguration,
    DiskLayoutType,
    FilesystemType,
    ModificationStatus,
    PartitionType,
    PartitionModification,
    PartitionFlag,
    Size,
    Unit,
)
from archinstall.lib.models.profile import ProfileConfiguration
from archinstall.lib.models.users import Password, User
from archinstall.lib.profile.profiles_handler import profile_handler


def run_chroot(mnt: Path, cmd: list[str]) -> None:
    subprocess.run(["arch-chroot", str(mnt)] + cmd, check=True)


def post_install_setup(mnt: Path, hostname: str, username: str, root_uuid: str):
    # Enable NetworkManager, sshd
    run_chroot(mnt, ["systemctl", "enable", "NetworkManager", "sshd"])

    # Locale
    (mnt / "etc/locale.gen").write_text("en_US.UTF-8 UTF-8\n")
    run_chroot(mnt, ["locale-gen"])
    (mnt / "etc/locale.conf").write_text("LANG=en_US.UTF-8\n")

    # Timezone & clock
    run_chroot(mnt, ["ln", "-sf", "/usr/share/zoneinfo/UTC", "/etc/localtime"])
    run_chroot(mnt, ["hwclock", "--systohc"])

    # Set hostname
    (mnt / "etc/hostname").write_text(hostname + "\n")
    hosts = f"127.0.0.1\tlocalhost\n::1\tlocalhost\n127.0.1.1\t{hostname}.localdomain {hostname}\n"
    (mnt / "etc/hosts").write_text(hosts)

    # Configure mkinitcpio for BTRFS (no encrypt)
    run_chroot(
        mnt,
        [
            "sed",
            "-i",
            r"s/^HOOKS=.*/HOOKS=(base systemd autodetect keyboard sd-vconsole modconf block filesystems btrfs fsck)/",
            "/etc/mkinitcpio.conf",
        ],
    )
    run_chroot(mnt, ["mkinitcpio", "-P"])

    # Install systemd-boot in EFI
    run_chroot(mnt, ["bootctl", "install"])

    # Write loader config
    loader_conf = """default arch
timeout 3
console-mode max
editor no
"""
    (mnt / "boot/loader/loader.conf").write_text(loader_conf)

    entry = f"""title Arch Linux
linux /vmlinuz-linux
initrd /initramfs-linux.img
options root=UUID={root_uuid} rw subvol=@
"""
    (mnt / "boot/loader/entries/arch.conf").write_text(entry)

    # fstab
    fstab = f"""UUID={root_uuid} / btrfs rw,relatime,compress=zstd,subvol=@ 0 1
UUID={root_uuid} /home btrfs rw,relatime,compress=zstd,subvol=@home 0 2
UUID={root_uuid} /.snapshots btrfs rw,relatime,compress=zstd,subvol=@snapshots 0 2
"""
    (mnt / "etc/fstab").write_text(fstab)


def main():
    user_password = getpass.getpass("User password: ")
    hostname = "arch-test"
    username = "archuser"
    mountpoint = Path("/mnt")

    # Prepare device
    dev = device_handler.get_device(Path("/dev/sda"))
    if dev is None:
        raise RuntimeError("No /dev/sda device found")

    dm = DeviceModification(dev, wipe=True)

    # EFI partition
    dm.add_partition(
        PartitionModification(
            status=ModificationStatus.Create,
            type=PartitionType.Primary,
            start=Size(1, Unit.MiB, dev.device_info.sector_size),
            length=Size(512, Unit.MiB, dev.device_info.sector_size),
            mountpoint=Path("/boot"),
            fs_type=FilesystemType.Fat32,
            flags=[PartitionFlag.BOOT],
        )
    )

    # Root BTRFS partition (remaining space)
    rootp = PartitionModification(
        status=ModificationStatus.Create,
        type=PartitionType.Primary,
        start=Size(513, Unit.MiB, dev.device_info.sector_size),
        length=Size(-1, Unit.MiB, dev.device_info.sector_size),
        mountpoint=None,
        fs_type=FilesystemType.Btrfs,
    )
    dm.add_partition(rootp)

    layout = DiskLayoutConfiguration(
        config_type=DiskLayoutType.Default, device_modifications=[dm]
    )

    fs = FilesystemHandler(layout)
    fs.perform_filesystem_operations(show_countdown=False)

    # Create subvolumes
    # ArchInstall’s built-in default BTRFS layout (2024/25) includes @, @home, @log, @pkg, @.snapshots :contentReference[oaicite:0]{index=0}
    # But we’ll only do a simpler set: @, @home, @snapshots
    # We must mount the root partition to /mnt first:
    subprocess.run(
        ["mount", "-o", "compress=zstd", "/dev/sda2", str(mountpoint)], check=True
    )
    for sv in ["@", "home", "snapshots"]:
        subprocess.run(
            ["btrfs", "subvolume", "create", str(mountpoint / sv)], check=True
        )
    subprocess.run(["umount", str(mountpoint)], check=True)

    with Installer(mountpoint, layout, kernels=["linux"]) as inst:
        # Mount subvolumes
        inst.add_mount(
            PartitionModification(
                mountpoint=Path("/"),
                fs_type=FilesystemType.Btrfs,
                mount_options=["subvol=@", "compress=zstd"],
            )
        )
        inst.add_mount(
            PartitionModification(
                mountpoint=Path("/home"),
                fs_type=FilesystemType.Btrfs,
                mount_options=["subvol=home", "compress=zstd"],
            )
        )
        inst.add_mount(
            PartitionModification(
                mountpoint=Path("/.snapshots"),
                fs_type=FilesystemType.Btrfs,
                mount_options=["subvol=snapshots", "compress=zstd"],
            )
        )

        # Also mount /boot
        inst.add_mount(
            PartitionModification(
                mountpoint=Path("/boot"), fs_type=FilesystemType.Fat32
            )
        )

        inst.mount_ordered_layout()
        inst.minimal_installation(hostname=hostname)

        inst.add_additional_packages(
            ["networkmanager", "openssh", "btrfs-progs", "efibootmgr"]
        )

        profile_handler.install_profile_config(
            inst, ProfileConfiguration(MinimalProfile())
        )

        user = User(username, Password(plaintext=user_password), True)
        inst.create_users(user)

        # Get root partition UUID
        res = subprocess.run(
            ["blkid", "-s", "UUID", "-o", "value", "/dev/sda2"],
            capture_output=True,
            text=True,
        )
        root_uuid = res.stdout.strip()

        post_install_setup(mountpoint, hostname, username, root_uuid)

    print("Installation done. Exit and reboot.")


if __name__ == "__main__":
    main()
