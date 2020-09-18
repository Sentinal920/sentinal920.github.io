
echo "==================================="
echo "[+] Building Senti"
echo "[+] OS: Tested on Fresh Ubuntu 20.04 LTS"
echo "[+] Author: Kunal Patel"
echo "[+] Date: 2020-09-16"
echo "[+] Email: kunalpatel920@gmail.com"
echo "==================================="
echo "[+] Point Value: 8"
echo "==================="

echo "[+] Installing utilities"

#apt -y update 
apt install -y net-tools vim open-vm-tools git

echo "============================="
echo "[+] Configuring first vector"
echo "============================="

echo "[+] Installing Apache and Mariadb"
apt install -y apache2 mariadb-server mariadb-client 
echo "[+] Installing Curl and Zip"
apt install -y curl zip unzip

echo "[+] Disabling Directory Listing on apache server"
sed -i "s/Options Indexes FollowSymLinks/Options FollowSymLinks/" /etc/apache2/apache2.conf


echo "[+] Enabling Apache2 Service"
systemctl stop apache2.service
systemctl start apache2.service
systemctl enable apache2.service

echo "[+] Enabling MariaDB Mysql Service"
systemctl stop mysql.service
systemctl start mysql.service
systemctl enable mariadb.service


echo "[+] Configuring Mysql_Secure_Installation"
[ ! -e /usr/bin/expect ] && { apt-get -y install expect; }
SECURE_MYSQL=$(expect -c "
set timeout 10
spawn mysql_secure_installation
expect \"Enter current password for root (enter for none): \"
send \"n\r\"
expect \"Switch to unix_socket authentication \[Y/n\] \"
send \"n\r\"
expect \"Change the root password? \[Y/n\] \"
send \"y\r\"
expect \"New password: \"
send \"RootisnotthathardastheysayButNotEasyEither\r\"
expect \"Re-enter new password: \"
send \"RootisnotthathardastheysayButNotEasyEither\r\"
expect \"Remove anonymous users? \[Y/n\] \"
send \"y\r\"
expect \"Disallow root login remotely? \[Y/n\] \"
send \"y\r\"
expect \"Remove test database and access to it? \[Y/n\] \"
send \"y\r\"
expect \"Reload privilege tables now? \[Y/n\] \"
send \"y\r\"
expect eof
")
systemctl restart mysql.service

echo "[+] Installing PHP"
apt install -y software-properties-common
echo "[+] Configuring PHP"
add-apt-repository ppa:ondrej/php -y 
echo "[+] Updating PHP"
apt -y update 
apt install -y php7.1 libapache2-mod-php7.1 php7.1-common php7.1-mbstring php7.1-xmlrpc php7.1-soap php7.1-gd php7.1-xml php7.1-intl php7.1-mysql php7.1-cli php7.1-mcrypt php7.1-zip php7.1-curl


# echo "[+] Original CMSMS Vulnerable to timebased SQL injection Version installation (Manual GUI Install)"
	#cd /tmp && wget http://s3.amazonaws.com/cmsms/downloads/14310/cmsms-2.2.9-install.zip
	#unzip cmsms-2.2.9-install.zip -d /var/www/html/cmsms 
# and visit site.com/cmsms-2.2.9-install.php and follow the on screen instruction
# here i'm configuring it manually to automate installing cmsms using this script.

echo "[+] Creating CMSMS Database"
mysql -uroot -e "CREATE DATABASE cmsmsdb;"
mysql -uroot -e "CREATE  USER 'juniordev'@'localhost' IDENTIFIED BY 'passion';"
mysql -uroot -e "GRANT ALL ON cmsmsdb.* TO 'juniordev'@'localhost' IDENTIFIED BY 'passion' WITH GRANT OPTION;"
mysql -uroot -e "FLUSH PRIVILEGES;"

echo "[+] Downloading Pre-Installed CMSMS Files"
cd /tmp && wget https://github.com/Sentinal920/Files/raw/master/html.zip
unzip -o html.zip -d /var/www/

echo "[+] Running CMSMS as www-data"
chown -R www-data:www-data /var/www/html/cmsms/
chown -R 755 /var/www/html/cmsms
chmod 777 /var/www/html/cmsms/

echo "[+] Configuring Apache2"
curl https://raw.githubusercontent.com/Sentinal920/Files/master/cmsms.conf -o /etc/apache2/sites-available/cmsms.conf

echo "[+] Configuring CMSMS Storage Settings"
curl https://raw.githubusercontent.com/Sentinal920/Files/master/php.ini -o /etc/php/7.1/apache2/php.ini

echo "[+] Dumping Database"
cd /var/www/html/cmsms && wget https://github.com/Sentinal920/Files/raw/master/dump.sql
mysql cmsmsdb < dump.sql

echo "[+] Giving Proper Rights for CMSMS to Work"
chmod 777 /var/www/html/cmsms/tmp/cache
chmod 777 /var/www/html/cmsms/tmp/templates_c

echo "[+] Rewriting CMSMS Module"
a2ensite cmsms.conf 
a2enmod rewrite
systemctl restart apache2.service



# Adding Users and Stuff

echo "[+] Creating users if they don't already exist"
id -u sentinal &>/dev/null || useradd -m sentinal
echo -e "SentinalISCRAIG\nSentinalISCRAIG\n" | passwd sentinal
id -u juniordev &>/dev/null || useradd -m juniordev
echo -e "passion\npassion\n" | passwd juniordev


echo "[+] Disabling history files"
ln -sf /dev/null /root/.bash_history
ln -sf /dev/null /home/sentinal/.bash_history
ln -sf /dev/null /home/juniordev/.bash_history

echo "[+] Configuring hostname"
hostnamectl set-hostname sentinal
cat << EOF > /etc/hosts
127.0.0.1 localhost sentinal.com
127.0.1.1 sentinal920
EOF

echo "[+] Enabling SSH"
apt -y install openssh-server



echo "============================="
echo "[+] Configuring Second Vector"
echo "============================="

#USER PRIVESC CRON JOB (juniordev {USER1}  -->  sentinal {USER2})
echo "[+] Adding Cron Job"
echo "* * * * * sentinal /home/sentinal/Pictures/sentinal.sh" >> /etc/crontab
cd /home/sentinal/Pictures && echo "cat /home/sentinal/.ssh/id_rsa" > sentinal.sh
chmod 776 sentinal.sh

#ROOT PRIVESC (User Sentinal can run zip as sudo)
echo "[+] Modifying permissions for user Sentinal"
echo "Defaults	env_reset" > /etc/sudoers
echo "Defaults	mail_badpass" >> /etc/sudoers
echo "Defaults	secure_path=\"/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin\"" >> /etc/sudoers
echo "root	ALL=(ALL:ALL) ALL" >> /etc/sudoers
echo "sentinal ALL=(ALL) NOPASSWD:/bin/zip" >> /etc/sudoers

echo "[+] Dropping flags"
echo "ba742c7ad39d517527f49590c02f76k9" > /root/proof.txt
echo "4h1642b69b2a23bca3c5867u3f1ffd60" > /home/sentinal/local.txt
chmod 0600 /root/proof.txt
chmod 0640 /home/sentinal/local.txt
chown sentinal:sentinal /home/sentinal/local.txt 





echo "========================"
echo "[+] Configuring firewall"
echo "========================"

echo "[+] Installing iptables"
echo "iptables-persistent iptables-persistent/autosave_v4 boolean false" | debconf-set-selections
echo "iptables-persistent iptables-persistent/autosave_v6 boolean false" | debconf-set-selections
apt install -y iptables-persistent
#
# Note: Unless specifically required as part of the exploitation path, please
#       ensure that inbound ICMP and SSH on port 22 are permitted.
#
echo "[+] Applying inbound firewall rules"
iptables -I INPUT 1 -i lo -j ACCEPT
iptables -A INPUT -m conntrack --ctstate NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
iptables -A INPUT -p icmp --icmp-type echo-reply -j ACCEPT
iptables -A INPUT -j DROP
#
# Note: Unless specifically required as part of the exploitation path, please
#       ensure that outbound ICMP, DNS (TCP & UDP) on port 53 and SSH on port 22
#       are permitted.
#
echo "[+] Applying outbound firewall rules"
iptables -A OUTPUT -o lo -j ACCEPT
iptables -A OUTPUT -p tcp --sport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p udp --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp --sport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p icmp --icmp-type echo-request -j ACCEPT
iptables -A OUTPUT -p icmp --icmp-type echo-reply -j ACCEPT
iptables -A OUTPUT -j DROP

echo "[+] Saving firewall rules"
service netfilter-persistent save

echo "[+] Disabling IPv6"
echo "net.ipv6.conf.all.disable_ipv6 = 1" >> /etc/sysctl.conf
echo "net.ipv6.conf.default.disable_ipv6 = 1" >> /etc/sysctl.conf
sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT=""/GRUB_CMDLINE_LINUX_DEFAULT="ipv6.disable=1"/' /etc/default/grub
sed -i 's/GRUB_CMDLINE_LINUX=""/GRUB_CMDLINE_LINUX="ipv6.disable=1"/' /etc/default/grub
update-grub


echo "[+] Cleaning up"
rm -rf /var/www/html/cmsms/dump.sql
rm -rf /root/build.sh
find /var/log -type f -exec sh -c "cat /dev/null > {}" \;
