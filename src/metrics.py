import os
import time

import psutil


BYTES_PER_GB = 1024 ** 3


def get_cpu_usage():
    return psutil.cpu_percent()


def get_memory_usage():
    memory = psutil.virtual_memory()

    return {
        "percent": memory.percent,
        "used_gb": memory.used / BYTES_PER_GB,
        "total_gb": memory.total / BYTES_PER_GB,
    }


def get_disk_usage():
    system_drive = os.environ.get("SystemDrive", "C:")
    disk = psutil.disk_usage(system_drive + "\\")

    return {
        "percent": disk.percent,
        "used_gb": disk.used / BYTES_PER_GB,
        "total_gb": disk.total / BYTES_PER_GB,
    }


def get_uptime():
    uptime_seconds = int(time.time() - psutil.boot_time())

    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    return f"{days}d {hours}h {minutes}m"