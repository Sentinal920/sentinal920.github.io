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
```
Index of ftp://13.72.119.96:21212/
Up to higher level directory
Name 	                    Size 	        Last Modified
File:intern-roles.txt      1 KB       01/10/20 	11:51:00 IST
File:note.txt              1 KB 	    01/10/20 	11:51:00 IST
```
Reading note.txt we know there are subdomains
```
Hey dave, 
I wont be available for the next 2 days. Please inform the new interns about their roles and assigned work.
Check the file i've uploaded for intern names and roles. They have been working on some web based networking monitoring tool for fun. Please make sure you take down any subdomains they might have created for their tool.
Regards,
Tom
```
Reading intern-roles.txt we know the usernames and domain name
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
