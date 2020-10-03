apt update

sudo apt-get install apache2 libapache2-mod-php mysql-server libnet-snmp-perl libcrypt-rijndael-perl libcrypt-hcesha-perl libcrypt-des-perl libdigest-hmac-perl libio-pty-perl libnet-telnet-perl libalgorithm-diff-perl librrds-perl php-mysql php-snmp php-gd rrdtool libsocket6-perl
sudo apt-get install php-dev libmcrypt-dev gcc make autoconf libc-dev pkg-config
sudo pecl install mcrypt-1.0.1
echo "extension=mcrypt.so" | sudo tee -a /etc/php/7.2/apache2/conf.d/mcrypt.ini
sudo service apache2 restart

mkdir /opt/nedi
cd /opt/nedi
wget http://www.nedi.ch/pub/nedi-1.9C.pkg
tar zxf nedi-1.9C.pkg

sudo chown -R www-data:www-data /opt/nedi
sudo chmod 775 /opt/nedi/html/log/

sudo ln -s /opt/nedi/html/ /var/www/

sudo ln -s /opt/nedi/nedi.conf /etc/nedi.conf

sudo mysqladmin -u root -p password "dragonballzuper"

cd /opt/nedi/
./nedi.pl -i

