from netmiko import ConnectHandler
from load_devices import load_inventory_from_csv



SYSLOG_SERVER_IP = "192.168.197.1"

def deploy_logging_config(device_list):
    config_commands = [
        "service timestamps log datetime msec",  # הוספת תאריך וזמן מדויק
        "logging on",  # הפעלת מערכת הלוגים
        f"logging host {SYSLOG_SERVER_IP}",  # הגדרת היעד לשליחה
        "logging trap informational",  # רמת פירוט שתתפוס כניסות
        "login on-failure log",  # לוג על כישלון כניסה
        "login on-success log",  # לוג על הצלחה בכניסה
        "login block-for 60 attempts 3 within 30"
    ]

    for device in device_list:
        label = device.pop('label')  # מוציאים את התווית כדי שלא תפריע ל-Netmiko
        dev_id = device.pop('id')

        try:
            print(f"[{dev_id}] 📡 Connecting to {label} ({device['host']})...")
            with ConnectHandler(**device) as net_connect:
                print(f"Configuring {device['host']}...")
                version_info = net_connect.send_command("show version | include iores")
                if not version_info:  # אם זו גרסה אחרת
                    version_info = net_connect.send_command("show version | include Software")

                print(f"📊 Device Info from {device['host']}:")
                print(version_info.strip())


                output = net_connect.send_config_set(config_commands)
                print(output)

                command_response = net_connect.send_command("write memory", use_textfsm=True)
                print(command_response)
                print(f"✅ Success! {device['host']} is now reporting to the listener.")

        except Exception as e:
            print(f"❌ Failed to configure {device['host']}: {e}")

if __name__ == "__main__":
    devices = load_inventory_from_csv("devices.csv")
    deploy_logging_config(devices)