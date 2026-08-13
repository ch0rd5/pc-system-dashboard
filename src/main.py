import tkinter as tk

from dashboard import Dashboard


def create_app_icon():
    icon = tk.PhotoImage(width=32, height=32)

    # Background
    icon.put("#221C19", to=(0, 0, 32, 32))

    # Four dashboard cards
    icon.put("#2D2521", to=(3, 3, 14, 14))
    icon.put("#2D2521", to=(18, 3, 29, 14))
    icon.put("#2D2521", to=(3, 18, 14, 29))
    icon.put("#2D2521", to=(18, 18, 29, 29))

    # Small status accents
    icon.put("#5F705E", to=(5, 10, 12, 12))
    icon.put("#A5744A", to=(20, 10, 27, 12))
    icon.put("#B56D5C", to=(5, 25, 12, 27))
    icon.put("#F3E7D7", to=(20, 21, 27, 23))

    return icon


def main():
    root = tk.Tk()

    root.title("PC System Dashboard")
    root.geometry("800x520")

    app_icon = create_app_icon()
    root.iconphoto(True, app_icon)

    Dashboard(root)

    root.mainloop()


if __name__ == "__main__":
    main()