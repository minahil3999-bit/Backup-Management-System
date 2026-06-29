from database import get_all_backups


def backup_report():

    backups = get_all_backups()

    if len(backups) == 0:
        print("\nNo backup records found.")
        return

    total_backups = len(backups)

    successful = 0
    failed = 0

    print("\n========== Backup Report ==========\n")

    for backup in backups:

        print(f"""
Backup ID   : {backup[0]}
Date        : {backup[1]}
Source      : {backup[2]}
Destination : {backup[3]}
Size        : {backup[4]}
Status      : {backup[5]}
Version     : {backup[6]}
---------------------------------------
""")

        if backup[5] == "Success":
            successful += 1
        else:
            failed += 1

    print("\n========== Summary ==========")
    print("Total Backups      :", total_backups)
    print("Successful Backup  :", successful)
    print("Failed Backup      :", failed)