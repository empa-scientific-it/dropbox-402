# Jython dropbox for 402

## Introduction and goals
The goal of this repository is to implement an ELN-LIMS dropbox for openBIS to cover the needs of the Advanced Fibers group at Empa.
Specifically, the users want to drop measurement data (as a zip file) in a folder. Metadata regarding the date of acquisition should be extracted automatically from the contents of the zip file and used
to add a new object in a predefined collection. The object should have a datetime properties filled with the date of acquisition, so that users can sort the collection. Finally, the uploaded zip file should be attached to the object just created.

## How to test the dropbox

The project can be tested using docker. All you need is a linux system with [taskfile](https://taskfile.dev/) and docker installed. To build and test the project, you can use:

```bash
task test
```
