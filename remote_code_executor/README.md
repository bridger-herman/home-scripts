# Remote Code Executor

A simple server to execute arbitrary shell commands on a Linux machine.

> [!WARNING]
> This is incredibly dangerous and insecure, and should only be used in a very
> specific use case.

My use case is to enable Home Assistant to monitor the health of my server so I
don't need to create a bunch of separate shell scripts for HA to execute with
the "command line" integration.

In an attempt to make this slightly less insecure:

- It's only exposed on localhost (not accessible to other devices on network)
- There's a list of "allowable named commands" which is configurable on the server side (commands.txt, separated by lines)
- Commands should only be "read" commands (i.e., no modifying the file system)
- If the command from the client doesn't match the one in the commands.txt exactly, it's ignored
