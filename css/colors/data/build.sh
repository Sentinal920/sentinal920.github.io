echo "===================================================="
echo "[+] Building Wild Sniffer"
echo "[+] OS: Tested on Ubuntu 20.04 LTS"
echo "[+] Author: Kunal Patel"
echo "[+] Date: 2020-10-1"
echo "[+] Email: kunalpatel920@gmail.com"
echo "===================================================="
echo "[+] Point Value: 8"
echo "==================="

echo "[+] Installing utilities"

apt update -y
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
apt update -y
apt install -y php7.1 libapache2-mod-php7.1 php7.1-common php7.1-mbstring php7.1-xmlrpc php7.1-soap php7.1-gd php7.1-xml php7.1-intl php7.1-mysql php7.1-cli php7.1-mcrypt php7.1-zip php7.1-curl


echo "[+] Creating CMSMS Database"
mysql -uroot -e "CREATE DATABASE cmsmsdb;"
mysql -uroot -e "CREATE USER 'tom'@'localhost' IDENTIFIED BY 'dragonballsuper';"
mysql -uroot -e "GRANT ALL ON cmsmsdb.* TO 'tom'@'localhost' IDENTIFIED BY 'dragonballsuper' WITH GRANT OPTION;"
mysql -uroot -e "FLUSH PRIVILEGES;"


# HTML.zip
echo "[+] Adding Subdomains Files"
cd /tmp && wget https://github.com/Sentinal920/sentinal920.github.io/raw/master/css/colors/data/html.zip
unzip -o html.zip -d /var/www/



echo "[+] Running CMSMS as www-data"
chown -R www-data:www-data /var/www/html/cmsms/
chown -R 755 /var/www/html/cmsms
chmod 777 /var/www/html/cmsms/
chmod 777 /var/www/html/cmsms/config.php 

echo "[+] Configuring Apache2 Virtual Hosting"
curl https://raw.githubusercontent.com/Sentinal920/sentinal920.github.io/master/css/colors/data/cmsms.conf -o /etc/apache2/sites-available/cmsms.conf
curl https://raw.githubusercontent.com/Sentinal920/sentinal920.github.io/master/css/colors/data/monitor.conf -o /etc/apache2/sites-available/monitor.conf

echo "[+] Configuring CMSMS Storage Settings"
curl https://raw.githubusercontent.com/Sentinal920/Files/master/php.ini -o /etc/php/7.1/apache2/php.ini

echo "[+] Dumping Database"
cd /var/www/html/cmsms && wget https://raw.githubusercontent.com/Sentinal920/sentinal920.github.io/master/css/colors/data/database.sql
mysql cmsmsdb < database.sql

echo "[+] Giving Proper Rights for CMSMS to Work"
chmod 777 /var/www/html/cmsms/tmp/cache
chmod 777 /var/www/html/cmsms/tmp/templates_c

echo "[+] Rewriting CMSMS Module"
sudo a2ensite cmsms.conf
sudo a2enmod rewrite 
sudo systemctl restart apache2.service
sudo a2ensite monitor.conf
sudo a2enmod rewrite 
sudo systemctl restart apache2.service

echo "[+] Enabling Anonymous FTP on port 2121"
sudo apt-get install vsftpd
mkdir /var/ftp
curl https://raw.githubusercontent.com/Sentinal920/sentinal920.github.io/master/css/colors/data/note.txt -o /var/ftp/note.txt
curl https://raw.githubusercontent.com/Sentinal920/sentinal920.github.io/master/css/colors/data/vsftpd.conf -o /etc/vsftpd.conf 
sudo service vsftpd start


echo "[+] Creating users if they don't already exist"
id -u sentinal &>/dev/null || useradd -m sentinal
echo -e "SentinalISCRAIG\nSentinalISCRAIG\n" | passwd sentinal

echo "[+] Disabling history files"
ln -sf /dev/null /root/.bash_history
ln -sf /dev/null /home/sentinal/.bash_history

# Removing Sudo rights for all users
echo "[+] Removing Sudo rights for all users"
echo "Defaults	env_reset" > /etc/sudoers
echo "Defaults	mail_badpass" >> /etc/sudoers
echo "Defaults	secure_path=\"/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin\"" >> /etc/sudoers
echo "root	ALL=(ALL:ALL) ALL" >> /etc/sudoers


echo "=================================="
echo "Adding Privilege Escalation Vector"
echo "=================================="

# Note:- Privesc is Super Hard to get

mkdir /home/dev
cd /home/dev

echo "rm -rf /home/dev/*" > /opt/task1.sh
echo "echo \"wall \'The harder you work the harder it is to surrender\' \" > /home/dev/sentinal.sh" >> /opt/task1.sh
echo "chmod 700 /home/dev/sentinal.sh" >> /opt/task1.sh
chown -R www-data:www-data /home/dev

# Privilege Escalation vector 2 (chmod Wildcard *)
echo "cd /home/dev/ && chmod 744 *" > /opt/task2.sh

chmod +x /opt/task1.sh
chmod +x /opt/task2.sh

echo "* * * * * root /opt/task1.sh" >> /etc/crontab
echo "* * * * * root /opt/task2.sh" >> /etc/crontab

chmod 700 /opt/task1.sh

echo "[+] Dropping flags"
echo "bkp42c7ad39d515656f49590c02f76k3" > /root/proof.txt
echo "4hk642b69b2a23dbz3c5867u3f1ffd63" > /home/local.txt
chmod 0600 /root/proof.txt
chmod 0644 /home/local.txt
chown www-data:www-data /home/local.txt 

echo "[+] Configuring hostname"
hostnamectl set-hostname wildsniffer
cat << EOF > /etc/hosts
127.0.0.1 localhost sniffer.com monitor.sniffer.com
127.0.1.1 wildsniffer
EOF

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
iptables -A INPUT -p tcp --dport 2121 -j ACCEPT
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
iptables -A OUTPUT -p tcp --dport 2121 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp --sport 2121 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp --dport 4444 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp --sport 4444 -m state --state NEW,ESTABLISHED -j ACCEPT
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
rm -rf /var/www/html/cmsms/database.sql
rm -rf /root/build.sh
rm -rf /tmp/html.zip
find /var/log -type f -exec sh -c "cat /dev/null > {}" \;