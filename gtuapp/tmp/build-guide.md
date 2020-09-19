# Build Guide for Sentinal

## Status

**NTP**: Off  
**Firewall**: On  
**Updates**: Off  
**ICMP**: On  
**IPv6**: Off  
**AV or Security**: Off

## Overview

**OS**: Ubuntu 20.04 LTS  
**Hostname**: Sentinal  
**Vulnerability 1**: Time based SQL Injection  
**Vulnerability 2**: Cronjob + Weak Sudo Permission  
**High Priv Username**: sentinal  
**High Priv Password**: SentinalISCRAIG  
**Low Priv Username**: juniordev  
**Low Priv Password**: passion  
**Location of local.txt**: /home/sentinal/local.txt  
**Value of local.txt**: 4h1642b69b2a23bca3c5867u3f1ffd60  
**Location of proof.txt**: /root/proof.txt  
**Value of proof.txt**: ba742c7ad39d517527f49590c02f76k9

## Required Settings

**CPU**: 1 CPU  
**Memory**: 2GB  
**Disk**: 10GB

## Build Guide

1. Install Ubuntu 20.04 LTS
2. During installation make a user with name `sentinal` and password `SentinalISCRAIG`
3. Enable network connectivity
4. Ensure machine is fully updated by running `apt update`
5. Change to `/root` and Upload the following file to `/root`
    - `build.sh`
6. Give file executable permission
    - `chmod +x build.sh`
6. Run `./build.sh`
