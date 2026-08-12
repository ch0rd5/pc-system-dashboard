import tkinter as tk
from tkinter import ttk

from metrics import (
    get_cpu_usage,
    get_memory_usage,
    get_disk_usage,
    get_uptime,
)


class Dashboard:
    def __init__(self, root):
        self.root = root

        self.frame = ttk.Frame(root, padding=20)
        self.frame.pack(fill="both", expand=True)

        self.cpu_value, self.cpu_detail = self.create_card("CPU Usage", 0, 0)
        self.ram_value, self.ram_detail = self.create_card("Memory Usage", 0, 1)
        self.disk_value, self.disk_detail = self.create_card("Disk Usage", 1, 0)
        self.uptime_value, self.uptime_detail = self.create_card("System Uptime", 1, 1)

        self.update_metrics()

    def create_card(self, title, row, column):
        card = ttk.LabelFrame(self.frame, text=title, padding=20)
        card.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        value_label = ttk.Label(card, text="Loading...", font=("Arial", 20))
        value_label.pack(expand=True)

        detail_label = ttk.Label(card, text="", font=("Arial", 10))
        detail_label.pack()

        self.frame.rowconfigure(row, weight=1)
        self.frame.columnconfigure(column, weight=1)

        return value_label, detail_label

    def update_metrics(self):
        memory = get_memory_usage()
        disk = get_disk_usage()

        self.cpu_value.config(text=f"{get_cpu_usage()}%")

        self.ram_value.config(text=f"{memory['percent']}%")
        self.ram_detail.config(
            text=f"{memory['used_gb']:.1f} GB / {memory['total_gb']:.1f} GB"
        )

        self.disk_value.config(text=f"{disk['percent']}%")
        self.disk_detail.config(
            text=f"{disk['used_gb']:.1f} GB / {disk['total_gb']:.1f} GB"
        )

        self.uptime_value.config(text=get_uptime())

        self.root.after(1000, self.update_metrics)