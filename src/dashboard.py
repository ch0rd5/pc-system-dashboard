from datetime import datetime
import tkinter as tk
from tkinter import ttk

from metrics import (
    format_percent,
    format_gb_usage,
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

        self.last_updated = ttk.Label(self.frame, text="Last updated: --")
        self.last_updated.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=(5, 0),
        )

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
        cpu = get_cpu_usage()
        memory = get_memory_usage()
        disk = get_disk_usage()
        uptime = get_uptime()

        self.cpu_value.config(text=format_percent(cpu))

        self.ram_value.config(
            text=format_percent(memory["percent"] if memory else None)
        )
        self.ram_detail.config(text=format_gb_usage(memory))

        self.disk_value.config(
            text=format_percent(disk["percent"] if disk else None)
        )
        self.disk_detail.config(text=format_gb_usage(disk))

        if uptime is not None:
            self.uptime_value.config(text=uptime)
        else:
            self.uptime_value.config(text="Unavailable")

        self.last_updated.config(
            text=f"Last updated: {datetime.now().strftime('%I:%M:%S %p')}"
        )

        self.root.after(1000, self.update_metrics)