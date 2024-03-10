apt update
apt install python3
mkdir /root/Kunker
cp -r ./* /root/Kunker
chmod +x /root/Kunker/kunker
ln -s /root/Kunker/kunker /usr/bin/kunker
cat << EOF > /etc/systemd/system/kunker.service
[Unit]
Description=Kunker setup

[Service]
ExecStart=python3 /root/Kunker/setup.py

[Install]
WantedBy=multi-user.target
EOF
systemctl enable kunker
