echo "[+] Building Senti"
echo "[+] OS: Tested on Ubuntu 20.04 LTS"
echo "[+] Author: Kunal Patel"
echo "[+] Date: 2020-09-16"
echo "[+] Email: kunalpatel920@gmail.com"

echo "[+] Point Value: 8"

echo "[+] Installing utilities"
sudo apt-get update -y
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

echo "Adding Mysql_Secure_Installation"
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
apt -y install php7.1 libapache2-mod-php7.1 php7.1-common php7.1-mbstring php7.1-xmlrpc php7.1-soap php7.1-gd php7.1-xml php7.1-intl php7.1-mysql php7.1-cli php7.1-mcrypt php7.1-zip php7.1-curl


echo "[+] Creating CMSMS Database"
mysql -uroot -e "CREATE DATABASE cmsmsdb;"
mysql -uroot -e "CREATE  USER 'juniordev'@'localhost' IDENTIFIED BY 'passion';"
mysql -uroot -e "GRANT ALL ON cmsmsdb.* TO 'juniordev'@'localhost' IDENTIFIED BY 'passion' WITH GRANT OPTION;"
mysql -uroot -e "FLUSH PRIVILEGES;"

echo "[+] Downloading CMSMS Vulnerable Version"
cd /tmp && wget http://s3.amazonaws.com/cmsms/downloads/14310/cmsms-2.2.9-install.zip

unzip cmsms-2.2.9-install.zip -d /var/www/html/cmsms

echo "[+] Giving www-data Permission to run CMSMS"
chown -R www-data:www-data /var/www/html/cmsms/
chown -R 755 /var/www/html/cmsms
chmod 777 /var/www/html/cmsms/
chmod 777 /var/www/html/cmsms/cmsms-2.2.9-install.php

echo "[+] Configuring Apache2"
curl https://raw.githubusercontent.com/Sentinal920/Files/master/cmsms.conf -o /etc/apache2/sites-available/cmsms.conf

echo "[+] Downloading Installed CMSMS"
cd /tmp/
wget https://github.com/Sentinal920/Files/raw/master/html.zip
unzip html.zip -d /var/www/

echo "[+] Configuring CMSMS Settings"
curl https://raw.githubusercontent.com/Sentinal920/Files/master/php.ini -o /etc/php/7.1/apache2/php.ini

echo "[+] Rewriting CMSMS Module"
a2ensite cmsms.conf 
a2enmod rewrite
systemctl restart apache2.service


echo "[+] Creating users if they don't already exist"
id -u juniordev &>/dev/null || useradd -m juniordev
echo -e "passion\npassion\n" | passwd juniordev

id -u sentinal &>/dev/null || useradd -m sentinal
echo -e "SentinalISCRAIG\nSentinalISCRAIG\n" | passwd sentinal

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
