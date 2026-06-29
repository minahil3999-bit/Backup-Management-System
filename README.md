# Backup Management System (GUI)

A modern Backup Management System built using Python and CustomTkinter GUI.
This application allows users to create, restore, and manage backups efficiently with a clean dashboard interface.

## Features
1. Dashboard Overview
Total backups count
Latest backup version
Storage usage
System status (live updates)
2. Create Backup
One-click backup creation
Progress indicator
3. Restore Backup
Restore selected backup from history
4. Backup History
View all backups in table format
Select backups for restore
5. Reports
Total backups
Success vs failed backups
Storage usage
Success rate
6. Select Source Folder
Choose folder to backup
7. Live Dashboard Updates
Auto-refresh statistics
Real-time system time
## Technologies Used
Python
CustomTkinter (Modern GUI)
Tkinter (ttk, messagebox, filedialog)
OS Module
Datetime Module
## How to Run
```bash
Clone the repository

git clone https://github.com/minahil3999-bit/Backup-Management-System
Navigate to project folder

cd BackupManagementSystem

Install required library

pip install customtkinter

Run the program

dashboard.py
```
## Requirements
- Python 3.x
- CustomTkinter installed
## Challenges Faced
- Managing real-time dashboard updates
- Handling GUI responsiveness
- Designing clean layout using CustomTkinter
- Synchronizing backup data with UI
- Implementing treeview selection logic
## Future Improvements
Backup Scheduler
Cloud Backup Support
Encryption for backups
Graphical analytics
## Author
Minahil Noor
