# PC System Dashboard

A lightweight Windows desktop utility for monitoring live CPU, memory, disk, and system uptime metrics.

![PC System Dashboard](assets/screenshot.png)

## Features

- Live CPU utilization
- Live memory utilization and capacity
- Primary Windows system-drive usage
- System uptime
- Automatic one-second refresh
- Graceful fallback when a metric cannot be read
- Warm dark-walnut desktop interface
- Packaged Windows executable

## Why I Built It

PC System Dashboard was my first project focused on completing the entire engineering workflow rather than only writing code.

The goal was to practice taking a small idea from initial requirements through implementation, debugging, reliability testing, UI polish, packaging, documentation, and final release.

## Tech Stack

- Python 3
- Tkinter
- psutil
- PyInstaller
- Git / GitHub

## Running From Source

### Requirements

- Windows
- Python 3
- Git

Clone the repository:

```bash
git clone https://github.com/ch0rd5/pc-system-dashboard.git
cd pc-system-dashboard