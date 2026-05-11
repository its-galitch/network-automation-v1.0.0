# Network Automation Project

This repository contains a set of Python scripts for automating network device management, focusing on Cisco IOS devices using the `netmiko` library.

## Project Structure

- **`backup_network_config.py`**: Connects to devices in the inventory and saves their running configuration to the `network_backups` directory with a timestamp.
- **`deploy_logging_config.py`**: Configures syslog settings on network devices, ensuring they report logs to a centralized syslog server.
- **`router_status.py`**: Connects to a specific router and retrieves the status of its interfaces using SSH.
- **`syslog_listener.py`**: A simple UDP server that listens on port 514 for incoming syslog messages and prints alerts for specific events.
- **`load_devices.py`**: A utility module to load device inventory from a CSV file.
- **`devices.csv`**: The inventory file containing device details (host, username, password, etc.).
- **`requirements.txt`**: List of Python dependencies required for this project.

## Getting Started

### Prerequisites

- Python 3.x installed on your system.

### Setting up a Virtual Environment

It is recommended to use a Python virtual environment to manage dependencies.

#### On Windows:

1. Open PowerShell or Command Prompt in the project directory.
2. Create the virtual environment:
   ```powershell
   python -m venv .venv
   ```
3. Activate the virtual environment:
   ```powershell
   .\.venv\Scripts\activate
   ```

#### On Linux/macOS:

1. Open a terminal in the project directory.
2. Create the virtual environment:
   ```bash
   python3 -m venv .venv
   ```
3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

### Installing Dependencies

Once the virtual environment is activated, install the required libraries:

```bash
pip install -r requirements.txt
```

## Usage

1. Update `devices.csv` with your network device details.
2. Run any of the scripts using Python:
   ```bash
   python backup_network_config.py
   ```
