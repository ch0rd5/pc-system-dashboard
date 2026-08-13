from datetime import datetime
import tkinter as tk

from metrics import (
    format_percent,
    format_gb_usage,
    get_cpu_usage,
    get_memory_usage,
    get_disk_usage,
    get_uptime,
)


# Walnut café color palette
BACKGROUND = "#221C19"
CARD_BACKGROUND = "#2D2521"
CARD_BORDER = "#4A3D36"

PRIMARY_TEXT = "#F3E7D7"
SECONDARY_TEXT = "#C9B8A4"

ACCENT = "#A5744A"
HEALTHY = "#5F705E"
WARNING = "#B56D5C"

PROGRESS_TRACK = "#3A302B"


def get_status_color(value):
    if value is None:
        return CARD_BORDER

    if value >= 90:
        return WARNING

    if value <= 40:
        return HEALTHY

    return ACCENT


class RoundedCard(tk.Canvas):
    def __init__(self, parent):
        super().__init__(
            parent,
            bg=BACKGROUND,
            highlightthickness=0,
            borderwidth=0,
        )

        self.content = tk.Frame(
            self,
            bg=CARD_BACKGROUND,
        )

        self.content.place(
            x=22,
            y=20,
            relwidth=1,
            width=-44,
            relheight=1,
            height=-40,
        )

        self.bind("<Configure>", self.redraw)

    def draw_rounded_rectangle(
        self,
        x1,
        y1,
        x2,
        y2,
        radius,
        color,
    ):
        radius = min(
            radius,
            (x2 - x1) / 2,
            (y2 - y1) / 2,
        )

        self.create_rectangle(
            x1 + radius,
            y1,
            x2 - radius,
            y2,
            fill=color,
            outline=color,
        )

        self.create_rectangle(
            x1,
            y1 + radius,
            x2,
            y2 - radius,
            fill=color,
            outline=color,
        )

        self.create_arc(
            x1,
            y1,
            x1 + radius * 2,
            y1 + radius * 2,
            start=90,
            extent=90,
            fill=color,
            outline=color,
        )

        self.create_arc(
            x2 - radius * 2,
            y1,
            x2,
            y1 + radius * 2,
            start=0,
            extent=90,
            fill=color,
            outline=color,
        )

        self.create_arc(
            x2 - radius * 2,
            y2 - radius * 2,
            x2,
            y2,
            start=270,
            extent=90,
            fill=color,
            outline=color,
        )

        self.create_arc(
            x1,
            y2 - radius * 2,
            x1 + radius * 2,
            y2,
            start=180,
            extent=90,
            fill=color,
            outline=color,
        )

    def redraw(self, event=None):
        self.delete("all")

        width = self.winfo_width()
        height = self.winfo_height()

        if width < 4 or height < 4:
            return

        self.draw_rounded_rectangle(
            0,
            0,
            width,
            height,
            13,
            CARD_BORDER,
        )

        self.draw_rounded_rectangle(
            1,
            1,
            width - 1,
            height - 1,
            12,
            CARD_BACKGROUND,
        )


class MetricProgressBar(tk.Canvas):
    def __init__(self, parent):
        super().__init__(
            parent,
            height=8,
            bg=CARD_BACKGROUND,
            highlightthickness=0,
            borderwidth=0,
        )

        self.value = 0
        self.bar_color = ACCENT

        self.bind("<Configure>", self.redraw)

    def set(self, value):
        if value is None:
            self.value = 0
            self.bar_color = CARD_BORDER
        else:
            self.value = max(0, min(float(value), 100))
            self.bar_color = get_status_color(self.value)

        self.redraw()

    def redraw(self, event=None):
        self.delete("all")

        width = self.winfo_width()

        if width <= 6:
            return

        center_y = 4

        self.create_line(
            4,
            center_y,
            width - 4,
            center_y,
            fill=PROGRESS_TRACK,
            width=6,
            capstyle=tk.ROUND,
        )

        if self.value <= 0:
            return

        usable_width = width - 8
        fill_width = usable_width * (self.value / 100)

        self.create_line(
            4,
            center_y,
            4 + fill_width,
            center_y,
            fill=self.bar_color,
            width=6,
            capstyle=tk.ROUND,
        )


class Dashboard:
    def __init__(self, root):
        self.root = root

        self.root.configure(bg=BACKGROUND)
        self.root.minsize(700, 520)
        self.frame = tk.Frame(
            root,
            bg=BACKGROUND,
            padx=24,
            pady=24,
        )
        self.frame.pack(fill="both", expand=True)

        self.frame.columnconfigure(0, weight=1, uniform="cards")
        self.frame.columnconfigure(1, weight=1, uniform="cards")
        self.frame.rowconfigure(0, weight=1, uniform="cards")
        self.frame.rowconfigure(1, weight=1, uniform="cards")

        (
            self.cpu_value,
            self.cpu_detail,
            self.cpu_progress,
        ) = self.create_card(
            "CPU Usage",
            0,
            0,
            show_progress=True,
        )

        (
            self.ram_value,
            self.ram_detail,
            self.ram_progress,
        ) = self.create_card(
            "Memory Usage",
            0,
            1,
            show_progress=True,
        )

        (
            self.disk_value,
            self.disk_detail,
            self.disk_progress,
        ) = self.create_card(
            "Disk Usage",
            1,
            0,
            show_progress=True,
        )

        (
            self.uptime_value,
            self.uptime_detail,
            _,
        ) = self.create_card(
            "System Uptime",
            1,
            1,
            show_progress=False,
        )

        self.last_updated = tk.Label(
            self.frame,
            text="Updated --",
            bg=BACKGROUND,
            fg=SECONDARY_TEXT,
            font=("Segoe UI", 9),
        )

        self.last_updated.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=(12, 0),
        )

        self.update_metrics()

    def create_card(
        self,
        title,
        row,
        column,
        show_progress,
    ):
        card = RoundedCard(self.frame)

        card.grid(
            row=row,
            column=column,
            padx=10,
            pady=10,
            sticky="nsew",
        )

        title_label = tk.Label(
            card.content,
            text=title,
            bg=CARD_BACKGROUND,
            fg=SECONDARY_TEXT,
            font=("Segoe UI", 10, "bold"),
            anchor="w",
        )
        title_label.pack(
            fill="x",
            anchor="w",
        )

        value_label = tk.Label(
            card.content,
            text="--",
            bg=CARD_BACKGROUND,
            fg=PRIMARY_TEXT,
            font=("Segoe UI", 30, "bold"),
            anchor="w",
        )
        value_label.pack(
            fill="x",
            anchor="w",
            pady=(12, 2),
        )

        detail_label = tk.Label(
            card.content,
            text="",
            bg=CARD_BACKGROUND,
            fg=SECONDARY_TEXT,
            font=("Segoe UI", 10),
            anchor="w",
        )
        detail_label.pack(
            fill="x",
            anchor="w",
        )

        progress_bar = None

        if show_progress:
            progress_bar = MetricProgressBar(card.content)
            progress_bar.pack(
                fill="x",
                pady=(18, 0),
            )

        return (
            value_label,
            detail_label,
            progress_bar,
        )

    def update_metrics(self):
        cpu = get_cpu_usage()
        memory = get_memory_usage()
        disk = get_disk_usage()
        uptime = get_uptime()

        self.cpu_value.config(
            text=format_percent(cpu)
        )
        self.cpu_progress.set(cpu)

        memory_percent = (
            memory["percent"]
            if memory
            else None
        )

        self.ram_value.config(
            text=format_percent(memory_percent)
        )
        self.ram_detail.config(
            text=format_gb_usage(memory)
        )
        self.ram_progress.set(memory_percent)

        disk_percent = (
            disk["percent"]
            if disk
            else None
        )

        self.disk_value.config(
            text=format_percent(disk_percent)
        )
        self.disk_detail.config(
            text=format_gb_usage(disk)
        )
        self.disk_progress.set(disk_percent)

        if uptime is not None:
            self.uptime_value.config(text=uptime)
        else:
            self.uptime_value.config(text="Unavailable")

        current_time = datetime.now().strftime(
            "%I:%M %p"
        ).lstrip("0")

        self.last_updated.config(
            text=f"Updated {current_time}"
        )

        self.root.after(
            1000,
            self.update_metrics,
        )