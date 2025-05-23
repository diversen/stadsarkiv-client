# systemd

Create a systemd service file for the stadsarkiv-client. E.g.:

    sudo vim /etc/systemd/system/maya.service

```
[Unit]
Description=Stadsarkiv Client Service
After=network.target

[Service]
# gunicorn
Type=simple

# run as
User=www-data
WorkingDirectory=/var/www/stadsarkiv-client
ExecStart=/var/www/stadsarkiv-client/venv/bin/python -m maya server-prod maya_root --port 5555

# restart on failure
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target

```

## enable

    sudo systemctl enable maya.service

## disable

    sudo systemctl disable maya.service

## remove

    sudo rm /etc/systemd/system/maya.service 

## reload systemd

E.g. you can edit the service file, but then remember to reload systemd.
    
    sudo systemctl daemon-reload

## start, stop or restart a service
    
    sudo systemctl start maya.service
    sudo systemctl stop maya.service
    sudo systemctl restart maya.service

## status of a service

E.g. you want to see the main process id of the service.
    
    sudo systemctl status maya.service

# Upgrade and restart service

See: [bin/upgrade.sh](https://github.com/aarhusstadsarkiv/stadsarkiv-client/blob/main/bin/upgrade.sh)

The above script will upgrade the source code to the latest tag. 

Run it like this: `./bin/upgrade.sh`

Then restart the service.

    sudo systemctl restart maya.service

## Multiple services

In the case of multiple services (or a just a single one), you can create a script that upgrades and restarts all services.

E.g.:

```bash
#!/bin/sh
cd stadsarkiv-client-demo
./bin/upgrade.sh
cp -rf ./sites/demo/* maya_root/
sudo service stadsarkiv-client-demo restart

cd stadarkiv-client-demo-2
./bin/upgrade.sh
cp -rf ./sites/demo-2/* maya_root/
sudo service stadsarkiv-client-demo-2 restart

```

# Logs

You can see the logs of the service with:

    sudo journalctl -u maya.service
