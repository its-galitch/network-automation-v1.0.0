import os
from datetime import datetime

from netmiko import ConnectHandler
from tabulate import tabulate  # להצגת טבלה מעוצבת

from load_devices import load_inventory_from_csv


def get_health_stats(net_connect):
    """שליפת נתוני בריאות מהמכשיר"""
    stats = {'cpu': 'N/A', 'down_intfs': 0}

    # 1. בדיקת CPU - שליפת השורה הראשונה של הפלט
    cpu_output = net_connect.send_command("show processes cpu sorted | include five seconds")
    if cpu_output:
        # חילוץ האחוז (למשל: "CPU utilization for five seconds: 5%/0%")
        stats['cpu'] = cpu_output.split(":")[1].split(";")[0].strip()

    # 2. בדיקת ממשקים תקולים (באמצעות Parsing אוטומטי)
    interfaces = net_connect.send_command("show ip interface brief", use_textfsm=True)
    if isinstance(interfaces, list):
        down_list = [i['interface'] for i in interfaces if i['status'] != 'up']
        stats['down_intfs'] = len(down_list)

    return stats


def run_network_audit():
    devices = load_inventory_from_csv('devices.csv')
    report_data = []  # רשימה שתאכסן את שורות הדוח

    if not os.path.exists('network_backups'):
        os.makedirs('network_backups')

    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"🚀 Starting Network Audit & Backup at {timestamp}...\n")

    for dev in devices:
        dev_id = dev.pop('id')
        label = dev.pop('label')
        status = "✅ Success"
        health = {'cpu': 'N/A', 'down_intfs': 'N/A'}

        try:
            with ConnectHandler(**dev) as net_connect:
                # ביצוע גיבוי
                config = net_connect.send_command("show running-config")
                with open(f"network_backups/{label}_backup.txt", 'w') as f:
                    f.write(config)

                # ביצוע בדיקת בריאות
                health = get_health_stats(net_connect)

        except Exception as e:
            status = f"❌ Failed"

        # הוספת נתונים לשורת הדוח
        report_data.append([
            dev_id,
            label,
            dev['host'],
            status,
            health['cpu'],
            health['down_intfs']
        ])

    # הדפסת הדוח הסופי בטבלה
    headers = ["ID", "Device Name", "IP Address", "Backup Status", "CPU Load", "Down Interfaces"]
    print("\n" + "=" * 80)
    print("                      NETWORK HEALTH & BACKUP REPORT")
    print("=" * 80)
    print(tabulate(report_data, headers=headers, tablefmt="grid"))
    print("=" * 80)


if __name__ == "__main__":
    run_network_audit()