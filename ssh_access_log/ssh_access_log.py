#!/usr/bin/python3
'''
ssh_access_count.py

@bridger-herman

Counts number of times ssh has been accessed and updates it in a specified
file
'''


WATCH_FILE = '/var/log/auth.log'

SSH_SUCCESS_REGEX =
'(.+).sshd\[(\d+)\]:.Accepted.publickey.for.(\w+).from.(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).port.(\d+)(.+)'


