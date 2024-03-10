import json
import os
import sys


def find_container(name_or_uid):
    with open("/root/Kunker/containers.json", 'r') as file:
        containers_data = json.load(file)
    for index, container in enumerate(containers_data):
        if container["name"] == name_or_uid or container["uid"] == name_or_uid:
            return index, container
    return -1, None


def run_container(name_or_uid):
    index, container_data = find_container(name_or_uid)

    if index == -1:
        print("Container not found.")
        return

    if container_data["status"] == "running":
        print("Container already running.")
        return

    os.system(
        f"cd /root/Kunker/containers/{container_data['name']} && tmux new-session -d -s kunker_{container_data['name']} \"runc run {container_data['uid']}\"")
    with open("/root/Kunker/containers.json", 'r') as file:
        containers_data = json.load(file)
    containers_data[index]["status"] = "running"
    with open("/root/Kunker/containers.json", 'w') as file:
        json.dump(containers_data, file, indent=4)
    print("Container running.")


def enter_container(name_or_uid, command="bash"):
    index, container_data = find_container(name_or_uid)

    if index == -1:
        print("Container not found.")
        return

    if container_data["status"] == "stopped":
        print("Container not running.")
        return

    os.system(f"runc exec -t {container_data['uid']} {command}")


def stop_container(name_or_uid):
    index, container_data = find_container(name_or_uid)

    if index == -1:
        print("Container not found.")
        return

    if container_data["status"] == "stopped":
        print("Container already stopped.")
        return

    os.system(
        f"cd /root/Kunker/containers/{container_data['name']} && tmux kill-session -t kunker_{container_data['name']}")
    with open("/root/Kunker/containers.json", 'r') as file:
        containers_data = json.load(file)
    containers_data[index]["status"] = "stopped"
    with open("/root/Kunker/containers.json", 'w') as file:
        json.dump(containers_data, file, indent=4)
    print("Container stopped.")


def delete_container(name_or_uid):
    index, container_data = find_container(name_or_uid)

    if index == -1:
        print("Container not found.")
        return

    if container_data["status"] == "running":
        os.system(
            f"cd /root/Kunker/containers/{container_data['name']} && tmux kill-session -t kunker_{container_data['name']}")

    os.system(f"rm -rf /root/Kunker/containers/{container_data['name']}")
    with open("/root/Kunker/containers.json", 'r') as file:
        containers_data = json.load(file)
    os.system(f"ip link delete veth{container_data['net']['id']}")
    os.system(f"ip netns delete kunker-ns{container_data['net']['id']}")
    containers_data.pop(index)
    with open("/root/Kunker/containers.json", 'w') as file:
        json.dump(containers_data, file, indent=4)
    print("Container deleted.")


def list_containers():
    print("Name\t\t\t\t\tUID\t\t\t\t\t\tStatus")
    with open("/root/Kunker/containers.json", 'r') as file:
        containers_data = json.load(file)
    for container in containers_data:
        print(f"{container['name']}" + "\t" * (
                    5 - len(container['name']) // 8) + f"({container['uid']})\t\t{container['status']}")


if __name__ == "__main__":
    if sys.argv[1] == "start":
        if len(sys.argv) > 2:
            run_container(sys.argv[2])
        else:
            print("Usage: kunker start <container_name_or_id>")
    elif sys.argv[1] == "enter":
        if len(sys.argv) > 3:
            enter_container(sys.argv[2], sys.argv[3])
        elif len(sys.argv) == 3:
            enter_container(sys.argv[2])
        else:
            print("Usage: kunker enter <container_name_or_id> [command]")
    elif sys.argv[1] == "stop":
        if len(sys.argv) > 2:
            stop_container(sys.argv[2])
        else:
            print("Usage: kunker stop <container_name_or_id>")
    elif sys.argv[1] == "delete":
        if len(sys.argv) > 2:
            delete_container(sys.argv[2])
        else:
            print("Usage: kunker delete <container_name_or_id>")
    elif sys.argv[1] == "list":
        list_containers()
