import socket

IP_ADDRESS = "0.0.0.0" #האזנה לכל כרטיסי הרשת

PORT = 514 # syslog port

def start_syslog_server():
    # creating UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.bind((IP_ADDRESS, PORT))
        print(f"🚀 Syslog Server is running on {IP_ADDRESS}:{PORT}...")
        print("Waiting for logs from the devices...\n")

        while True:
            data, addr = sock.recvfrom(4096) # buffer size 4KB

            # message decryption
            message = data.decode('utf-8', errors='ignore')

            print(f"🔔 [FROM {addr[0]}] {message.strip()}")

            if "CONFIG_I" in message:
                print("⚠️  ALERT: Someone just entered Configuration Mode!")
            if "SYS-5-RESTART" in message:
                print("🔥 ALERT: The router just restarted!")

    except PermissionError:
        print("❌ Error: You need Admin/Sudo privileges to listen on port 514.")
    except KeyboardInterrupt:
        print("\nStopping service...")
    finally:
        sock.close()

if __name__ == "__main__":
    start_syslog_server()

