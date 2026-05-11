from netmiko import ConnectHandler
import json

# הגדרת פרטי המכשיר
cisco_router = {
    'device_type': 'cisco_ios',
    'host': '192.168.197.130',
    'username': 'admin',
    'password': 'P@ssw0rd123',
    'port': 22,
}


def get_router_status():
    try:
        print(f"--- Connecting to {cisco_router['host']} ---")

        # יצירת חיבור SSH
        with ConnectHandler(**cisco_router) as net_connect:
            # הרצת הפקודה
            interfaces_output = net_connect.send_command("show ip interface brief", use_textfsm=True)

            print(json.dumps(interfaces_output, indent=4))

            print("\n --- Logic Analysis ---")
            for line in interfaces_output:
                print(line)
                if line['status'] != 'up':
                    print(f"⚠️ Warning: Interface {line['interface']} is DOWN")
                else:
                    print('STATUS IS UP')
                    print(f"✅ Interface {line['interface']} is UP")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    get_router_status()