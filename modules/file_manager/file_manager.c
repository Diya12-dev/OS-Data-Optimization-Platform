#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "file_manager.h"
FileSystemNode *createDirectory(const char *name)
{
    FileSystemNode *node = malloc(sizeof(FileSystemNode));

    if (node == NULL) {
        printf("Error: Memory allocation failed.\n");
        return NULL;
    }

    strncpy(node->name, name, MAX_NAME - 1);
    node->name[MAX_NAME - 1] = '\0';

    node->type = DIRECTORY_NODE;
    node->size = 0;

    node->parent = NULL;
    node->firstChild = NULL;
    node->nextSibling = NULL;

    return node;
}
FileSystemNode *createFile(const char *name, int size)
{
    FileSystemNode *node = malloc(sizeof(FileSystemNode));

    if (node == NULL) {
        printf("Error: Memory allocation failed.\n");
        return NULL;
    }

    strncpy(node->name, name, MAX_NAME - 1);
    node->name[MAX_NAME - 1] = '\0';

    node->type = FILE_NODE;
    node->size = size;

    node->parent = NULL;
    node->firstChild = NULL;
    node->nextSibling = NULL;

    return node;
}
void addChild(FileSystemNode *parent, FileSystemNode *child)
{
    if (parent == NULL || child == NULL) {
        return;
    }

    if (parent->type != DIRECTORY_NODE) {
        printf("Error: Cannot add a child to a file.\n");
        return;
    }

    child->parent = parent;

    if (parent->firstChild == NULL) {
        parent->firstChild = child;
        return;
    }

    FileSystemNode *current = parent->firstChild;

    while (current->nextSibling != NULL) {
        current = current->nextSibling;
    }

    current->nextSibling = child;
}
void printFileSystem(FileSystemNode *root, int level)
{
    if (root == NULL) {
        return;
    }

    for (int i = 0; i < level; i++) {
        printf("    ");
    }

    if (root->type == DIRECTORY_NODE) {
        printf("[DIR] %s/\n", root->name);
    } else {
        printf("[FILE] %s (%d bytes)\n", root->name, root->size);
    }

    FileSystemNode *child = root->firstChild;

    while (child != NULL) {
        printFileSystem(child, level + 1);
        child = child->nextSibling;
    }
}
void freeFileSystem(FileSystemNode *root)
{
    if (root == NULL) {
        return;
    }

    FileSystemNode *child = root->firstChild;

    while (child != NULL) {
        FileSystemNode *next = child->nextSibling;

        freeFileSystem(child);

        child = next;
    }

    free(root);
}
FileSystemNode *createDirectoryInDirectory(
    FileSystemNode *parent,
    const char *name
)
{
    if (parent == NULL || parent->type != DIRECTORY_NODE) {
        printf("Error: Invalid parent directory.\n");
        return NULL;
    }

    FileSystemNode *newDirectory = createDirectory(name);

    if (newDirectory == NULL) {
        return NULL;
    }

    addChild(parent, newDirectory);

    return newDirectory;
}

FileSystemNode *createFileInDirectory(
    FileSystemNode *parent,
    const char *name,
    int size
)
{
    if (parent == NULL || parent->type != DIRECTORY_NODE) {
        printf("Error: Invalid parent directory.\n");
        return NULL;
    }

    if (size < 0) {
        printf("Error: File size cannot be negative.\n");
        return NULL;
    }

    FileSystemNode *newFile = createFile(name, size);

    if (newFile == NULL) {
        return NULL;
    }

    addChild(parent, newFile);

    return newFile;
}
int deleteNode(FileSystemNode *node)
{
    if (node == NULL) {
        printf("Error: Node does not exist.\n");
        return 0;
    }

    if (node->parent == NULL) {
        printf("Error: Cannot delete the root directory.\n");
        return 0;
    }

    FileSystemNode *parent = node->parent;

    /* If node is the first child */
    if (parent->firstChild == node) {
        parent->firstChild = node->nextSibling;
    }
    else {
        FileSystemNode *current = parent->firstChild;

        while (current != NULL &&
               current->nextSibling != node) {
            current = current->nextSibling;
        }

        if (current == NULL) {
            printf("Error: Node not found in parent directory.\n");
            return 0;
        }

        current->nextSibling = node->nextSibling;
    }

    node->parent = NULL;
    node->nextSibling = NULL;

    freeFileSystem(node);

    return 1;
}
int renameNode(FileSystemNode *node, const char *newName)
{
    if (node == NULL || newName == NULL || strlen(newName) == 0) {
        printf("Error: Invalid node or name.\n");
        return 0;
    }

    strncpy(node->name, newName, MAX_NAME - 1);
    node->name[MAX_NAME - 1] = '\0';

    return 1;
}

int moveNode(FileSystemNode *node, FileSystemNode *newParent)
{
    if (node == NULL || newParent == NULL) {
        printf("Error: Invalid node or destination.\n");
        return 0;
    }

    if (newParent->type != DIRECTORY_NODE) {
        printf("Error: Destination must be a directory.\n");
        return 0;
    }

    if (node->parent == NULL) {
        printf("Error: Cannot move root directory.\n");
        return 0;
    }

    FileSystemNode *oldParent = node->parent;

    /* Remove node from old parent's child list */
    if (oldParent->firstChild == node) {
        oldParent->firstChild = node->nextSibling;
    } else {
        FileSystemNode *current = oldParent->firstChild;

        while (current != NULL && current->nextSibling != node) {
            current = current->nextSibling;
        }

        if (current == NULL) {
            printf("Error: Node not found in parent directory.\n");
            return 0;
        }

        current->nextSibling = node->nextSibling;
    }

    /* Detach from old location */
    node->parent = NULL;
    node->nextSibling = NULL;

    /* Attach to new directory */
    addChild(newParent, node);

    return 1;
}