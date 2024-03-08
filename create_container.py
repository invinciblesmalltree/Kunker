import json
import os
import sys
import uuid


def read_layer(image, tag):
    with open(f"/root/Kunker/images/manifests/{image}/{tag}/layers.json", 'r') as file:
        layer_data = json.load(file)
    return layer_data


def unpack_layer(name, digest):
    os.system(f"tar zxf /root/Kunker/images/files/{digest.split(':')[1]}.tar -C /root/Kunker/containers/{name}/rootfs/")


def create_container(name, image, tag="latest", command=None, hostname="kunker", cwd="/"):
    if command is None:
        command = ["bash"]

    if not image.count("/"):
        image = "library/" + image

    if os.path.exists(f"/root/Kunker/containers/{name}/"):
        print("Container already exists.")
        return

    if not os.path.exists(f"/root/Kunker/images/manifests/{image}/{tag}/layers.json"):
        print("Image not found.")
        return

    os.makedirs(f"/root/Kunker/containers/{name}/rootfs/")

    with open(f"/root/Kunker/images/configs/config.json", 'r') as file:
        config_data = json.load(file)
    config_data["process"]["args"] = command
    config_data["root"]["path"] = f"/root/Kunker/containers/{name}/rootfs/"
    config_data["hostname"] = hostname
    config_data["cwd"] = cwd
    with open(f"/root/Kunker/containers/{name}/config.json", 'w') as file:
        json.dump(config_data, file, indent=4)
    print("Config created.")

    layer_list = read_layer(image, tag)
    print("Layer List obtained.")

    print("Layers:")
    for layer in layer_list:
        unpack_layer(name, layer["digest"])
        print(f"Unpacking {layer['digest']}")

    os.system(f"cp -f /etc/resolv.conf /root/Kunker/containers/{name}/rootfs/etc/resolv.conf")

    if not os.path.exists(f"/root/Kunker/containers.json"):
        with open("/root/Kunker/containers.json", 'w') as file:
            json.dump([], file, indent=4)
    with open("/root/Kunker/containers.json", 'r') as file:
        containers_data = json.load(file)
    uid = str(uuid.uuid4())
    containers_data.append({"name": name, "uid": uid, "status": "stopped"})
    with open("/root/Kunker/containers.json", 'w') as file:
        json.dump(containers_data, file, indent=4)
    print(f"Container created: {uid}")


if __name__ == "__main__":
    args = {}
    for arg in sys.argv[1:]:
        if arg.count("="):
            key, value = arg.split("=")
            args[key] = value
    if "cmd" in args:
        if args["cmd"].count("["):
            args["cmd"] = json.load(args["cmd"])
        if not args["cmd"] is list:
            print("Command must be a list.")
            exit(0)
    else:
        args["cmd"] = ["bash"]
    if "name" in args and "image" in args:
        create_container(args["name"], args["image"], args.get("tag", "latest"), args.get("cmd"),
                         args.get("hostname", "kunker"), args.get("cwd", "/"))
    else:
        print(
            "Usage: kunker create name=<name> image=<image> [tag=<tag>] [cmd=<command>] [hostname=<hostname>] [cwd=<cwd>]")
