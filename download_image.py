import os
import requests
import sys


def get_token(image):
    url = f"https://auth.docker.io/token?service=registry.docker.io&scope=repository:{image}:pull"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["token"]


def get_manifest_list(image, tag, token):
    headers = {'Authorization': f'Bearer {token}',
               'Accept': 'application/vnd.docker.distribution.manifest.list.v2+json'}
    url = f"https://registry-1.docker.io/v2/{image}/manifests/{tag}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def find_platform_manifest(manifest_list, architecture='amd64', system='linux'):
    for manifest in manifest_list["manifests"]:
        if manifest["platform"]["architecture"] == architecture and manifest["platform"]["os"] == system:
            return manifest
    return None


def get_layer_list(image, digest, token):
    headers = {'Authorization': f'Bearer {token}',
               'Accept': 'application/vnd.oci.image.manifest.v1+json'}
    url = f"https://registry-1.docker.io/v2/{image}/manifests/{digest}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["layers"]


def get_layer(image, digest, token):
    if not os.path.exists(f"/root/Kunker/images/files/"):
        os.makedirs(f"/root/Kunker/images/files/")
    if not os.path.exists(f"/root/Kunker/images/files/{digest.split(':')[1]}.tar"):
        headers = {'Authorization': f'Bearer {token}',
                   'Accept': 'application/vnd.oci.image.layer.v1.tar+gzip'}
        url = f"https://registry-1.docker.io/v2/{image}/blobs/{digest}/"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        with open(f"/root/Kunker/images/files/{digest.split(':')[1]}.tar", 'wb') as f:
            f.write(response.content)


def write_layer(image, layer_list, tag):
    if not os.path.exists(f"/root/Kunker/images/manifests/{image}/{tag}/"):
        os.makedirs(f"/root/Kunker/images/manifests/{image}/{tag}/")
    layer_data = str(layer_list).replace("'", '"')
    with open(f"/root/Kunker/images/manifests/{image}/{tag}/layers.json", 'w') as file:
        file.write(layer_data)


def download_image(image, tag="latest"):
    if not image.count("/"):
        image = "library/" + image

    token = get_token(image)
    print(f"Token: {token[:30]}...")

    manifest_list = get_manifest_list(image, tag, token)
    print("Manifest List obtained.")

    platform_manifest = find_platform_manifest(manifest_list)
    if platform_manifest:
        print(f"Found platform manifest: {platform_manifest['digest']}")
    else:
        print("Platform manifest not found.")
        return

    layer_list = get_layer_list(image, platform_manifest["digest"], token)
    print("Layer List obtained.")

    print("Layers:")
    for layer in layer_list:
        print(layer["digest"])
        get_layer(image, layer["digest"], token)
    write_layer(image, layer_list, tag)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        download_image(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        download_image(sys.argv[1])
    else:
        print("Usage: kunker pull <images> [tag]")
    # download_image("library/ubuntu", "latest")
    # download_image("itzg/minecraft-server", "latest")
    # download_image("library/busybox", "latest")
