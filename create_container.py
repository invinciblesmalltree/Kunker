import json
import os
import uuid


def create_config(name):
    if not os.path.exists(f"./containers/{name}/rootfs/"):
        os.makedirs(f"./containers/{name}/rootfs/")
    os.system(f"cp ./images/configs/config.json ./containers/{name}/config.json")


def read_layer(image, tag):
    with open(f"./images/manifests/{image}/{tag}/layers.json", 'r') as file:
        layer_data = json.load(file)
    return layer_data


def unpack_layer(name, digest):
    os.system(f"tar zxf ./images/files/{digest.split(':')[1]}.tar -C ./containers/{name}/rootfs/")


def create_container(name, image, tag="latest", command=None, hostname="kunker", cwd="/"):
    if command is None:
        command = ["bash"]
    if not image.count("/"):
        image = "library/" + image

    create_config(name)
    with open(f"./containers/{name}/config.json", 'r') as file:
        config_data = json.load(file)
    config_data["process"]["args"] = command
    config_data["root"]["path"] = f"/root/Kunker/containers/{name}/rootfs/"
    config_data["hostname"] = hostname
    config_data["cwd"] = cwd
    with open(f"./containers/{name}/config.json", 'w') as file:
        json.dump(config_data, file, indent=4)
    print("Config created.")

    os.system(f"cp /etc/resolv.conf ./containers/{name}/rootfs/etc/resolv.conf")

    layer_list = read_layer(image, tag)
    print("Layer List obtained.")

    print("Layers:")
    for layer in layer_list:
        unpack_layer(name, layer["digest"])
        print(f"Unpacking {layer['digest']}")

    if not os.path.exists(f"./containers.json"):
        with open("./containers.json", 'w') as file:
            json.dump([], file, indent=4)
    with open("./containers.json", 'r+') as file:
        containers_data = json.load(file)
        file.seek(0)
        uid = str(uuid.uuid4())
        containers_data.append({"name": name, "uid": uid, "status": "stopped"})
        json.dump(containers_data, file, indent=4)
    print(f"Container created: {uid}")


if __name__ == "__main__":
    # create_container("busybox", "library/busybox", "latest", "sh")
    create_container("ubuntu", "library/ubuntu", "latest", hostname="insmtr")
