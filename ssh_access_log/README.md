## Purpose

This service makes it easier to tell if/when someone SSHes into the server, to
be reportable to Home Assistant.


## Setup and installation

This service depends on systemd and systemd file watching.


To get it set up, run the following commands from this directory:


```bash
sudo cp ssh-access-watcher.* /etc/systemd/system

sudo systemctl enable ssh-access-watcher.service ssh-access-watcher.path

sudo systemctl start ssh-access-watcher.service ssh-access-watcher.path
```

You may need to adjust the path for `copy_ssh_log.sh` if that changed for any
reason.






## Design Documentation


I went through several iterations of thinking about this:

1. Could have HA watch `/var/log/auth.log` directly (doesn't work because HA
   is running in container)

2. Could create a bindmount for /var/log (LOL biiiiig security problem)

3. Could run a local server that HA pings to have full access to
   `/var/log/auth.log` (still kinda security, and unnecessary usage of local
   port)

4. Just watch `/var/log/auth.log` and copy the relevant parts to a
   HA-accessible directory (e.g., ~/ha_config)



We're going with Option 4 here.


The script `copy_ssh_log.sh` does the bulk of the work, the other files just
handle the setup / file watching. If everything is set up correctly, the script will be run anytime `/var/log/auth.log` is changed.


Effectively we need to:

1. Log that we're starting
2. Gather the contents of `/var/log/auth.log`
3. Copy only the contents that match the following regex (accepted
   publickey/password from sshd):
4. Paste the contents into a HA-accessible file




I thought I'd need the following regex but I think I'll just do `grep sshd`

```
(.+).sshd\[(\d+)\]:.Accepted.(\w+).for.(\w+).from.(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).port.(\d+)(.+)
```
