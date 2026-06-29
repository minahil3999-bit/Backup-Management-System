import customtkinter as ctk
import os
from tkinter import messagebox, filedialog
from tkinter import ttk
from datetime import datetime
from backup import create_backup
from restore import restore_backup
from report import backup_report
from database import get_all_backups
from config import BACKUP_FOLDER
selected_backup = None
def create_backup_gui():

    try:

        progress.set(0.2)
        app.update()
        create_backup()
        progress.set(1)
        update_dashboard()
        messagebox.showinfo(
            "Success",
            "Backup created successfully!"
        )
        progress.set(0)
    except Exception as e:
        progress.set(0)
        messagebox.showerror(
            "Error",
            str(e)
        )

def restore_backup_gui():
    global selected_backup

    try:

        if selected_backup is None:
            messagebox.showwarning(
                "Warning",
                "Please select a backup from Backup History first."
            )
            return

        backup_path = selected_backup[3]
        answer = messagebox.askyesno(
            "Restore Backup",
            "Do you want to restore the selected backup?"
        )

        if not answer:
            return
        restore_backup(
            backup_path,
            "restored_files"
        )

        messagebox.showinfo(
            "Success",
            "Backup restored successfully!"
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )

def report_gui():

    report_window = ctk.CTkToplevel(app)
    report_window.title("Backup Report")
    report_window.geometry("1000x650")

    backups = get_all_backups()

    total = len(backups)

    success = 0
    failed = 0
    latest_version = 0
    total_size = 0

    for backup in backups:

        if backup[5].lower() == "success":
            success += 1
        else:
            failed += 1

        if backup[6] > latest_version:
            latest_version = backup[6]

        try:
            total_size += float(backup[4].replace(" MB", ""))
        except:
            pass

    # ===========================
    # Summary
    # ===========================

    summary = ctk.CTkFrame(report_window)
    summary.pack(fill="x", padx=20, pady=20)

    ctk.CTkLabel(
        summary,
        text="BACKUP REPORT",
        font=("Arial",24,"bold")
    ).pack(pady=10)

    info = f"""
Total Backups       : {total}
Successful Backups  : {success}
Failed Backups      : {failed}
Latest Version      : V{latest_version}
Total Storage Used  : {round(total_size,2)} MB
"""

    ctk.CTkLabel(
        summary,
        text=info,
        justify="left",
        font=("Arial",16)
    ).pack(anchor="w", padx=20)

    # ===========================
    # Table
    # ===========================

    tree = ttk.Treeview(
        report_window,
        columns=("ID","Date","Version","Size","Status"),
        show="headings"
    )

    tree.heading("ID",text="ID")
    tree.heading("Date",text="Date")
    tree.heading("Version",text="Version")
    tree.heading("Size",text="Size")
    tree.heading("Status",text="Status")

    tree.column("ID",width=70)
    tree.column("Date",width=220)
    tree.column("Version",width=100)
    tree.column("Size",width=120)
    tree.column("Status",width=120)

    tree.pack(fill="both",expand=True,padx=20,pady=15)

    for backup in backups:

        tree.insert(
            "",
            "end",
            values=(
                backup[0],
                backup[1],
                backup[6],
                backup[4],
                backup[5]
            )
        )

    # ===========================
    # Footer
    # ===========================

    success_rate = 0

    if total != 0:
        success_rate = (success/total)*100

    footer = ctk.CTkLabel(
        report_window,
        text=f"Success Rate : {success_rate:.1f}%        Total Versions : {latest_version}",
        font=("Arial",16,"bold")
    )

    footer.pack(pady=10)

def exit_app():
    app.destroy()
#make it live
def update_dashboard():

    backups = get_all_backups()

    total = len(backups)

    total_label.configure(text=str(total))

    if total == 0:
        version_label.configure(text="V0")
        storage_label.configure(text="0 MB")
    else:

        version_label.configure(text=f"V{backups[-1][6]}")

        total_storage = 0

        for backup in backups:

            size = backup[4]

            try:
                total_storage += float(size.replace(" MB", ""))

            except:
                pass

        storage_label.configure(
            text=f"{round(total_storage,2)} MB"
        )

    status_label.configure(text="Ready")

    current_time = datetime.now().strftime("%d-%m-%Y   %I:%M:%S %p")

    time_label.configure(text=current_time)

    app.after(1000, update_dashboard)
# Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def history_gui():

    history_window = ctk.CTkToplevel(app)

    history_window.title("Backup History")

    history_window.geometry("900x500")

    tree = ttk.Treeview(
        history_window,
        columns=("ID", "Date", "Source", "Destination", "Size", "Status", "Version"),
        show="headings"
    )

    tree.heading("ID", text="ID")
    tree.heading("Date", text="Date")
    tree.heading("Source", text="Source")
    tree.heading("Destination", text="Destination")
    tree.heading("Size", text="Size")
    tree.heading("Status", text="Status")
    tree.heading("Version", text="Version")

    tree.column("ID", width=60)
    tree.column("Date", width=150)
    tree.column("Source", width=150)
    tree.column("Destination", width=180)
    tree.column("Size", width=80)
    tree.column("Status", width=80)
    tree.column("Version", width=80)

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def select_backup(event):
        global selected_backup

        item = tree.focus()

        if item:
            values = tree.item(item, "values")
            selected_backup = values

    tree.bind("<<TreeviewSelect>>", select_backup)

    backups = get_all_backups()

    # Insert backup records into the table
    for backup in backups:
        tree.insert("", "end", values=backup)


def choose_source_folder():

    folder = filedialog.askdirectory(
        title="Select Source Folder"
    )

    if folder:
        messagebox.showinfo(
            "Selected Folder",
            folder
        )
# -----------------------------
# Main Window
# -----------------------------
app = ctk.CTk()
app.title("Backup Management System")
app.geometry("1200x700")
app.resizable(False, False)

# =============================
# Left Sidebar
# =============================
sidebar = ctk.CTkFrame(app, width=220, corner_radius=0)
sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(
    sidebar,
    text="Backup\nManagement",
    font=("Arial", 24, "bold")
)
logo.pack(pady=30)

dashboard_btn = ctk.CTkButton(sidebar, text="Dashboard")
dashboard_btn.pack(pady=8)

backup_btn = ctk.CTkButton(
    sidebar,
    text="Create Backup",
    command=create_backup_gui
)
backup_btn.pack(pady=8)
source_btn = ctk.CTkButton(
    sidebar,
    text="Select Source",
    command=choose_source_folder
)

source_btn.pack(pady=8)
restore_btn = ctk.CTkButton(
    sidebar,
    text="Restore Backup",
    command=restore_backup_gui
)
restore_btn.pack(pady=8)

history_btn = ctk.CTkButton(
    sidebar,
    text="Backup History",
    command=history_gui
)
history_btn.pack(pady=8)

report_btn = ctk.CTkButton(
    sidebar,
    text="Reports",
    command=report_gui
)
report_btn.pack(pady=8)

scheduler_btn = ctk.CTkButton(
    sidebar,
    text="Scheduler"
)
scheduler_btn.pack(pady=8)

exit_btn = ctk.CTkButton(
    sidebar,
    text="Exit",
    command=exit_app
)
exit_btn.pack(pady=8)

# =============================
# Main Area
# =============================
main = ctk.CTkFrame(app)
main.pack(fill="both", expand=True, padx=20, pady=20)

title = ctk.CTkLabel(
    main,
    text="Backup Management Dashboard",
    font=("Arial", 30, "bold")
)
title.pack(pady=20)

subtitle = ctk.CTkLabel(
    main,
    text="Monitor and Manage Your Backups",
    font=("Arial", 18)
)
subtitle.pack()
time_label = ctk.CTkLabel(
    main,
    text="",
    font=("Arial", 16)
)

time_label.pack(pady=5)
# =============================
# Statistics Cards
# =============================
cards = ctk.CTkFrame(main, fg_color="transparent")
cards.pack(pady=30)

card1 = ctk.CTkFrame(cards, width=220, height=120)
card1.grid(row=0, column=0, padx=15)

ctk.CTkLabel(
    card1,
    text="Total Backups",
    font=("Arial",18)
).pack(pady=10)

total_label = ctk.CTkLabel(
    card1,
    text="0",
    font=("Arial",36,"bold")
)
total_label.pack()

card2 = ctk.CTkFrame(cards, width=220, height=120)
card2.grid(row=0, column=1, padx=15)

ctk.CTkLabel(
    card2,
    text="Latest Version",
    font=("Arial",18)
).pack(pady=10)

version_label = ctk.CTkLabel(
    card2,
    text="V0",
    font=("Arial",36,"bold")
)

version_label.pack()

card3 = ctk.CTkFrame(cards, width=220, height=120)
card3.grid(row=0, column=2, padx=15)

ctk.CTkLabel(
    card3,
    text="Status",
    font=("Arial",18)
).pack(pady=10)

status_label = ctk.CTkLabel(
    card3,
    text="Ready",
    font=("Arial",30,"bold")
)
status_label.pack()
card4 = ctk.CTkFrame(cards, width=220, height=120)
card4.grid(row=0, column=3, padx=15)

ctk.CTkLabel(
    card4,
    text="Storage Used",
    font=("Arial", 18)
).pack(pady=10)

storage_label = ctk.CTkLabel(
    card4,
    text="0 MB",
    font=("Arial", 30, "bold")
)

storage_label.pack()

# =============================
# Bottom Status
# =============================
status = ctk.CTkLabel(
    main,
    text="System Ready",
    font=("Arial",16)
)
status.pack(side="bottom", pady=15)
progress = ctk.CTkProgressBar(main, width=500)

progress.pack(pady=10)

progress.set(0)
update_dashboard()
app.mainloop()