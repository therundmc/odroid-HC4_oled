# Odroid-HC4 OLED Display System Info Script

This repository contains a Python script for displaying system information on an OLED display connected to an Odroid HC4 single-board computer.

## Prerequisites

Before using this script, you will need to install the necessary dependencies on your Odroid HC4. These can be found in the following wiki page:

https://wiki.odroid.com/odroid-hc4/application_note/oled

Make sure to follow the instructions carefully to ensure that the necessary packages and drivers are installed.

## Usage

To use the script, simply clone this repository to your Odroid HC4 and navigate to the `odroid-HC4_oled` directory. Then, run the `sys_info.py` script with Python 3:
`sudo python3 sys_info.py`

This will display system information on the OLED display.

### Setting up the Script to Run on Startup

To automatically start the script on system startup, you can create a `systemd` service unit file. Here's how:

1. Open a terminal and navigate to the `systemd` directory:
`cd /etc/systemd/system/`

2. Create a new service unit file with the following command:
`sudo nano sys_info.service`

3. Paste the following contents into the file:<br/>
[Unit]<br/>
Description=System Information Service<br/>
[Service]<br/>
Type=simple<br/>
ExecStart=/usr/bin/python3 /path/to/sys_info.py<br/>
Restart=always<br/>
User=root<br/>
Group=root<br/>
[Install]<br/>
WantedBy=multi-user.target<br/>

Replace `/path/to/sys_info.py` with the actual path to the `sys_info.py` script.

4. Save and close the file by pressing `Ctrl + X`, then `Y`, and then `Enter`.

5. Reload `systemd` to read the new service unit file:
`sudo systemctl daemon-reload`

6. Enable the service to start automatically on system startup:
`sudo systemctl enable sys_info.service`

7. Start the service:
`sudo systemctl start sys_info.service`

That's it! The script should now start automatically on system startup and display system information on the OLED display.


## Contributing

If you find any issues with the script or have suggestions for improvements, feel free to open an issue or submit a pull request. We welcome contributions from the community!

## License

This script is released under the MIT license. See the `LICENSE` file for more information.

