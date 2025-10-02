import pyudev
import psutil


def list_partitions():
    """List unmounted partitions."""
    partitions = []
    index = 1
    context = pyudev.Context()
    for device in context.list_devices(subsystem="block", DEVTYPE="partition"):
        dev_path = device.device_node
        if not any(dev_path == p.device for p in psutil.disk_partitions()):
            partitions.append(dev_path)
            print(f"{index}) {dev_path}")
            index += 1
    return partitions
