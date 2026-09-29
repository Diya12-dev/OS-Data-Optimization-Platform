#include <stdio.h>
#include "file_manager.h"

int main(void)
{
    /* Create the root directory */
    FileSystemNode *root = createDirectory("root");

    /* Create directories */
    FileSystemNode *documents = createDirectory("Documents");
    FileSystemNode *pictures = createDirectory("Pictures");

    /* Create files */
    FileSystemNode *notes = createFile("notes.txt", 1200);
    FileSystemNode *assignment = createFile("assignment.pdf", 5000);
    FileSystemNode *photo = createFile("photo.jpg", 3500);

    /* Build the directory tree */
    addChild(root, documents);
    addChild(root, pictures);

    addChild(documents, notes);
    addChild(documents, assignment);

    addChild(pictures, photo);

    /* Display the virtual file system */
    printf("\nSMART FILE MANAGER\n");
    printf("==================\n");

    FileSystemNode *college =
    createDirectoryInDirectory(documents, "College");

    createFileInDirectory(college, "os_notes.pdf", 2500);

    printFileSystem(root, 0);

    /* Free allocated memory */
    printf("\nDeleting assignment.pdf...\n");

    if (deleteNode(assignment)) {
    printf("File deleted successfully.\n");
    }

    printf("\nFILE SYSTEM AFTER DELETE\n");
    printf("========================\n");

    printFileSystem(root, 0);
    printf("\nRenaming notes.txt to study_notes.txt...\n");

if (renameNode(notes, "study_notes.txt")) {
    printf("File renamed successfully.\n");
}

printf("\nFILE SYSTEM AFTER RENAME\n");
printf("========================\n");

printFileSystem(root, 0);
printf("\nMoving study_notes.txt from Documents to Pictures...\n");

if (moveNode(notes, pictures)) {
    printf("File moved successfully.\n");
}

printf("\nFILE SYSTEM AFTER MOVE\n");
printf("======================\n");

printFileSystem(root, 0);
    freeFileSystem(root);

    return 0;
}