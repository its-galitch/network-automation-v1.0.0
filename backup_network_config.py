from netmiko import ConnectHandler
from datetime import datetime
import os

from load_devices import load_inventory_from_csv


def backup_network_configs(device_list):
    # יצירת תיקיית גיבוי אם היא לא קיימת
    if not os.path.exists('network_backups'):
        os.makedirs('network_backups')

    now = datetime.now().strftime("%Y-%m-%d_%H-%M")

    print(f"Starting backup for {len(device_list)} devices...\n")

    for device in device_list:
        label = device.pop('label')  # מוציאים את התווית כדי שלא תפריע ל-Netmiko
        dev_id = device.pop('id')
        try:
            print(f"[{dev_id}] 📡 Connecting to {label} ({device['host']})...")

            with ConnectHandler(**device) as net_connect:
                # הרצת הפקודה לשליפת ההגדרות
                config_data = net_connect.send_command("show running-config")

                # שמירה לקובץ
                filename = f"network_backups/{label}_{now}.txt"
                with open(filename, 'w') as f:
                    f.write(config_data)

            print(f"✅ Backup saved to {filename}")

        except Exception as e:
            print(f"❌ Failed to backup {label}: {e}")


if __name__ == "__main__":
    devices = load_inventory_from_csv("devices.csv")
    backup_network_configs(devices)