import tkinter as tk

from dashboard import Dashboard


def main():
    root = tk.Tk()
    root.title("PC System Dashboard")
    root.geometry("800x500")

    Dashboard(root)

    root.mainloop()


if __name__ == "__main__":
    main()