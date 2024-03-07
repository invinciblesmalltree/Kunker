import json
import os


def find_container(name_or_uid):
    container_data = None
    index = 0
    with open("./containers.json", 'r') as file:
        containers_data = json.load(file)
    for container in containers_data:
        if container["name"] == name_or_uid or container["uid"] == name_or_uid:
            container_data = container
            break
        index += 1
    return container_data, index


def run_container(name_or_uid):
    container_data, index = find_container(name_or_uid)

    if container_data is None:
        print("Container not found.")
        return

    if container_data["status"] == "running":
        print("Container already running.")
        return

    os.system(
        f"cd ./containers/{container_data['name']} && tmux new-session -d -s kunker_{container_data['name']} \"runc run {container_data['uid']}\"")
    with open("./containers.json", 'r') as file:
        containers_data = json.load(file)
    containers_data[index]["status"] = "running"
    with open("./containers.json", 'w') as file:
        json.dump(containers_data, file, indent=4)
    print("Container running.")


def stop_container(name_or_uid):
    container_data, index = find_container(name_or_uid)

    if container_data is None:
        print("Container not found.")
        return

    if container_data["status"] == "stopped":
        print("Container already stopped.")
        return

    os.system(
        f"cd ./containers/{container_data['name']} && tmux kill-session -t kunker_{container_data['name']}")
    with open("./containers.json", 'r') as file:
        containers_data = json.load(file)
    containers_data[index]["status"] = "stopped"
    with open("./containers.json", 'w') as file:
        json.dump(containers_data, file, indent=4)
    print("Container stopped.")


def delete_container(name_or_uid):
    container_data, index = find_container(name_or_uid)

    if container_data is None:
        print("Container not found.")
        return

    if container_data["status"] == "running":
        os.system(
            f"cd ./containers/{container_data['name']} && tmux kill-session -t kunker_{container_data['name']}")

    os.system(f"rm -rf ./containers/{container_data['name']}")
    with open("./containers.json", 'r') as file:
        containers_data = json.load(file)
    containers_data.pop(index)
    with open("./containers.json", 'w') as file:
        json.dump(containers_data, file, indent=4)
    print("Container deleted.")


if __name__ == "__main__":
    # run_container("ubuntu")
    # stop_container("ubuntu")
    delete_container("ubuntu")
