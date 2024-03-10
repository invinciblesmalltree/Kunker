apt update
apt install -y python3 runc tmux
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
ip link add name kunker-br0 type bridge
ip addr add 172.10.1.1/16 dev kunker-br0
ip link set dev kunker-br0 up
python3 /root/Kunker/setup.py
