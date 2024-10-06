# 使用方法

## 安装

下载release里的包，解压，进入对应的文件夹，运行

```sh
sudo ./install
```

因为安装之后文件将释放到`/root/Kunker`，因此请确保用root用户运行

## 基本命令

1. 拉取镜像

   ```sh
   sudo kunker pull <images> [tag]
   ```

   举例：

   ```sh
   sudo kunker pull ubuntu	
   ```

2. 创建容器

   ```sh
   sudo kunker create name=<name> image=<image> [tag=<tag>] [cmd=<command>] [hostname=<hostname>] [cwd=<cwd>]
   ```

   举例：

   ```sh
   sudo kunker create name=ubuntu image=ubuntu hostname=ubuntu
   ```

3. 启动容器

   ```sh
   sudo kunker start <container_name_or_id>
   ```

   举例：

   ```sh
   sudo kunker start ubuntu
   ```

4. 进入容器

   ```sh
   sudo kunker enter <container_name_or_id> [command]
   ```

   举例：

   ```sh
   sudo kunker enter ubuntu bash
   ```

5. 停止容器

   ```sh
   sudo kunker stop <container_name_or_id>
   ```

   举例：

   ```sh
   sudo kunker stop ubuntu
   ```

6. 删除容器

   ```sh
   sudo kunker delete <container_name_or_id>
   ```

   举例：

   ```sh
   sudo kunker delete ubuntu
   ```

7. 列出容器

   ```sh
   sudo kunker list
   ```

## 其他注意事项

拉取镜像的时候如果是非library的镜像，请在镜像前面补齐作者名字，用斜杠分隔，比如：

```sh
sudo kunker pull itzg/minecraft-server
sudo kunker create name=mc image=itzg/minecraft-server
```

创建或进入容器时如未指定启动的程序，则将默认使用bash，因此如果使用busybox之类的比较精简的镜像，请手动指定启动命令为sh（或其它shell）。

如想使用网络的话，请禁用ufw，本程序使用iptables来管理。