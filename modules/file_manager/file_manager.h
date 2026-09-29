#ifndef FILE_MANAGER_H
#define FILE_MANAGER_H

#define MAX_NAME 100

typedef enum {
    FILE_NODE,
    DIRECTORY_NODE
} NodeType;

typedef struct FileSystemNode {
    char name[MAX_NAME];
    NodeType type;
    int size;

    struct FileSystemNode *parent;
    struct FileSystemNode *firstChild;
    struct FileSystemNode *nextSibling;
} FileSystemNode;

FileSystemNode *createDirectory(const char *name);
FileSystemNode *createFile(const char *name, int size);

void addChild(FileSystemNode *parent, FileSystemNode *child);
void printFileSystem(FileSystemNode *root, int level);
void freeFileSystem(FileSystemNode *root);
FileSystemNode *createDirectoryInDirectory(
    FileSystemNode *parent,
    const char *name
);

FileSystemNode *createFileInDirectory(
    FileSystemNode *parent,
    const char *name,
    int size
);

int deleteNode(FileSystemNode *node);
int renameNode(FileSystemNode *node, const char *newName);
int moveNode(FileSystemNode *node, FileSystemNode *newParent);

#endif