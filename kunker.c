#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    char command[1024] = "python3 ";
    if (!strcmp(argv[1], "pull"))
        strcat(command, "/root/Kunker/download_image.py");
    else if (!strcmp(argv[1], "create"))
        strcat(command, "/root/Kunker/create_container.py");
    else if (!(strcmp(argv[1], "start") && strcmp(argv[1], "enter") &&
               strcmp(argv[1], "stop") && strcmp(argv[1], "delete") &&
               strcmp(argv[1], "list")))
        strcat(command, "/root/Kunker/operate_container.py "),
            strcat(command, argv[1]);
    else {
        printf("Unknown command \"%s\"\n", argv[1]);
        return 0;
    }
    for (int i = 2; i < argc; i++)
        strcat(command, " "), strcat(command, argv[i]);
    system(command);
    return 0;
}
