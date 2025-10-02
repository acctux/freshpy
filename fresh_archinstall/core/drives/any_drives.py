3. Hard Drive and Filesystem Interaction
These libraries help manage disks, partitions, and filesystems.

psutil:

Purpose: Monitor system resources, including disk usage, partitions, and I/O statistics.
Installation:
bashsudo pacman -S python-psutil

Example Usage:
pythonimport psutil
for disk in psutil.disk_partitions():
    print(f"Device: {disk.device}, Mount: {disk.mountpoint}, Usage: {psutil.disk_usage(disk.mountpoint).percent}%")



pyudev:

Purpose: Interact with udev for device management (e.g., detecting hard drives, USBs, or other hardware).
Installation:
    sudo pacman -S python-pyudev

Example Usage:
pythonimport pyudev
context = pyudev.Context()
for device in context.list_devices(subsystem='block'):
    print(device.get('DEVNAME'), device.get('ID_MODEL'))
This lists block devices (e.g., hard drives) and their models.
