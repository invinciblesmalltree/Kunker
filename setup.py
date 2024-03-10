import json
import os
import re
import subprocess


def get_default_route_interface():
    try:
        result = subprocess.run(["ip", "route", "show", "default"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        output = result.stdout
        match = re.search(r'default via \S+ dev (\S+)', output)
        if match:
            return match.group(1)
        return None
    except Exception as e:
        return None


os.system("ip link add name kunker-br0 type bridge")
os.system("ip addr add 172.10.1.1/16 dev kunker-br0")
os.system("ip link set dev kunker-br0 up")

with open("/root/Kunker/containers.json", 'r') as file:
    containers_data = json.load(file)
for index, container in enumerate(containers_data):
    os.system(f"ip netns add kunker-ns{container['net']['id']}")
    os.system(f"ip link add veth{container['net']['id']} type veth peer name kunker-eth{container['net']['id']}")
    os.system(f"ip link set kunker-eth{container['net']['id']} netns kunker-ns{container['net']['id']}")
    os.system(f"ip link set veth{container['net']['id']} master kunker-br0")
    os.system(f"ip link set veth{container['net']['id']} up")
    os.system(
        f"ip netns exec kunker-ns{container['net']['id']} ip addr add {container['net']['ip']}/16 dev kunker-eth{container['net']['id']}")
    os.system(f"ip netns exec kunker-ns{container['net']['id']} ip link set kunker-eth{container['net']['id']} up")
    os.system(f"ip netns exec kunker-ns{container['net']['id']} ip route add default via 172.10.1.1")
    if container["status"] == "running":
        containers_data[index]["status"] = "stopped"
with open("/root/Kunker/containers.json", 'w') as file:
    json.dump(containers_data, file, indent=4)
os.system("sysctl -w net.ipv4.ip_forward=1")
os.system(f"iptables -t nat -A POSTROUTING -s 172.10.0.0/16 -o {get_default_route_interface()} -j MASQUERADE")
