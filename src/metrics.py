import os
import time

import psutil


BYTES_PER_GB = 1024 ** 3


def get_cpu_usage():
    try:
        return psutil.cpu_percent()
    except Exception as error:
        print(f"CPU metric error: {error}")
        return None


def get_memory_usage():
    try:
        memory = psutil.virtual_memory()

        return {
            "percent": memory.percent,
            "used_gb": memory.used / BYTES_PER_GB,
            "total_gb": memory.total / BYTES_PER_GB,
        }
    except Exception as error:
        print(f"Memory metric error: {error}")
        return None


def get_disk_usage():
    try:
        system_drive = os.environ.get("SystemDrive", "C:")
        disk = psutil.disk_usage(system_drive + "\\")

        return {
            "percent": disk.percent,
            "used_gb": disk.used / BYTES_PER_GB,
            "total_gb": disk.total / BYTES_PER_GB,
        }
    except Exception as error:
        print(f"Disk metric error: {error}")
        return None


def get_uptime():
    try:
        uptime_seconds = int(time.time() - psutil.boot_time())

        days, remainder = divmod(uptime_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)

        return f"{days}d {hours}h {minutes}m"
    except Exception as error:
        print(f"Uptime metric error: {error}")
        return None


def format_percent(value):
    try:
        return f"{float(value):.1f}%"
    except (TypeError, ValueError):
        return "Unavailable"


def format_gb_usage(data):
    try:
        return f"{data['used_gb']:.1f} GB / {data['total_gb']:.1f} GB"
    except (TypeError, KeyError, ValueError):
        return ""